"""add deal transparency rejection and outcome fields

Revision ID: 202606011757
Revises: 202605310950
Create Date: 2026-06-01 17:57:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "202606011757"
down_revision: Union[str, None] = "202605310950"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _columns() -> set[str] | None:
    bind = op.get_bind()
    try:
        inspector = sa.inspect(bind)
    except sa.exc.NoInspectionAvailable:
        return None
    if "deals" not in inspector.get_table_names():
        return set()
    return {column["name"] for column in inspector.get_columns("deals")}


def _add_column_if_missing(existing: set[str] | None, column: sa.Column) -> None:
    if existing is None or column.name not in existing:
        op.add_column("deals", column)


def _drop_column_if_exists(existing: set[str] | None, column_name: str) -> None:
    if existing is None or column_name in existing:
        op.drop_column("deals", column_name)


def upgrade() -> None:
    existing = _columns()
    _add_column_if_missing(existing, sa.Column("desired_minimum_profit_sek", sa.Numeric(12, 2), server_default="20000", nullable=False))
    _add_column_if_missing(existing, sa.Column("recommended_max_bid_eur", sa.Numeric(12, 2), server_default="0", nullable=False))
    _add_column_if_missing(existing, sa.Column("eur_to_sek_rate", sa.Numeric(12, 4), server_default="11.4000", nullable=False))
    _add_column_if_missing(existing, sa.Column("confidence_explanation", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False))
    _add_column_if_missing(existing, sa.Column("reject_reason", sa.String(length=120), nullable=True))
    _add_column_if_missing(existing, sa.Column("reject_notes", sa.Text(), nullable=True))
    _add_column_if_missing(existing, sa.Column("actual_purchase_price_sek", sa.Numeric(12, 2), nullable=True))
    _add_column_if_missing(existing, sa.Column("actual_transport_cost_sek", sa.Numeric(12, 2), nullable=True))
    _add_column_if_missing(existing, sa.Column("actual_registration_cost_sek", sa.Numeric(12, 2), nullable=True))
    _add_column_if_missing(existing, sa.Column("actual_repair_cost_sek", sa.Numeric(12, 2), nullable=True))
    _add_column_if_missing(existing, sa.Column("actual_total_cost_sek", sa.Numeric(12, 2), nullable=True))
    _add_column_if_missing(existing, sa.Column("actual_sale_price_sek", sa.Numeric(12, 2), nullable=True))
    _add_column_if_missing(existing, sa.Column("actual_profit_sek", sa.Numeric(12, 2), nullable=True))
    _add_column_if_missing(existing, sa.Column("days_to_sell", sa.Integer(), nullable=True))
    _add_column_if_missing(existing, sa.Column("lesson_learned", sa.Text(), nullable=True))


def downgrade() -> None:
    existing = _columns()
    for column_name in [
        "lesson_learned",
        "days_to_sell",
        "actual_profit_sek",
        "actual_sale_price_sek",
        "actual_total_cost_sek",
        "actual_repair_cost_sek",
        "actual_registration_cost_sek",
        "actual_transport_cost_sek",
        "actual_purchase_price_sek",
        "reject_notes",
        "reject_reason",
        "confidence_explanation",
        "eur_to_sek_rate",
        "recommended_max_bid_eur",
        "desired_minimum_profit_sek",
    ]:
        _drop_column_if_exists(existing, column_name)
