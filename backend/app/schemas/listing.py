from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ListingRead(BaseModel):
    id: int
    year: int
    make: str
    model: str
    trim: str | None
    source_market: str
    target_market: str
    asking_price: float
    estimated_market_price: float
    mileage: int
    estimated_spread: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardSummary(BaseModel):
    total_listings: int
    average_spread: float
    best_spread: float
    best_listing: ListingRead | None
