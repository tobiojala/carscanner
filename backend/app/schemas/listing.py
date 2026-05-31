from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ListingRead(BaseModel):
    id: int
    source: str
    source_listing_id: str
    listing_url: str | None
    seller_country: str
    seller_type: str
    brand: str
    model: str
    variant: str | None
    trim: str | None
    year: int
    mileage_km: int
    fuel_type: str | None
    transmission: str | None
    body_type: str | None
    price_eur: float
    currency: str
    vat_deductible: bool
    damaged: bool
    service_history: str | None
    scraped_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DealOpportunityRead(BaseModel):
    id: int
    listing_id: int
    source: str
    listing_url: str | None
    seller_country: str
    seller_type: str
    brand: str
    model: str
    variant: str | None
    trim: str | None
    year: int
    mileage_km: int
    fuel_type: str | None
    transmission: str | None
    price_eur: float
    purchase_price_sek: float
    estimated_swedish_price_sek: float
    total_landed_cost_sek: float
    expected_profit_sek: float
    margin_percent: float
    confidence_score: int
    risk_score: int
    liquidity_score: int
    deal_grade: str
    status: str
    risk_flags: list[str]
    explanation: str | None
    created_at: datetime


class DashboardSummary(BaseModel):
    cars_scanned_today: int
    active_opportunities: int
    average_expected_profit_sek: float
    best_model_this_week: str | None
    high_confidence_deals: int
    best_opportunity: DealOpportunityRead | None
