"""create car arbitrage schema

Revision ID: 202605310920
Revises:
Create Date: 2026-05-31 09:20:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "202605310920"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "car_listings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=80), nullable=False),
        sa.Column("source_listing_id", sa.String(length=120), nullable=True),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("vin", sa.String(length=32), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("make", sa.String(length=80), nullable=False),
        sa.Column("model", sa.String(length=120), nullable=False),
        sa.Column("trim", sa.String(length=120), nullable=True),
        sa.Column("body_style", sa.String(length=80), nullable=True),
        sa.Column("fuel_type", sa.String(length=80), nullable=True),
        sa.Column("transmission", sa.String(length=80), nullable=True),
        sa.Column("drivetrain", sa.String(length=80), nullable=True),
        sa.Column("mileage", sa.Integer(), nullable=False),
        sa.Column("exterior_color", sa.String(length=80), nullable=True),
        sa.Column("location_city", sa.String(length=120), nullable=True),
        sa.Column("location_country", sa.String(length=2), nullable=False),
        sa.Column("source_market", sa.String(length=80), nullable=False),
        sa.Column("target_market", sa.String(length=80), nullable=False),
        sa.Column("asking_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("estimated_market_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("raw_data", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source", "source_listing_id", name="uq_car_listing_source_id"),
    )
    op.create_index(op.f("ix_car_listings_id"), "car_listings", ["id"], unique=False)
    op.create_index(op.f("ix_car_listings_make"), "car_listings", ["make"], unique=False)
    op.create_index(op.f("ix_car_listings_model"), "car_listings", ["model"], unique=False)
    op.create_index(op.f("ix_car_listings_status"), "car_listings", ["status"], unique=False)
    op.create_index(op.f("ix_car_listings_vin"), "car_listings", ["vin"], unique=False)
    op.create_index(op.f("ix_car_listings_year"), "car_listings", ["year"], unique=False)

    op.create_table(
        "cost_assumptions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("origin_market", sa.String(length=80), nullable=False),
        sa.Column("destination_market", sa.String(length=80), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("exchange_rate_to_sek", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("transport_cost", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("import_duty_rate", sa.Numeric(precision=6, scale=4), nullable=False),
        sa.Column("vat_rate", sa.Numeric(precision=6, scale=4), nullable=False),
        sa.Column("registration_cost", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("inspection_cost", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("platform_fee", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("repair_buffer_percent", sa.Numeric(precision=6, scale=4), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("effective_from", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_cost_assumptions_is_active"), "cost_assumptions", ["is_active"], unique=False)

    op.create_table(
        "model_research",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("make", sa.String(length=80), nullable=False),
        sa.Column("model", sa.String(length=120), nullable=False),
        sa.Column("trim", sa.String(length=120), nullable=True),
        sa.Column("model_year_start", sa.Integer(), nullable=True),
        sa.Column("model_year_end", sa.Integer(), nullable=True),
        sa.Column("market", sa.String(length=80), nullable=False),
        sa.Column("average_price_sek", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("median_price_sek", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("sample_size", sa.Integer(), nullable=False),
        sa.Column("demand_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("liquidity_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("search_terms", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("common_issues", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("make", "model", "trim", "model_year_start", "model_year_end", "market", name="uq_model_research_vehicle_market"),
    )
    op.create_index(op.f("ix_model_research_make"), "model_research", ["make"], unique=False)
    op.create_index(op.f("ix_model_research_market"), "model_research", ["market"], unique=False)
    op.create_index(op.f("ix_model_research_model"), "model_research", ["model"], unique=False)

    op.create_table(
        "swedish_comparables",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("car_listing_id", sa.Integer(), nullable=True),
        sa.Column("source", sa.String(length=80), nullable=False),
        sa.Column("source_listing_id", sa.String(length=120), nullable=True),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("make", sa.String(length=80), nullable=False),
        sa.Column("model", sa.String(length=120), nullable=False),
        sa.Column("trim", sa.String(length=120), nullable=True),
        sa.Column("mileage_km", sa.Integer(), nullable=True),
        sa.Column("asking_price_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("location", sa.String(length=160), nullable=True),
        sa.Column("dealer_name", sa.String(length=160), nullable=True),
        sa.Column("observed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("confidence_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("raw_data", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["car_listing_id"], ["car_listings.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source", "source_listing_id", name="uq_swedish_comparable_source_id"),
    )
    op.create_index(op.f("ix_swedish_comparables_car_listing_id"), "swedish_comparables", ["car_listing_id"], unique=False)
    op.create_index(op.f("ix_swedish_comparables_make"), "swedish_comparables", ["make"], unique=False)
    op.create_index(op.f("ix_swedish_comparables_model"), "swedish_comparables", ["model"], unique=False)
    op.create_index(op.f("ix_swedish_comparables_year"), "swedish_comparables", ["year"], unique=False)

    op.create_table(
        "deals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("car_listing_id", sa.Integer(), nullable=False),
        sa.Column("swedish_comparable_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("acquisition_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("acquisition_currency", sa.String(length=3), nullable=False),
        sa.Column("estimated_sale_price_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("estimated_total_cost_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("estimated_profit_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("margin_percent", sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column("transport_cost_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("import_cost_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("inspection_cost_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("repair_budget_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("platform_fee_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["car_listing_id"], ["car_listings.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["swedish_comparable_id"], ["swedish_comparables.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_deals_car_listing_id"), "deals", ["car_listing_id"], unique=False)
    op.create_index(op.f("ix_deals_status"), "deals", ["status"], unique=False)
    op.create_index(op.f("ix_deals_swedish_comparable_id"), "deals", ["swedish_comparable_id"], unique=False)

    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("car_listing_id", sa.Integer(), nullable=True),
        sa.Column("deal_id", sa.Integer(), nullable=True),
        sa.Column("alert_type", sa.String(length=80), nullable=False),
        sa.Column("severity", sa.String(length=40), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False),
        sa.Column("triggered_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["car_listing_id"], ["car_listings.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["deal_id"], ["deals.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_alerts_alert_type"), "alerts", ["alert_type"], unique=False)
    op.create_index(op.f("ix_alerts_car_listing_id"), "alerts", ["car_listing_id"], unique=False)
    op.create_index(op.f("ix_alerts_deal_id"), "alerts", ["deal_id"], unique=False)
    op.create_index(op.f("ix_alerts_is_read"), "alerts", ["is_read"], unique=False)
    op.create_index(op.f("ix_alerts_severity"), "alerts", ["severity"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_alerts_severity"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_is_read"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_deal_id"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_car_listing_id"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_alert_type"), table_name="alerts")
    op.drop_table("alerts")

    op.drop_index(op.f("ix_deals_swedish_comparable_id"), table_name="deals")
    op.drop_index(op.f("ix_deals_status"), table_name="deals")
    op.drop_index(op.f("ix_deals_car_listing_id"), table_name="deals")
    op.drop_table("deals")

    op.drop_index(op.f("ix_swedish_comparables_year"), table_name="swedish_comparables")
    op.drop_index(op.f("ix_swedish_comparables_model"), table_name="swedish_comparables")
    op.drop_index(op.f("ix_swedish_comparables_make"), table_name="swedish_comparables")
    op.drop_index(op.f("ix_swedish_comparables_car_listing_id"), table_name="swedish_comparables")
    op.drop_table("swedish_comparables")

    op.drop_index(op.f("ix_model_research_model"), table_name="model_research")
    op.drop_index(op.f("ix_model_research_market"), table_name="model_research")
    op.drop_index(op.f("ix_model_research_make"), table_name="model_research")
    op.drop_table("model_research")

    op.drop_index(op.f("ix_cost_assumptions_is_active"), table_name="cost_assumptions")
    op.drop_table("cost_assumptions")

    op.drop_index(op.f("ix_car_listings_year"), table_name="car_listings")
    op.drop_index(op.f("ix_car_listings_vin"), table_name="car_listings")
    op.drop_index(op.f("ix_car_listings_status"), table_name="car_listings")
    op.drop_index(op.f("ix_car_listings_model"), table_name="car_listings")
    op.drop_index(op.f("ix_car_listings_make"), table_name="car_listings")
    op.drop_index(op.f("ix_car_listings_id"), table_name="car_listings")
    op.drop_table("car_listings")
