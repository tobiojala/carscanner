import csv
from collections import Counter
from decimal import Decimal
from io import StringIO
from statistics import mean
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import CarListing, CostAssumption, Deal, ModelResearch, SwedishComparable
from app.schemas import (
    ComparableCreate,
    ComparableRead,
    CsvImportResponse,
    ConfidenceExplanationRead,
    ActualOutcomeUpdate,
    ActualOutcomeRead,
    ModelResearchUpdate,
    ModelResearchRead,
    DealStatusUpdate,
    CostAssumptionUpdate,
    CostAssumptionRead,
    CostBreakdown,
    DashboardSummary,
    DealCalculateRequest,
    DealDetailRead,
    DealOpportunityRead,
    ListingCreate,
    ListingRead,
    ListingUpdate,
)
from app.scoring import (
    ActualOutcomeInput,
    DealScoringInput,
    ProfitCalculationInput,
    calculate_actual_outcome,
    calculate_profit,
    score_deal,
)

REJECT_REASONS = {
    "Profit too low",
    "Weak Swedish comps",
    "Mileage too high",
    "Bad trim/spec",
    "Missing service history",
    "Accident/damage risk",
    "Seller risk",
    "Price too high",
    "Duplicate listing",
    "Other",
}

CSV_REQUIRED_COLUMNS = {
    "source",
    "listing_url",
    "brand",
    "model",
    "year",
    "mileage_km",
    "price_eur",
    "seller_country",
    "seller_type",
    "fuel_type",
    "transmission",
    "trim",
    "notes",
}

ALLOWED_DEAL_STATUSES = {
    "new",
    "researching",
    "contacted",
    "negotiating",
    "bought",
    "imported",
    "listed_in_sweden",
    "sold",
    "rejected",
}


def _money(value: object) -> float:
    return float(value or 0)


def _decimal(value: float | Decimal | None, fallback: Decimal) -> Decimal:
    if value is None:
        return fallback
    return Decimal(str(value))


def _actual_outcome(deal: Deal) -> ActualOutcomeRead:
    return ActualOutcomeRead(
        actual_purchase_price_sek=_money(deal.actual_purchase_price_sek) if deal.actual_purchase_price_sek is not None else None,
        actual_transport_cost_sek=_money(deal.actual_transport_cost_sek) if deal.actual_transport_cost_sek is not None else None,
        actual_registration_cost_sek=_money(deal.actual_registration_cost_sek) if deal.actual_registration_cost_sek is not None else None,
        actual_repair_cost_sek=_money(deal.actual_repair_cost_sek) if deal.actual_repair_cost_sek is not None else None,
        actual_total_cost_sek=_money(deal.actual_total_cost_sek) if deal.actual_total_cost_sek is not None else None,
        actual_sale_price_sek=_money(deal.actual_sale_price_sek) if deal.actual_sale_price_sek is not None else None,
        actual_profit_sek=_money(deal.actual_profit_sek) if deal.actual_profit_sek is not None else None,
        days_to_sell=deal.days_to_sell,
        lesson_learned=deal.lesson_learned,
    )


def _confidence_explanation(deal: Deal) -> ConfidenceExplanationRead:
    raw = deal.confidence_explanation or {}
    return ConfidenceExplanationRead(
        score=int(raw.get("score", deal.confidence_score)),
        positive_factors=list(raw.get("positive_factors", [])),
        negative_factors=list(raw.get("negative_factors", [])),
        missing_data=list(raw.get("missing_data", [])),
        comparable_count=int(raw.get("comparable_count", 0)),
        summary=raw.get("summary") or (
            f"Confidence {deal.confidence_score}/100. Detailed factors were not stored for this older calculation."
        ),
    )


def _to_listing_read(listing: CarListing) -> ListingRead:
    return ListingRead(
        id=listing.id,
        source=listing.source,
        source_listing_id=listing.source_listing_id,
        listing_url=listing.listing_url,
        seller_country=listing.seller_country,
        seller_type=listing.seller_type,
        brand=listing.brand,
        model=listing.model,
        variant=listing.variant,
        trim=listing.trim,
        year=listing.year,
        mileage_km=listing.mileage_km,
        fuel_type=listing.fuel_type,
        transmission=listing.transmission,
        body_type=listing.body_type,
        price_eur=_money(listing.price_eur),
        currency=listing.currency,
        vat_deductible=listing.vat_deductible,
        damaged=listing.damaged,
        service_history=listing.service_history,
        scraped_at=listing.scraped_at,
        created_at=listing.created_at,
    )


def _to_comparable_read(comparable: SwedishComparable) -> ComparableRead:
    return ComparableRead.model_validate(comparable)


def _to_settings_read(assumptions: CostAssumption) -> CostAssumptionRead:
    return CostAssumptionRead.model_validate(assumptions)


def _to_model_research_read(research: ModelResearch) -> ModelResearchRead:
    return ModelResearchRead.model_validate(research)


def _to_opportunity_read(deal: Deal) -> DealOpportunityRead:
    listing = deal.foreign_listing
    return DealOpportunityRead(
        id=deal.id,
        listing_id=listing.id,
        source=listing.source,
        listing_url=listing.listing_url,
        seller_country=listing.seller_country,
        seller_type=listing.seller_type,
        brand=listing.brand,
        model=listing.model,
        variant=listing.variant,
        trim=listing.trim,
        year=listing.year,
        mileage_km=listing.mileage_km,
        fuel_type=listing.fuel_type,
        transmission=listing.transmission,
        price_eur=_money(listing.price_eur),
        desired_minimum_profit_sek=_money(deal.desired_minimum_profit_sek),
        recommended_max_bid_eur=_money(deal.recommended_max_bid_eur),
        eur_to_sek_rate=_money(deal.eur_to_sek_rate),
        purchase_price_sek=_money(deal.purchase_price_sek),
        estimated_swedish_price_sek=_money(deal.estimated_swedish_price_sek),
        total_landed_cost_sek=_money(deal.total_landed_cost_sek),
        expected_profit_sek=_money(deal.expected_profit_sek),
        margin_percent=_money(deal.margin_percent),
        confidence_score=deal.confidence_score,
        risk_score=deal.risk_score,
        liquidity_score=deal.liquidity_score,
        deal_grade=deal.deal_grade,
        status=deal.status,
        reject_reason=deal.reject_reason,
        reject_notes=deal.reject_notes,
        risk_flags=deal.risk_flags,
        explanation=deal.explanation,
        confidence_explanation=_confidence_explanation(deal),
        actual_outcome=_actual_outcome(deal),
        created_at=deal.created_at,
    )


def _get_listing_or_404(db: Session, listing_id: int) -> CarListing:
    listing = db.get(CarListing, listing_id)
    if listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found",
        )
    return listing


def _get_deal_or_404(db: Session, deal_id: int) -> Deal:
    deal = db.scalars(
        select(Deal)
        .options(selectinload(Deal.foreign_listing))
        .where(Deal.id == deal_id)
    ).first()
    if deal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found",
        )
    return deal


def _get_cost_assumptions(db: Session) -> CostAssumption:
    assumptions = db.scalars(select(CostAssumption).limit(1)).first()
    if assumptions is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cost assumptions must be seeded before calculating deals",
        )
    return assumptions


def _comparable_count_for_listing(db: Session, listing: CarListing) -> int:
    return len(
        db.scalars(
            select(SwedishComparable.id).where(
                SwedishComparable.brand == listing.brand,
                SwedishComparable.model == listing.model,
            )
        ).all()
    )


def _average_listing_age_for_listing(db: Session, listing: CarListing) -> int:
    ages = db.scalars(
        select(SwedishComparable.listing_age_days).where(
            SwedishComparable.brand == listing.brand,
            SwedishComparable.model == listing.model,
        )
    ).all()
    known_ages = [age for age in ages if age is not None]
    if not known_ages:
        return 45
    return round(sum(known_ages) / len(known_ages))


def _model_liquidity_score(db: Session, listing: CarListing) -> int:
    research = db.scalars(
        select(ModelResearch).where(
            ModelResearch.brand == listing.brand,
            ModelResearch.model == listing.model,
        )
    ).first()
    return research.liquidity_score if research else 70


def list_listings(db: Session) -> list[ListingRead]:
    listings = db.scalars(select(CarListing).order_by(CarListing.id)).all()
    return [_to_listing_read(listing) for listing in listings]


def get_listing(db: Session, listing_id: int) -> ListingRead:
    return _to_listing_read(_get_listing_or_404(db, listing_id))


def create_listing(db: Session, payload: ListingCreate) -> ListingRead:
    source_listing_id = payload.source_listing_id or f"manual-{uuid4().hex[:12]}"
    existing = db.scalars(
        select(CarListing).where(
            CarListing.source == payload.source,
            CarListing.source_listing_id == source_listing_id,
        )
    ).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A listing with this source and source_listing_id already exists",
        )

    data = payload.model_dump()
    data["source_listing_id"] = source_listing_id
    listing = CarListing(**data, raw_data={"input_method": "manual"})
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return _to_listing_read(listing)


def update_listing(db: Session, listing_id: int, payload: ListingUpdate) -> ListingRead:
    listing = _get_listing_or_404(db, listing_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(listing, field, value)
    db.commit()
    db.refresh(listing)
    return _to_listing_read(listing)


def delete_listing(db: Session, listing_id: int) -> None:
    listing = _get_listing_or_404(db, listing_id)
    db.delete(listing)
    db.commit()


def list_comparables(db: Session) -> list[ComparableRead]:
    comparables = db.scalars(
        select(SwedishComparable).order_by(SwedishComparable.created_at.desc())
    ).all()
    return [_to_comparable_read(comparable) for comparable in comparables]


def create_comparable(db: Session, payload: ComparableCreate) -> ComparableRead:
    comparable = SwedishComparable(**payload.model_dump())
    db.add(comparable)
    db.commit()
    db.refresh(comparable)
    return _to_comparable_read(comparable)


def calculate_deal(db: Session, payload: DealCalculateRequest) -> DealOpportunityRead:
    listing = _get_listing_or_404(db, payload.listing_id)
    assumptions = _get_cost_assumptions(db)

    desired_profit_sek = _decimal(
        payload.desired_profit_sek,
        assumptions.minimum_profit_threshold_sek,
    )
    estimated_swedish_price_sek = Decimal(str(payload.estimated_swedish_price_sek))
    transport_cost_sek = _decimal(
        payload.transport_cost_sek,
        assumptions.default_transport_cost_sek,
    )
    registration_cost_sek = _decimal(
        payload.registration_cost_sek,
        assumptions.default_registration_cost_sek,
    )
    inspection_cost_sek = _decimal(
        payload.inspection_cost_sek,
        assumptions.default_inspection_cost_sek,
    )
    repair_buffer_sek = _decimal(
        payload.repair_buffer_sek,
        assumptions.default_repair_buffer_sek,
    )
    tax_cost_sek = _decimal(payload.tax_cost_sek, assumptions.default_tax_cost_sek)
    other_costs_sek = _decimal(
        payload.other_costs_sek,
        assumptions.default_other_costs_sek,
    )

    profit = calculate_profit(
        ProfitCalculationInput(
            purchase_price_eur=listing.price_eur,
            eur_to_sek_rate=assumptions.eur_to_sek_rate,
            estimated_swedish_price_sek=estimated_swedish_price_sek,
            transport_cost_sek=transport_cost_sek,
            registration_cost_sek=registration_cost_sek,
            inspection_cost_sek=inspection_cost_sek,
            repair_buffer_sek=repair_buffer_sek,
            tax_cost_sek=tax_cost_sek,
            other_costs_sek=other_costs_sek,
            desired_profit_sek=desired_profit_sek,
        )
    )

    scoring = score_deal(
        DealScoringInput(
            expected_profit_sek=float(profit.expected_profit_sek),
            comparable_count=_comparable_count_for_listing(db, listing),
            mileage_difference_km=12_000,
            year_difference=1,
            trim_matches=True,
            seller_type=listing.seller_type,
            has_service_history=bool(
                listing.service_history
                and "partial" not in listing.service_history.lower()
            ),
            damaged=listing.damaged,
            accident_history=bool(
                listing.accident_history
                and "minor" in listing.accident_history.lower()
            ),
            missing_data_points=0,
            average_listing_age_days=_average_listing_age_for_listing(db, listing),
            model_popularity_score=_model_liquidity_score(db, listing),
        )
    )

    deal = Deal(
        foreign_listing_id=listing.id,
        estimated_swedish_price_sek=estimated_swedish_price_sek,
        desired_minimum_profit_sek=desired_profit_sek,
        recommended_max_bid_eur=profit.recommended_max_bid_eur,
        eur_to_sek_rate=assumptions.eur_to_sek_rate,
        purchase_price_sek=profit.purchase_price_sek,
        transport_cost_sek=transport_cost_sek,
        registration_cost_sek=registration_cost_sek,
        inspection_cost_sek=inspection_cost_sek,
        repair_buffer_sek=repair_buffer_sek,
        tax_cost_sek=tax_cost_sek,
        other_costs_sek=other_costs_sek,
        total_landed_cost_sek=profit.total_landed_cost_sek,
        expected_profit_sek=profit.expected_profit_sek,
        margin_percent=profit.margin_percent,
        confidence_score=scoring.confidence_score,
        risk_score=scoring.risk_score,
        liquidity_score=scoring.liquidity_score,
        deal_grade=scoring.deal_grade,
        status="new",
        notes="Calculated from manual input.",
        explanation=scoring.explanation,
        confidence_explanation=scoring.confidence_explanation.model_dump(),
        risk_flags=scoring.risk_flags,
    )
    db.add(deal)
    db.commit()
    db.refresh(deal)
    deal = db.scalars(
        select(Deal)
        .options(selectinload(Deal.foreign_listing))
        .where(Deal.id == deal.id)
    ).one()
    return _to_opportunity_read(deal)


def _matching_comparables(db: Session, listing: CarListing) -> list[ComparableRead]:
    comparables = db.scalars(
        select(SwedishComparable)
        .where(
            SwedishComparable.brand == listing.brand,
            SwedishComparable.model == listing.model,
        )
        .order_by(SwedishComparable.price_sek.desc())
    ).all()
    return [_to_comparable_read(comparable) for comparable in comparables]


def get_deal_detail(db: Session, deal_id: int) -> DealDetailRead:
    deal = _get_deal_or_404(db, deal_id)
    listing = deal.foreign_listing
    return DealDetailRead(
        opportunity=_to_opportunity_read(deal),
        listing=_to_listing_read(listing),
        cost_breakdown=CostBreakdown(
            eur_to_sek_rate=_money(deal.eur_to_sek_rate),
            german_purchase_price_eur=_money(listing.price_eur),
            purchase_price_sek=_money(deal.purchase_price_sek),
            transport_cost_sek=_money(deal.transport_cost_sek),
            registration_cost_sek=_money(deal.registration_cost_sek),
            inspection_cost_sek=_money(deal.inspection_cost_sek),
            repair_buffer_sek=_money(deal.repair_buffer_sek),
            tax_cost_sek=_money(deal.tax_cost_sek),
            other_costs_sek=_money(deal.other_costs_sek),
            total_landed_cost_sek=_money(deal.total_landed_cost_sek),
            estimated_swedish_resale_price_sek=_money(deal.estimated_swedish_price_sek),
            expected_profit_sek=_money(deal.expected_profit_sek),
            desired_minimum_profit_sek=_money(deal.desired_minimum_profit_sek),
            recommended_max_bid_eur=_money(deal.recommended_max_bid_eur),
        ),
        comparables=_matching_comparables(db, listing),
        notes=deal.notes,
    )


def list_opportunities(
    db: Session,
    model: str | None = None,
    min_profit_sek: float | None = None,
    min_confidence: int | None = None,
    source: str | None = None,
    seller_type: str | None = None,
    fuel_type: str | None = None,
    transmission: str | None = None,
    status_filter: str | None = None,
) -> list[DealOpportunityRead]:
    query = select(Deal).join(Deal.foreign_listing).options(selectinload(Deal.foreign_listing))

    if model:
        query = query.where(CarListing.model.ilike(f"%{model}%"))
    if min_profit_sek is not None:
        query = query.where(Deal.expected_profit_sek >= Decimal(str(min_profit_sek)))
    if min_confidence is not None:
        query = query.where(Deal.confidence_score >= min_confidence)
    if source:
        query = query.where(CarListing.source == source)
    if seller_type:
        query = query.where(CarListing.seller_type == seller_type)
    if fuel_type:
        query = query.where(CarListing.fuel_type == fuel_type)
    if transmission:
        query = query.where(CarListing.transmission == transmission)
    if status_filter:
        query = query.where(Deal.status == status_filter)

    deals = db.scalars(
        query.order_by(Deal.expected_profit_sek.desc(), Deal.confidence_score.desc())
    ).all()
    return [_to_opportunity_read(deal) for deal in deals]


def update_deal_status(
    db: Session,
    deal_id: int,
    payload: DealStatusUpdate,
) -> DealOpportunityRead:
    status_value = payload.status.strip().lower()
    if status_value not in ALLOWED_DEAL_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Status must be one of: {', '.join(sorted(ALLOWED_DEAL_STATUSES))}",
        )

    deal = _get_deal_or_404(db, deal_id)
    deal.status = status_value
    if status_value == "rejected":
        if payload.reject_reason and payload.reject_reason not in REJECT_REASONS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Reject reason must be one of: {', '.join(sorted(REJECT_REASONS))}",
            )
        deal.reject_reason = payload.reject_reason or deal.reject_reason or "Other"
        deal.reject_notes = payload.reject_notes
    elif status_value != "rejected":
        deal.reject_reason = None
        deal.reject_notes = None
    db.commit()
    db.refresh(deal)
    deal = _get_deal_or_404(db, deal.id)
    return _to_opportunity_read(deal)


def update_actual_outcome(
    db: Session,
    deal_id: int,
    payload: ActualOutcomeUpdate,
) -> DealDetailRead:
    deal = _get_deal_or_404(db, deal_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        if value is not None and field != "lesson_learned":
            setattr(deal, field, Decimal(str(value)))
        else:
            setattr(deal, field, value)

    if (
        deal.actual_purchase_price_sek is not None
        and deal.actual_transport_cost_sek is not None
        and deal.actual_registration_cost_sek is not None
        and deal.actual_repair_cost_sek is not None
    ):
        actual = calculate_actual_outcome(
            ActualOutcomeInput(
                actual_purchase_price_sek=deal.actual_purchase_price_sek,
                actual_transport_cost_sek=deal.actual_transport_cost_sek,
                actual_registration_cost_sek=deal.actual_registration_cost_sek,
                actual_repair_cost_sek=deal.actual_repair_cost_sek,
                actual_sale_price_sek=deal.actual_sale_price_sek,
            )
        )
        deal.actual_total_cost_sek = actual.actual_total_cost_sek
        deal.actual_profit_sek = actual.actual_profit_sek

    db.commit()
    return get_deal_detail(db, deal.id)


def import_listings_csv(db: Session, csv_text: str) -> CsvImportResponse:
    reader = csv.DictReader(StringIO(csv_text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CSV header row is required")

    missing_columns = sorted(CSV_REQUIRED_COLUMNS - set(reader.fieldnames))
    if missing_columns:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Missing required columns: {', '.join(missing_columns)}",
        )

    listings: list[ListingRead] = []
    errors: list[str] = []
    for row_number, row in enumerate(reader, start=2):
        try:
            payload = ListingCreate(
                source=row["source"] or "csv",
                listing_url=row["listing_url"] or None,
                seller_country=row["seller_country"] or "DE",
                seller_type=row["seller_type"] or "dealer",
                brand=row["brand"],
                model=row["model"],
                trim=row["trim"] or None,
                year=int(row["year"]),
                mileage_km=int(row["mileage_km"]),
                price_eur=float(row["price_eur"]),
                fuel_type=row["fuel_type"] or None,
                transmission=row["transmission"] or None,
                description=row["notes"] or None,
            )
            listings.append(create_listing(db, payload))
        except Exception as exc:  # noqa: BLE001 - keep row-level import errors visible
            errors.append(f"Row {row_number}: {exc}")

    return CsvImportResponse(imported_count=len(listings), errors=errors, listings=listings)


def get_settings(db: Session) -> CostAssumptionRead:
    return _to_settings_read(_get_cost_assumptions(db))


def update_settings(
    db: Session,
    payload: CostAssumptionUpdate,
) -> CostAssumptionRead:
    assumptions = _get_cost_assumptions(db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(assumptions, field, Decimal(str(value)) if field != "minimum_confidence_score" else value)
    db.commit()
    db.refresh(assumptions)
    return _to_settings_read(assumptions)


def list_model_research(db: Session) -> list[ModelResearchRead]:
    rows = db.scalars(
        select(ModelResearch).order_by(ModelResearch.brand, ModelResearch.model)
    ).all()
    return [_to_model_research_read(row) for row in rows]


def update_model_research(
    db: Session,
    research_id: int,
    payload: ModelResearchUpdate,
) -> ModelResearchRead:
    research = db.get(ModelResearch, research_id)
    if research is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model research row not found",
        )

    decimal_fields = {
        "target_buy_price_min",
        "target_buy_price_max",
        "target_sell_price_min",
        "target_sell_price_max",
    }
    for field, value in payload.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(research, field, Decimal(str(value)) if field in decimal_fields else value)
    db.commit()
    db.refresh(research)
    return _to_model_research_read(research)


def get_dashboard_summary(db: Session) -> DashboardSummary:
    opportunities = list_opportunities(db)

    if not opportunities:
        return DashboardSummary(
            cars_scanned_today=0,
            active_opportunities=0,
            average_expected_profit_sek=0,
            best_model_this_week=None,
            high_confidence_deals=0,
            best_opportunity=None,
        )

    active_statuses = {"new", "researching", "contacted", "negotiating"}
    active_opportunities = [
        opportunity
        for opportunity in opportunities
        if opportunity.status.lower() in active_statuses
    ]
    model_counts = Counter(
        f"{opportunity.brand} {opportunity.model}" for opportunity in opportunities
    )
    best_opportunity = max(
        opportunities,
        key=lambda opportunity: opportunity.expected_profit_sek,
    )

    return DashboardSummary(
        cars_scanned_today=len(opportunities),
        active_opportunities=len(active_opportunities),
        average_expected_profit_sek=round(
            mean(opportunity.expected_profit_sek for opportunity in opportunities), 2
        ),
        best_model_this_week=model_counts.most_common(1)[0][0],
        high_confidence_deals=sum(
            1 for opportunity in opportunities if opportunity.confidence_score >= 75
        ),
        best_opportunity=best_opportunity,
    )
