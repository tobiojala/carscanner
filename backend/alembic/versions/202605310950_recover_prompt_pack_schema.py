"""recover stale local prompt pack schema

Revision ID: 202605310950
Revises: 202605310920
Create Date: 2026-05-31 09:50:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app import models  # noqa: F401
from app.db.base import Base

revision: str = "202605310950"
down_revision: Union[str, None] = "202605310920"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _columns_for(inspector: sa.Inspector, table_name: str) -> set[str]:
    if table_name not in inspector.get_table_names():
        return set()
    return {column["name"] for column in inspector.get_columns(table_name)}


def upgrade() -> None:
    bind = op.get_bind()
    try:
        inspector = sa.inspect(bind)
    except sa.exc.NoInspectionAvailable:
        return

    listing_columns = _columns_for(inspector, "car_listings")
    deal_columns = _columns_for(inspector, "deals")
    schema_matches_prompt_pack = {
        "brand",
        "price_eur",
        "seller_country",
        "mileage_km",
    }.issubset(listing_columns) and {
        "foreign_listing_id",
        "expected_profit_sek",
        "deal_grade",
    }.issubset(deal_columns)

    if schema_matches_prompt_pack:
        return

    # This branch has not shipped yet. For local Phase 2 Docker volumes created
    # before the prompt-pack schema alignment, reset only the app tables so the
    # backend can migrate and reseed cleanly instead of failing on stale columns.
    Base.metadata.drop_all(bind=bind)
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    pass
