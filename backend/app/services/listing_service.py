from collections import Counter
from statistics import mean

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import CarListing, Deal
from app.schemas import DashboardSummary, DealOpportunityRead, ListingRead


def _money(value: object) -> float:
    return float(value or 0)


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
        risk_flags=deal.risk_flags,
        explanation=deal.explanation,
        created_at=deal.created_at,
    )


def list_listings(db: Session) -> list[ListingRead]:
    listings = db.scalars(select(CarListing).order_by(CarListing.id)).all()
    return [_to_listing_read(listing) for listing in listings]


def list_opportunities(db: Session) -> list[DealOpportunityRead]:
    deals = db.scalars(
        select(Deal)
        .options(selectinload(Deal.foreign_listing))
        .order_by(Deal.expected_profit_sek.desc(), Deal.confidence_score.desc())
    ).all()
    return [_to_opportunity_read(deal) for deal in deals]


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
