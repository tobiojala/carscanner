from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func, text
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
    source: Mapped[str] = mapped_column(String(80), nullable=False, default="seed")
    source_listing_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    vin: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)

    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    make: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    trim: Mapped[str | None] = mapped_column(String(120), nullable=True)
    body_style: Mapped[str | None] = mapped_column(String(80), nullable=True)
    fuel_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    transmission: Mapped[str | None] = mapped_column(String(80), nullable=True)
    drivetrain: Mapped[str | None] = mapped_column(String(80), nullable=True)

    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    exterior_color: Mapped[str | None] = mapped_column(String(80), nullable=True)
    location_city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    location_country: Mapped[str] = mapped_column(String(2), nullable=False, default="US")
    source_market: Mapped[str] = mapped_column(String(80), nullable=False)
    target_market: Mapped[str] = mapped_column(String(80), nullable=False)

    asking_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    estimated_market_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    status: Mapped[str] = mapped_column(String(40), nullable=False, default="candidate", index=True)
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    last_seen_at: Mapped[datetime] = mapped_column(
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

    swedish_comparables: Mapped[list["SwedishComparable"]] = relationship(
        back_populates="car_listing",
        passive_deletes=True,
    )
    deals: Mapped[list["Deal"]] = relationship(
        back_populates="car_listing",
        cascade="all, delete-orphan",
    )
    alerts: Mapped[list["Alert"]] = relationship(
        back_populates="car_listing",
        passive_deletes=True,
    )


class SwedishComparable(TimestampMixin, Base):
    __tablename__ = "swedish_comparables"
    __table_args__ = (
        UniqueConstraint("source", "source_listing_id", name="uq_swedish_comparable_source_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    car_listing_id: Mapped[int | None] = mapped_column(
        ForeignKey("car_listings.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    source: Mapped[str] = mapped_column(String(80), nullable=False, default="seed")
    source_listing_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    make: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    trim: Mapped[str | None] = mapped_column(String(120), nullable=True)
    mileage_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    asking_price_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    location: Mapped[str | None] = mapped_column(String(160), nullable=True)
    dealer_name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    confidence_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    raw_data: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    car_listing: Mapped[CarListing | None] = relationship(back_populates="swedish_comparables")
    deals: Mapped[list["Deal"]] = relationship(
        back_populates="swedish_comparable",
        passive_deletes=True,
    )


class Deal(TimestampMixin, Base):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True)
    car_listing_id: Mapped[int] = mapped_column(
        ForeignKey("car_listings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    swedish_comparable_id: Mapped[int | None] = mapped_column(
        ForeignKey("swedish_comparables.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="watching", index=True)

    acquisition_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    acquisition_currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    estimated_sale_price_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    estimated_total_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    estimated_profit_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    margin_percent: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)

    transport_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    import_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    inspection_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    repair_budget_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    platform_fee_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    car_listing: Mapped[CarListing] = relationship(back_populates="deals")
    swedish_comparable: Mapped[SwedishComparable | None] = relationship(back_populates="deals")
    alerts: Mapped[list["Alert"]] = relationship(
        back_populates="deal",
        passive_deletes=True,
    )


class ModelResearch(TimestampMixin, Base):
    __tablename__ = "model_research"
    __table_args__ = (
        UniqueConstraint(
            "make",
            "model",
            "trim",
            "model_year_start",
            "model_year_end",
            "market",
            name="uq_model_research_vehicle_market",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    make: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    trim: Mapped[str | None] = mapped_column(String(120), nullable=True)
    model_year_start: Mapped[int | None] = mapped_column(Integer, nullable=True)
    model_year_end: Mapped[int | None] = mapped_column(Integer, nullable=True)
    market: Mapped[str] = mapped_column(String(80), nullable=False, default="SE", index=True)

    average_price_sek: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    median_price_sek: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    demand_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    liquidity_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    search_terms: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    common_issues: Mapped[str | None] = mapped_column(Text, nullable=True)


class CostAssumption(TimestampMixin, Base):
    __tablename__ = "cost_assumptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    origin_market: Mapped[str] = mapped_column(String(80), nullable=False)
    destination_market: Mapped[str] = mapped_column(String(80), nullable=False, default="SE")
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="SEK")

    exchange_rate_to_sek: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    transport_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    import_duty_rate: Mapped[Decimal] = mapped_column(Numeric(6, 4), nullable=False, default=0)
    vat_rate: Mapped[Decimal] = mapped_column(Numeric(6, 4), nullable=False, default=0)
    registration_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    inspection_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    platform_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    repair_buffer_percent: Mapped[Decimal] = mapped_column(Numeric(6, 4), nullable=False, default=0)

    is_active: Mapped[bool] = mapped_column(nullable=False, default=True, index=True)
    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class Alert(TimestampMixin, Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    car_listing_id: Mapped[int | None] = mapped_column(
        ForeignKey("car_listings.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    deal_id: Mapped[int | None] = mapped_column(
        ForeignKey("deals.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    alert_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(40), nullable=False, default="info", index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(nullable=False, default=False, index=True)
    triggered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    car_listing: Mapped[CarListing | None] = relationship(back_populates="alerts")
    deal: Mapped[Deal | None] = relationship(back_populates="alerts")
