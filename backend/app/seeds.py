from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CarListing


SEED_LISTINGS = [
    {
        "year": 2021,
        "make": "Toyota",
        "model": "RAV4",
        "trim": "XLE",
        "source_market": "Phoenix, AZ",
        "target_market": "Los Angeles, CA",
        "asking_price": Decimal("24750.00"),
        "estimated_market_price": Decimal("28600.00"),
        "mileage": 38200,
    },
    {
        "year": 2020,
        "make": "Honda",
        "model": "Civic",
        "trim": "EX",
        "source_market": "Las Vegas, NV",
        "target_market": "San Francisco, CA",
        "asking_price": Decimal("18400.00"),
        "estimated_market_price": Decimal("21150.00"),
        "mileage": 45500,
    },
    {
        "year": 2022,
        "make": "Ford",
        "model": "Maverick",
        "trim": "XLT Hybrid",
        "source_market": "Dallas, TX",
        "target_market": "Seattle, WA",
        "asking_price": Decimal("26800.00"),
        "estimated_market_price": Decimal("31400.00"),
        "mileage": 21800,
    },
    {
        "year": 2019,
        "make": "Subaru",
        "model": "Outback",
        "trim": "Limited",
        "source_market": "Boise, ID",
        "target_market": "Portland, OR",
        "asking_price": Decimal("21950.00"),
        "estimated_market_price": Decimal("24200.00"),
        "mileage": 60300,
    },
]


def seed_database(db: Session) -> None:
    has_listings = db.scalars(select(CarListing.id).limit(1)).first()
    if has_listings:
        return

    db.add_all(CarListing(**listing) for listing in SEED_LISTINGS)
    db.commit()
