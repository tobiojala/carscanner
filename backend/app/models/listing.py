from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CarListing(Base):
    __tablename__ = "car_listings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    make: Mapped[str] = mapped_column(String(80), nullable=False)
    model: Mapped[str] = mapped_column(String(120), nullable=False)
    trim: Mapped[str | None] = mapped_column(String(120), nullable=True)
    source_market: Mapped[str] = mapped_column(String(80), nullable=False)
    target_market: Mapped[str] = mapped_column(String(80), nullable=False)
    asking_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    estimated_market_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
