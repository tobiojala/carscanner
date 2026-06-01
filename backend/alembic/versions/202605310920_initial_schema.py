"""create prompt pack car arbitrage schema

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
        sa.Column("source_listing_id", sa.String(length=120), nullable=False),
        sa.Column("listing_url", sa.Text(), nullable=True),
        sa.Column("seller_country", sa.String(length=2), nullable=False),
        sa.Column("seller_type", sa.String(length=40), nullable=False),
        sa.Column("brand", sa.String(length=80), nullable=False),
        sa.Column("model", sa.String(length=120), nullable=False),
        sa.Column("variant", sa.String(length=120), nullable=True),
        sa.Column("trim", sa.String(length=120), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("first_registration_date", sa.Date(), nullable=True),
        sa.Column("mileage_km", sa.Integer(), nullable=False),
        sa.Column("fuel_type", sa.String(length=80), nullable=True),
        sa.Column("transmission", sa.String(length=80), nullable=True),
        sa.Column("drivetrain", sa.String(length=80), nullable=True),
        sa.Column("body_type", sa.String(length=80), nullable=True),
        sa.Column("color", sa.String(length=80), nullable=True),
        sa.Column("price_eur", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("vat_deductible", sa.Boolean(), nullable=False),
        sa.Column("damaged", sa.Boolean(), nullable=False),
        sa.Column("accident_history", sa.Text(), nullable=True),
        sa.Column("service_history", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_urls", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.Column("scraped_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("raw_data", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source", "source_listing_id", name="uq_car_listing_source_id"),
    )
    op.create_index(op.f("ix_car_listings_brand"), "car_listings", ["brand"], unique=False)
    op.create_index(op.f("ix_car_listings_damaged"), "car_listings", ["damaged"], unique=False)
    op.create_index(op.f("ix_car_listings_id"), "car_listings", ["id"], unique=False)
    op.create_index(op.f("ix_car_listings_model"), "car_listings", ["model"], unique=False)
    op.create_index(op.f("ix_car_listings_seller_country"), "car_listings", ["seller_country"], unique=False)
    op.create_index(op.f("ix_car_listings_seller_type"), "car_listings", ["seller_type"], unique=False)
    op.create_index(op.f("ix_car_listings_source"), "car_listings", ["source"], unique=False)
    op.create_index(op.f("ix_car_listings_year"), "car_listings", ["year"], unique=False)

    op.create_table(
        "cost_assumptions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("eur_to_sek_rate", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("default_transport_cost_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("default_registration_cost_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("default_inspection_cost_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("default_repair_buffer_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("default_tax_cost_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("default_other_costs_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("minimum_profit_threshold_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("minimum_confidence_score", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "model_research",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("brand", sa.String(length=80), nullable=False),
        sa.Column("model", sa.String(length=120), nullable=False),
        sa.Column("variant", sa.String(length=120), nullable=True),
        sa.Column("good_years", sa.String(length=120), nullable=True),
        sa.Column("strong_trims", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.Column("weak_trims", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.Column("common_issues", sa.Text(), nullable=True),
        sa.Column("swedish_demand_score", sa.Integer(), nullable=False),
        sa.Column("german_supply_score", sa.Integer(), nullable=False),
        sa.Column("liquidity_score", sa.Integer(), nullable=False),
        sa.Column("risk_notes", sa.Text(), nullable=True),
        sa.Column("target_buy_price_min", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("target_buy_price_max", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("target_sell_price_min", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("target_sell_price_max", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("brand", "model", "variant", name="uq_model_research_vehicle"),
    )
    op.create_index(op.f("ix_model_research_brand"), "model_research", ["brand"], unique=False)
    op.create_index(op.f("ix_model_research_model"), "model_research", ["model"], unique=False)

    op.create_table(
        "swedish_comparables",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=80), nullable=False),
        sa.Column("listing_url", sa.Text(), nullable=True),
        sa.Column("brand", sa.String(length=80), nullable=False),
        sa.Column("model", sa.String(length=120), nullable=False),
        sa.Column("variant", sa.String(length=120), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("mileage_km", sa.Integer(), nullable=True),
        sa.Column("fuel_type", sa.String(length=80), nullable=True),
        sa.Column("transmission", sa.String(length=80), nullable=True),
        sa.Column("trim", sa.String(length=120), nullable=True),
        sa.Column("price_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("location", sa.String(length=160), nullable=True),
        sa.Column("seller_type", sa.String(length=40), nullable=True),
        sa.Column("listing_age_days", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_swedish_comparables_brand"), "swedish_comparables", ["brand"], unique=False)
    op.create_index(op.f("ix_swedish_comparables_model"), "swedish_comparables", ["model"], unique=False)
    op.create_index(op.f("ix_swedish_comparables_source"), "swedish_comparables", ["source"], unique=False)
    op.create_index(op.f("ix_swedish_comparables_year"), "swedish_comparables", ["year"], unique=False)

    op.create_table(
        "deals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("foreign_listing_id", sa.Integer(), nullable=False),
        sa.Column("estimated_swedish_price_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("purchase_price_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("transport_cost_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("registration_cost_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("inspection_cost_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("repair_buffer_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("tax_cost_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("other_costs_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("total_landed_cost_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("expected_profit_sek", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("margin_percent", sa.Numeric(precision=6, scale=2), nullable=False),
        sa.Column("confidence_score", sa.Integer(), nullable=False),
        sa.Column("risk_score", sa.Integer(), nullable=False),
        sa.Column("liquidity_score", sa.Integer(), nullable=False),
        sa.Column("deal_grade", sa.String(length=4), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("risk_flags", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["foreign_listing_id"], ["car_listings.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_deals_confidence_score"), "deals", ["confidence_score"], unique=False)
    op.create_index(op.f("ix_deals_deal_grade"), "deals", ["deal_grade"], unique=False)
    op.create_index(op.f("ix_deals_expected_profit_sek"), "deals", ["expected_profit_sek"], unique=False)
    op.create_index(op.f("ix_deals_foreign_listing_id"), "deals", ["foreign_listing_id"], unique=False)
    op.create_index(op.f("ix_deals_risk_score"), "deals", ["risk_score"], unique=False)
    op.create_index(op.f("ix_deals_status"), "deals", ["status"], unique=False)

    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("deal_id", sa.Integer(), nullable=True),
        sa.Column("alert_type", sa.String(length=80), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("sent", sa.Boolean(), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["deal_id"], ["deals.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_alerts_alert_type"), "alerts", ["alert_type"], unique=False)
    op.create_index(op.f("ix_alerts_deal_id"), "alerts", ["deal_id"], unique=False)
    op.create_index(op.f("ix_alerts_sent"), "alerts", ["sent"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_alerts_sent"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_deal_id"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_alert_type"), table_name="alerts")
    op.drop_table("alerts")

    op.drop_index(op.f("ix_deals_status"), table_name="deals")
    op.drop_index(op.f("ix_deals_risk_score"), table_name="deals")
    op.drop_index(op.f("ix_deals_foreign_listing_id"), table_name="deals")
    op.drop_index(op.f("ix_deals_expected_profit_sek"), table_name="deals")
    op.drop_index(op.f("ix_deals_deal_grade"), table_name="deals")
    op.drop_index(op.f("ix_deals_confidence_score"), table_name="deals")
    op.drop_table("deals")

    op.drop_index(op.f("ix_swedish_comparables_year"), table_name="swedish_comparables")
    op.drop_index(op.f("ix_swedish_comparables_source"), table_name="swedish_comparables")
    op.drop_index(op.f("ix_swedish_comparables_model"), table_name="swedish_comparables")
    op.drop_index(op.f("ix_swedish_comparables_brand"), table_name="swedish_comparables")
    op.drop_table("swedish_comparables")

    op.drop_index(op.f("ix_model_research_model"), table_name="model_research")
    op.drop_index(op.f("ix_model_research_brand"), table_name="model_research")
    op.drop_table("model_research")

    op.drop_table("cost_assumptions")

    op.drop_index(op.f("ix_car_listings_year"), table_name="car_listings")
    op.drop_index(op.f("ix_car_listings_source"), table_name="car_listings")
    op.drop_index(op.f("ix_car_listings_seller_type"), table_name="car_listings")
    op.drop_index(op.f("ix_car_listings_seller_country"), table_name="car_listings")
    op.drop_index(op.f("ix_car_listings_model"), table_name="car_listings")
    op.drop_index(op.f("ix_car_listings_id"), table_name="car_listings")
    op.drop_index(op.f("ix_car_listings_damaged"), table_name="car_listings")
    op.drop_index(op.f("ix_car_listings_brand"), table_name="car_listings")
    op.drop_table("car_listings")
