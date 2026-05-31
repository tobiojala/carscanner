from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    Alert,
    CarListing,
    CostAssumption,
    Deal,
    ModelResearch,
    SwedishComparable,
)


SEED_LISTINGS = [
    {
        "source": "seed",
        "source_listing_id": "seed-rav4-2021",
        "year": 2021,
        "make": "Toyota",
        "model": "RAV4",
        "trim": "XLE",
        "body_style": "SUV",
        "fuel_type": "Gasoline",
        "transmission": "Automatic",
        "drivetrain": "AWD",
        "source_market": "Phoenix, AZ",
        "target_market": "Sweden",
        "location_city": "Phoenix",
        "asking_price": Decimal("24750.00"),
        "estimated_market_price": Decimal("28600.00"),
        "mileage": 38200,
    },
    {
        "source": "seed",
        "source_listing_id": "seed-civic-2020",
        "year": 2020,
        "make": "Honda",
        "model": "Civic",
        "trim": "EX",
        "body_style": "Sedan",
        "fuel_type": "Gasoline",
        "transmission": "CVT",
        "drivetrain": "FWD",
        "source_market": "Las Vegas, NV",
        "target_market": "Sweden",
        "location_city": "Las Vegas",
        "asking_price": Decimal("18400.00"),
        "estimated_market_price": Decimal("21150.00"),
        "mileage": 45500,
    },
    {
        "source": "seed",
        "source_listing_id": "seed-maverick-2022",
        "year": 2022,
        "make": "Ford",
        "model": "Maverick",
        "trim": "XLT Hybrid",
        "body_style": "Truck",
        "fuel_type": "Hybrid",
        "transmission": "Automatic",
        "drivetrain": "FWD",
        "source_market": "Dallas, TX",
        "target_market": "Sweden",
        "location_city": "Dallas",
        "asking_price": Decimal("26800.00"),
        "estimated_market_price": Decimal("31400.00"),
        "mileage": 21800,
    },
    {
        "source": "seed",
        "source_listing_id": "seed-outback-2019",
        "year": 2019,
        "make": "Subaru",
        "model": "Outback",
        "trim": "Limited",
        "body_style": "Wagon",
        "fuel_type": "Gasoline",
        "transmission": "CVT",
        "drivetrain": "AWD",
        "source_market": "Boise, ID",
        "target_market": "Sweden",
        "location_city": "Boise",
        "asking_price": Decimal("21950.00"),
        "estimated_market_price": Decimal("24200.00"),
        "mileage": 60300,
    },
]

SEED_COST_ASSUMPTIONS = [
    {
        "name": "US to Sweden baseline",
        "origin_market": "US",
        "destination_market": "SE",
        "currency": "SEK",
        "exchange_rate_to_sek": Decimal("10.50"),
        "transport_cost": Decimal("28000.00"),
        "import_duty_rate": Decimal("0.1000"),
        "vat_rate": Decimal("0.2500"),
        "registration_cost": Decimal("4500.00"),
        "inspection_cost": Decimal("2500.00"),
        "platform_fee": Decimal("3500.00"),
        "repair_buffer_percent": Decimal("0.0500"),
        "notes": "Baseline assumptions for local seed deals.",
    }
]

SEED_MODEL_RESEARCH = [
    {
        "make": "Toyota",
        "model": "RAV4",
        "trim": "XLE",
        "model_year_start": 2019,
        "model_year_end": 2022,
        "market": "SE",
        "average_price_sek": Decimal("318000.00"),
        "median_price_sek": Decimal("309000.00"),
        "sample_size": 18,
        "demand_score": Decimal("8.40"),
        "liquidity_score": Decimal("7.80"),
        "search_terms": {"make": "Toyota", "model": "RAV4", "trim": "XLE"},
        "notes": "Strong family SUV demand with hybrid preference.",
    },
    {
        "make": "Ford",
        "model": "Maverick",
        "trim": "XLT Hybrid",
        "model_year_start": 2022,
        "model_year_end": 2024,
        "market": "SE",
        "average_price_sek": Decimal("365000.00"),
        "median_price_sek": Decimal("358000.00"),
        "sample_size": 7,
        "demand_score": Decimal("7.60"),
        "liquidity_score": Decimal("6.90"),
        "search_terms": {"make": "Ford", "model": "Maverick", "trim": "Hybrid"},
        "notes": "Limited local supply creates arbitrage signal.",
    },
]


def _seed_car_listings(db: Session) -> dict[str, CarListing]:
    for listing in SEED_LISTINGS:
        existing_listing = db.scalars(
            select(CarListing).where(
                CarListing.source == listing["source"],
                CarListing.source_listing_id == listing["source_listing_id"],
            )
        ).first()
        if existing_listing is None:
            db.add(CarListing(**listing))

    db.flush()

    seed_source_ids = [listing["source_listing_id"] for listing in SEED_LISTINGS]
    listings = db.scalars(
        select(CarListing).where(CarListing.source_listing_id.in_(seed_source_ids))
    ).all()
    return {listing.source_listing_id or str(listing.id): listing for listing in listings}


def _seed_swedish_comparables(
    db: Session, listings_by_source_id: dict[str, CarListing]
) -> list[SwedishComparable]:
    comparable_rows = [
        {
            "car_listing_id": listings_by_source_id["seed-rav4-2021"].id,
            "source": "seed",
            "source_listing_id": "se-rav4-2021-a",
            "year": 2021,
            "make": "Toyota",
            "model": "RAV4",
            "trim": "XLE",
            "mileage_km": 62000,
            "asking_price_sek": Decimal("319000.00"),
            "location": "Stockholm",
            "dealer_name": "Seed Auto Stockholm",
            "confidence_score": Decimal("0.92"),
        },
        {
            "car_listing_id": listings_by_source_id["seed-maverick-2022"].id,
            "source": "seed",
            "source_listing_id": "se-maverick-2022-a",
            "year": 2022,
            "make": "Ford",
            "model": "Maverick",
            "trim": "XLT Hybrid",
            "mileage_km": 36000,
            "asking_price_sek": Decimal("369000.00"),
            "location": "Goteborg",
            "dealer_name": "Seed Auto Goteborg",
            "confidence_score": Decimal("0.88"),
        },
    ]
    for comparable in comparable_rows:
        existing_comparable = db.scalars(
            select(SwedishComparable).where(
                SwedishComparable.source == comparable["source"],
                SwedishComparable.source_listing_id == comparable["source_listing_id"],
            )
        ).first()
        if existing_comparable is None:
            db.add(SwedishComparable(**comparable))

    db.flush()

    seed_source_ids = [row["source_listing_id"] for row in comparable_rows]
    return db.scalars(
        select(SwedishComparable).where(
            SwedishComparable.source_listing_id.in_(seed_source_ids)
        )
    ).all()


def _seed_cost_assumptions(db: Session) -> None:
    if db.scalars(select(CostAssumption.id).limit(1)).first():
        return

    db.add_all(CostAssumption(**assumption) for assumption in SEED_COST_ASSUMPTIONS)


def _seed_model_research(db: Session) -> None:
    if db.scalars(select(ModelResearch.id).limit(1)).first():
        return

    db.add_all(ModelResearch(**research) for research in SEED_MODEL_RESEARCH)


def _seed_deals(
    db: Session,
    listings_by_source_id: dict[str, CarListing],
    comparables: list[SwedishComparable],
) -> list[Deal]:
    if not db.scalars(select(Deal.id).limit(1)).first():
        comparables_by_source_id = {
            comparable.source_listing_id: comparable for comparable in comparables
        }
        rav4 = listings_by_source_id["seed-rav4-2021"]
        maverick = listings_by_source_id["seed-maverick-2022"]
        deal_rows = [
            {
                "car_listing_id": rav4.id,
                "swedish_comparable_id": comparables_by_source_id["se-rav4-2021-a"].id,
                "status": "watching",
                "acquisition_price": rav4.asking_price,
                "estimated_sale_price_sek": Decimal("319000.00"),
                "estimated_total_cost_sek": Decimal("287500.00"),
                "estimated_profit_sek": Decimal("31500.00"),
                "margin_percent": Decimal("10.96"),
                "transport_cost_sek": Decimal("28000.00"),
                "import_cost_sek": Decimal("26000.00"),
                "inspection_cost_sek": Decimal("2500.00"),
                "repair_budget_sek": Decimal("12000.00"),
                "platform_fee_sek": Decimal("3500.00"),
                "notes": "Seed deal showing positive spread after baseline costs.",
            },
            {
                "car_listing_id": maverick.id,
                "swedish_comparable_id": comparables_by_source_id["se-maverick-2022-a"].id,
                "status": "watching",
                "acquisition_price": maverick.asking_price,
                "estimated_sale_price_sek": Decimal("369000.00"),
                "estimated_total_cost_sek": Decimal("330000.00"),
                "estimated_profit_sek": Decimal("39000.00"),
                "margin_percent": Decimal("11.82"),
                "transport_cost_sek": Decimal("30000.00"),
                "import_cost_sek": Decimal("31000.00"),
                "inspection_cost_sek": Decimal("2500.00"),
                "repair_budget_sek": Decimal("9000.00"),
                "platform_fee_sek": Decimal("3500.00"),
                "notes": "Seed deal for low-supply hybrid pickup segment.",
            },
        ]
        db.add_all(Deal(**row) for row in deal_rows)
        db.flush()

    return db.scalars(select(Deal)).all()


def _seed_alerts(db: Session, deals: list[Deal]) -> None:
    if db.scalars(select(Alert.id).limit(1)).first() or not deals:
        return

    best_deal = max(deals, key=lambda deal: deal.estimated_profit_sek)
    db.add(
        Alert(
            car_listing_id=best_deal.car_listing_id,
            deal_id=best_deal.id,
            alert_type="profit_threshold",
            severity="info",
            title="Seed deal exceeds profit threshold",
            message="A seeded opportunity has estimated profit above the local watch threshold.",
            metadata_json={"threshold_sek": 30000},
        )
    )


def seed_database(db: Session) -> None:
    listings_by_source_id = _seed_car_listings(db)
    comparables = _seed_swedish_comparables(db, listings_by_source_id)
    _seed_cost_assumptions(db)
    _seed_model_research(db)
    deals = _seed_deals(db, listings_by_source_id, comparables)
    _seed_alerts(db, deals)
    db.commit()
