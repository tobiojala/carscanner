from statistics import mean

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CarListing
from app.schemas import DashboardSummary, ListingRead


def _to_listing_read(listing: CarListing) -> ListingRead:
    asking_price = float(listing.asking_price)
    estimated_market_price = float(listing.estimated_market_price)

    return ListingRead(
        id=listing.id,
        year=listing.year,
        make=listing.make,
        model=listing.model,
        trim=listing.trim,
        source_market=listing.source_market,
        target_market=listing.target_market,
        asking_price=asking_price,
        estimated_market_price=estimated_market_price,
        mileage=listing.mileage,
        estimated_spread=estimated_market_price - asking_price,
        created_at=listing.created_at,
    )


def list_opportunities(db: Session) -> list[ListingRead]:
    listings = db.scalars(select(CarListing).order_by(CarListing.id)).all()
    return [_to_listing_read(listing) for listing in listings]


def get_dashboard_summary(db: Session) -> DashboardSummary:
    opportunities = list_opportunities(db)

    if not opportunities:
        return DashboardSummary(
            total_listings=0,
            average_spread=0,
            best_spread=0,
            best_listing=None,
        )

    best_listing = max(opportunities, key=lambda listing: listing.estimated_spread)
    spreads = [listing.estimated_spread for listing in opportunities]

    return DashboardSummary(
        total_listings=len(opportunities),
        average_spread=round(mean(spreads), 2),
        best_spread=round(best_listing.estimated_spread, 2),
        best_listing=best_listing,
    )
