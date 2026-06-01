from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ListingBase(BaseModel):
    source: str = "manual"
    source_listing_id: str | None = None
    listing_url: str | None = None
    seller_country: str = "DE"
    seller_type: str = "dealer"
    brand: str
    model: str
    variant: str | None = None
    trim: str | None = None
    year: int = Field(ge=1900, le=2100)
    mileage_km: int = Field(ge=0)
    fuel_type: str | None = None
    transmission: str | None = None
    drivetrain: str | None = None
    body_type: str | None = None
    color: str | None = None
    price_eur: float = Field(gt=0)
    currency: str = "EUR"
    vat_deductible: bool = False
    damaged: bool = False
    accident_history: str | None = None
    service_history: str | None = None
    description: str | None = None
    image_urls: list[str] = Field(default_factory=list)


class ListingCreate(ListingBase):
    pass


class ListingUpdate(BaseModel):
    listing_url: str | None = None
    seller_type: str | None = None
    variant: str | None = None
    trim: str | None = None
    mileage_km: int | None = Field(default=None, ge=0)
    fuel_type: str | None = None
    transmission: str | None = None
    drivetrain: str | None = None
    body_type: str | None = None
    color: str | None = None
    price_eur: float | None = Field(default=None, gt=0)
    vat_deductible: bool | None = None
    damaged: bool | None = None
    accident_history: str | None = None
    service_history: str | None = None
    description: str | None = None
    image_urls: list[str] | None = None


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


class ComparableCreate(BaseModel):
    source: str = "manual"
    listing_url: str | None = None
    brand: str
    model: str
    variant: str | None = None
    year: int = Field(ge=1900, le=2100)
    mileage_km: int | None = Field(default=None, ge=0)
    fuel_type: str | None = None
    transmission: str | None = None
    trim: str | None = None
    price_sek: float = Field(gt=0)
    location: str | None = None
    seller_type: str | None = None
    listing_age_days: int | None = Field(default=None, ge=0)


class ComparableRead(ComparableCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CsvImportResponse(BaseModel):
    imported_count: int
    errors: list[str]
    listings: list[ListingRead]


class DealCalculateRequest(BaseModel):
    listing_id: int
    estimated_swedish_price_sek: float = Field(gt=0)
    desired_profit_sek: float | None = Field(default=None, ge=0)
    transport_cost_sek: float | None = Field(default=None, ge=0)
    registration_cost_sek: float | None = Field(default=None, ge=0)
    inspection_cost_sek: float | None = Field(default=None, ge=0)
    repair_buffer_sek: float | None = Field(default=None, ge=0)
    tax_cost_sek: float | None = Field(default=None, ge=0)
    other_costs_sek: float | None = Field(default=None, ge=0)


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
    desired_minimum_profit_sek: float
    recommended_max_bid_eur: float
    eur_to_sek_rate: float
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
    reject_reason: str | None
    reject_notes: str | None
    risk_flags: list[str]
    explanation: str | None
    confidence_explanation: ConfidenceExplanationRead
    actual_outcome: ActualOutcomeRead
    created_at: datetime


class CostBreakdown(BaseModel):
    eur_to_sek_rate: float
    german_purchase_price_eur: float
    purchase_price_sek: float
    transport_cost_sek: float
    registration_cost_sek: float
    inspection_cost_sek: float
    repair_buffer_sek: float
    tax_cost_sek: float
    other_costs_sek: float
    total_landed_cost_sek: float
    estimated_swedish_resale_price_sek: float
    expected_profit_sek: float
    desired_minimum_profit_sek: float
    recommended_max_bid_eur: float


class DealDetailRead(BaseModel):
    opportunity: DealOpportunityRead
    listing: ListingRead
    cost_breakdown: CostBreakdown
    comparables: list[ComparableRead]
    notes: str | None


class DealStatusUpdate(BaseModel):
    status: str
    reject_reason: str | None = None
    reject_notes: str | None = None


class ActualOutcomeUpdate(BaseModel):
    actual_purchase_price_sek: float | None = Field(default=None, ge=0)
    actual_transport_cost_sek: float | None = Field(default=None, ge=0)
    actual_registration_cost_sek: float | None = Field(default=None, ge=0)
    actual_repair_cost_sek: float | None = Field(default=None, ge=0)
    actual_total_cost_sek: float | None = Field(default=None, ge=0)
    actual_sale_price_sek: float | None = Field(default=None, ge=0)
    days_to_sell: int | None = Field(default=None, ge=0)
    lesson_learned: str | None = None


class ActualOutcomeRead(ActualOutcomeUpdate):
    actual_profit_sek: float | None = None


class ConfidenceExplanationRead(BaseModel):
    score: int
    positive_factors: list[str]
    negative_factors: list[str]
    missing_data: list[str]
    comparable_count: int
    summary: str


class CostAssumptionRead(BaseModel):
    id: int
    eur_to_sek_rate: float
    default_transport_cost_sek: float
    default_registration_cost_sek: float
    default_inspection_cost_sek: float
    default_repair_buffer_sek: float
    default_tax_cost_sek: float
    default_other_costs_sek: float
    minimum_profit_threshold_sek: float
    minimum_confidence_score: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CostAssumptionUpdate(BaseModel):
    eur_to_sek_rate: float | None = Field(default=None, gt=0)
    default_transport_cost_sek: float | None = Field(default=None, ge=0)
    default_registration_cost_sek: float | None = Field(default=None, ge=0)
    default_inspection_cost_sek: float | None = Field(default=None, ge=0)
    default_repair_buffer_sek: float | None = Field(default=None, ge=0)
    default_tax_cost_sek: float | None = Field(default=None, ge=0)
    default_other_costs_sek: float | None = Field(default=None, ge=0)
    minimum_profit_threshold_sek: float | None = Field(default=None, ge=0)
    minimum_confidence_score: int | None = Field(default=None, ge=0, le=100)


class ModelResearchRead(BaseModel):
    id: int
    brand: str
    model: str
    variant: str | None
    good_years: str | None
    strong_trims: list[str]
    weak_trims: list[str]
    common_issues: str | None
    swedish_demand_score: int
    german_supply_score: int
    liquidity_score: int
    risk_notes: str | None
    target_buy_price_min: float | None
    target_buy_price_max: float | None
    target_sell_price_min: float | None
    target_sell_price_max: float | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ModelResearchUpdate(BaseModel):
    good_years: str | None = None
    strong_trims: list[str] | None = None
    weak_trims: list[str] | None = None
    common_issues: str | None = None
    swedish_demand_score: int | None = Field(default=None, ge=0, le=100)
    german_supply_score: int | None = Field(default=None, ge=0, le=100)
    liquidity_score: int | None = Field(default=None, ge=0, le=100)
    risk_notes: str | None = None
    target_buy_price_min: float | None = Field(default=None, ge=0)
    target_buy_price_max: float | None = Field(default=None, ge=0)
    target_sell_price_min: float | None = Field(default=None, ge=0)
    target_sell_price_max: float | None = Field(default=None, ge=0)


class DashboardSummary(BaseModel):
    cars_scanned_today: int
    active_opportunities: int
    average_expected_profit_sek: float
    best_model_this_week: str | None
    high_confidence_deals: int
    best_opportunity: DealOpportunityRead | None
