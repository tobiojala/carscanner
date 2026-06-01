from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class CarListing(TimestampMixin, Base):
    __tablename__ = "car_listings"
    __table_args__ = (
        UniqueConstraint("source", "source_listing_id", name="uq_car_listing_source_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    source_listing_id: Mapped[str] = mapped_column(String(120), nullable=False)
    listing_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    seller_country: Mapped[str] = mapped_column(String(2), nullable=False, default="DE", index=True)
    seller_type: Mapped[str] = mapped_column(String(40), nullable=False, default="dealer", index=True)

    brand: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    variant: Mapped[str | None] = mapped_column(String(120), nullable=True)
    trim: Mapped[str | None] = mapped_column(String(120), nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    first_registration_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    mileage_km: Mapped[int] = mapped_column(Integer, nullable=False)
    fuel_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    transmission: Mapped[str | None] = mapped_column(String(80), nullable=True)
    drivetrain: Mapped[str | None] = mapped_column(String(80), nullable=True)
    body_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    color: Mapped[str | None] = mapped_column(String(80), nullable=True)

    price_eur: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="EUR")
    vat_deductible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    damaged: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    accident_history: Mapped[str | None] = mapped_column(Text, nullable=True)
    service_history: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_urls: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )
    scraped_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    raw_data: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    deals: Mapped[list["Deal"]] = relationship(
        back_populates="foreign_listing",
        cascade="all, delete-orphan",
    )


class SwedishComparable(Base):
    __tablename__ = "swedish_comparables"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    listing_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    brand: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    variant: Mapped[str | None] = mapped_column(String(120), nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    mileage_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fuel_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    transmission: Mapped[str | None] = mapped_column(String(80), nullable=True)
    trim: Mapped[str | None] = mapped_column(String(120), nullable=True)
    price_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    location: Mapped[str | None] = mapped_column(String(160), nullable=True)
    seller_type: Mapped[str | None] = mapped_column(String(40), nullable=True)
    listing_age_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class Deal(TimestampMixin, Base):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True)
    foreign_listing_id: Mapped[int] = mapped_column(
        ForeignKey("car_listings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    estimated_swedish_price_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    desired_minimum_profit_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    recommended_max_bid_eur: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    eur_to_sek_rate: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False, default=0)
    purchase_price_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    transport_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    registration_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    inspection_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    repair_buffer_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    tax_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    other_costs_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_landed_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    expected_profit_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, index=True)
    margin_percent: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    confidence_score: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    liquidity_score: Mapped[int] = mapped_column(Integer, nullable=False)
    deal_grade: Mapped[str] = mapped_column(String(4), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="new", index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence_explanation: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )
    reject_reason: Mapped[str | None] = mapped_column(String(120), nullable=True)
    reject_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    actual_purchase_price_sek: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    actual_transport_cost_sek: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    actual_registration_cost_sek: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    actual_repair_cost_sek: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    actual_total_cost_sek: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    actual_sale_price_sek: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    actual_profit_sek: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    days_to_sell: Mapped[int | None] = mapped_column(Integer, nullable=True)
    lesson_learned: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_flags: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )

    foreign_listing: Mapped[CarListing] = relationship(back_populates="deals")
    alerts: Mapped[list["Alert"]] = relationship(
        back_populates="deal",
        cascade="all, delete-orphan",
    )


class ModelResearch(TimestampMixin, Base):
    __tablename__ = "model_research"
    __table_args__ = (
        UniqueConstraint("brand", "model", "variant", name="uq_model_research_vehicle"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    variant: Mapped[str | None] = mapped_column(String(120), nullable=True)
    good_years: Mapped[str | None] = mapped_column(String(120), nullable=True)
    strong_trims: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )
    weak_trims: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
        server_default=text("'[]'::jsonb"),
    )
    common_issues: Mapped[str | None] = mapped_column(Text, nullable=True)
    swedish_demand_score: Mapped[int] = mapped_column(Integer, nullable=False)
    german_supply_score: Mapped[int] = mapped_column(Integer, nullable=False)
    liquidity_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_buy_price_min: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    target_buy_price_max: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    target_sell_price_min: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    target_sell_price_max: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)


class CostAssumption(Base):
    __tablename__ = "cost_assumptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    eur_to_sek_rate: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    default_transport_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    default_registration_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    default_inspection_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    default_repair_buffer_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    default_tax_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    default_other_costs_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    minimum_profit_threshold_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    minimum_confidence_score: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    deal_id: Mapped[int | None] = mapped_column(
        ForeignKey("deals.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    alert_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    sent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    deal: Mapped[Deal | None] = relationship(back_populates="alerts")
