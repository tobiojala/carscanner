from statistics import mean

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models import Deal

router = APIRouter(prefix="/compare", tags=["compare"])


class CompareDealsRequest(BaseModel):
    deal_ids: list[int] = Field(min_length=2, max_length=4)


class CompareDealItem(BaseModel):
    id: int
    title: str
    source: str
    year: int
    mileage_km: int
    price_eur: float
    total_landed_cost_sek: float
    estimated_swedish_price_sek: float
    expected_profit_sek: float
    margin_percent: float
    confidence_score: int
    risk_score: int
    liquidity_score: int
    deal_grade: str
    status: str
    risk_flags: list[str]
    recommended_max_bid_eur: float


class CompareDealsResponse(BaseModel):
    deals: list[CompareDealItem]
    best_profit_deal_id: int | None
    best_confidence_deal_id: int | None
    lowest_risk_deal_id: int | None
    average_expected_profit_sek: float


class CompareVerdictResponse(BaseModel):
    verdict: str
    best_deal_id: int | None
    reasons: list[str]
    cautions: list[str]


def _deal_title(deal: Deal) -> str:
    listing = deal.foreign_listing
    trim = listing.trim or listing.variant
    return f"{listing.year} {listing.brand} {listing.model}{f' {trim}' if trim else ''}"


def _to_compare_item(deal: Deal) -> CompareDealItem:
    listing = deal.foreign_listing
    return CompareDealItem(
        id=deal.id,
        title=_deal_title(deal),
        source=listing.source,
        year=listing.year,
        mileage_km=listing.mileage_km,
        price_eur=float(listing.price_eur),
        total_landed_cost_sek=float(deal.total_landed_cost_sek),
        estimated_swedish_price_sek=float(deal.estimated_swedish_price_sek),
        expected_profit_sek=float(deal.expected_profit_sek),
        margin_percent=float(deal.margin_percent),
        confidence_score=deal.confidence_score,
        risk_score=deal.risk_score,
        liquidity_score=deal.liquidity_score,
        deal_grade=deal.deal_grade,
        status=deal.status,
        risk_flags=deal.risk_flags,
        recommended_max_bid_eur=float(deal.recommended_max_bid_eur),
    )


def _load_deals(db: Session, deal_ids: list[int]) -> list[Deal]:
    unique_ids = list(dict.fromkeys(deal_ids))
    deals = db.scalars(
        select(Deal)
        .options(selectinload(Deal.foreign_listing))
        .where(Deal.id.in_(unique_ids))
    ).all()
    by_id = {deal.id: deal for deal in deals}
    ordered = [by_id[deal_id] for deal_id in unique_ids if deal_id in by_id]
    if len(ordered) < 2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="At least two valid deals are required for comparison",
        )
    return ordered


@router.post("/deals", response_model=CompareDealsResponse)
def compare_deals(
    payload: CompareDealsRequest,
    db: Session = Depends(get_db),
) -> CompareDealsResponse:
    deals = _load_deals(db, payload.deal_ids)
    items = [_to_compare_item(deal) for deal in deals]

    return CompareDealsResponse(
        deals=items,
        best_profit_deal_id=max(items, key=lambda item: item.expected_profit_sek).id,
        best_confidence_deal_id=max(items, key=lambda item: item.confidence_score).id,
        lowest_risk_deal_id=min(items, key=lambda item: item.risk_score).id,
        average_expected_profit_sek=round(mean(item.expected_profit_sek for item in items), 2),
    )


@router.post("/ai-verdict", response_model=CompareVerdictResponse)
def compare_ai_verdict(
    payload: CompareDealsRequest,
    db: Session = Depends(get_db),
) -> CompareVerdictResponse:
    deals = _load_deals(db, payload.deal_ids)
    items = [_to_compare_item(deal) for deal in deals]
    ranked = sorted(
        items,
        key=lambda item: (
            item.expected_profit_sek,
            item.confidence_score,
            -item.risk_score,
            item.liquidity_score,
        ),
        reverse=True,
    )
    best = ranked[0]

    reasons = [
        f"Highest blended score candidate: {best.title}",
        f"Expected profit {round(best.expected_profit_sek):,} SEK with {best.margin_percent}% margin",
        f"Confidence {best.confidence_score}/100 and risk {best.risk_score}/100",
    ]
    cautions: list[str] = []
    for item in ranked:
        if item.risk_score >= 55:
            cautions.append(f"{item.title}: elevated risk score ({item.risk_score})")
        if item.confidence_score < 60:
            cautions.append(f"{item.title}: confidence below 60")
        if item.expected_profit_sek < 20_000:
            cautions.append(f"{item.title}: profit below 20,000 SEK threshold")
        if item.risk_flags:
            cautions.append(f"{item.title}: {', '.join(item.risk_flags[:3])}")

    verdict = (
        f"Prefer {best.title} for manual follow-up, assuming the Swedish comps and service history check out. "
        "Do not buy based on this comparison alone; verify listing condition, ownership, service history, and live Swedish comps."
    )

    return CompareVerdictResponse(
        verdict=verdict,
        best_deal_id=best.id,
        reasons=reasons,
        cautions=cautions[:8],
    )
