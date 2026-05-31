from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Alert, CarListing, CostAssumption, Deal, ModelResearch, SwedishComparable
from app.scoring import DealScoringInput, ProfitCalculationInput, calculate_profit, score_deal
from app.seeds.model_research import (
    build_bmw_320d_touring_seed,
    build_vw_golf_variant_mk7_seed,
    build_vw_passat_gte_variant_seed,
)

DEFAULT_COST_ASSUMPTIONS = {
    "eur_to_sek_rate": Decimal("11.40"),
    "default_transport_cost_sek": Decimal("8000.00"),
    "default_registration_cost_sek": Decimal("4000.00"),
    "default_inspection_cost_sek": Decimal("2500.00"),
    "default_repair_buffer_sek": Decimal("10000.00"),
    "default_tax_cost_sek": Decimal("0.00"),
    "default_other_costs_sek": Decimal("3000.00"),
    "minimum_profit_threshold_sek": Decimal("20000.00"),
    "minimum_confidence_score": 65,
}

SEED_LISTINGS = [
    {
        "source": "mobile.de",
        "source_listing_id": "mock-de-vw-golf-gtd-2018",
        "listing_url": "https://example.com/mobile-de/vw-golf-gtd-2018",
        "seller_country": "DE",
        "seller_type": "dealer",
        "brand": "VW",
        "model": "Golf",
        "variant": "GTD",
        "trim": "GTD DSG",
        "year": 2018,
        "first_registration_date": date(2018, 5, 1),
        "mileage_km": 118000,
        "fuel_type": "diesel",
        "transmission": "automatic",
        "drivetrain": "FWD",
        "body_type": "hatchback",
        "color": "white",
        "price_eur": Decimal("15900.00"),
        "currency": "EUR",
        "vat_deductible": True,
        "damaged": False,
        "accident_history": "No known accident history",
        "service_history": "Full service history",
        "description": "Mock German listing for Phase 2 local MVP.",
        "image_urls": [],
    },
    {
        "source": "AutoScout24",
        "source_listing_id": "mock-de-vw-passat-gte-2020",
        "listing_url": "https://example.com/autoscout24/vw-passat-gte-2020",
        "seller_country": "DE",
        "seller_type": "dealer",
        "brand": "VW",
        "model": "Passat GTE",
        "variant": "Variant",
        "trim": "GTE Executive",
        "year": 2020,
        "first_registration_date": date(2020, 3, 15),
        "mileage_km": 96000,
        "fuel_type": "plug-in hybrid",
        "transmission": "automatic",
        "drivetrain": "FWD",
        "body_type": "wagon",
        "color": "blue",
        "price_eur": Decimal("21900.00"),
        "currency": "EUR",
        "vat_deductible": True,
        "damaged": False,
        "accident_history": "No known accident history",
        "service_history": "Dealer service records available",
        "description": "Mock German listing for Swedish hybrid demand validation.",
        "image_urls": [],
    },
    {
        "source": "mobile.de",
        "source_listing_id": "mock-de-bmw-320d-touring-2019",
        "listing_url": "https://example.com/mobile-de/bmw-320d-touring-2019",
        "seller_country": "DE",
        "seller_type": "dealer",
        "brand": "BMW",
        "model": "320d Touring",
        "variant": "G21",
        "trim": "M Sport",
        "year": 2019,
        "first_registration_date": date(2019, 9, 10),
        "mileage_km": 132000,
        "fuel_type": "diesel",
        "transmission": "automatic",
        "drivetrain": "RWD",
        "body_type": "wagon",
        "color": "black",
        "price_eur": Decimal("22900.00"),
        "currency": "EUR",
        "vat_deductible": False,
        "damaged": False,
        "accident_history": "No accidents reported by seller",
        "service_history": "Digital service history",
        "description": "Mock German premium wagon listing.",
        "image_urls": [],
    },
    {
        "source": "AutoScout24",
        "source_listing_id": "mock-de-audi-a4-avant-2018",
        "listing_url": "https://example.com/autoscout24/audi-a4-avant-2018",
        "seller_country": "DE",
        "seller_type": "private",
        "brand": "Audi",
        "model": "A4 Avant",
        "variant": "B9",
        "trim": "S-Line quattro",
        "year": 2018,
        "first_registration_date": date(2018, 8, 20),
        "mileage_km": 144000,
        "fuel_type": "diesel",
        "transmission": "automatic",
        "drivetrain": "AWD",
        "body_type": "wagon",
        "color": "gray",
        "price_eur": Decimal("20500.00"),
        "currency": "EUR",
        "vat_deductible": False,
        "damaged": False,
        "accident_history": "Seller says minor paintwork on rear bumper",
        "service_history": "Partial service history",
        "description": "Mock private seller listing with moderate risk flags.",
        "image_urls": [],
    },
    {
        "source": "mobile.de",
        "source_listing_id": "mock-de-volvo-v60-d4-2019",
        "listing_url": "https://example.com/mobile-de/volvo-v60-d4-2019",
        "seller_country": "DE",
        "seller_type": "dealer",
        "brand": "Volvo",
        "model": "V60",
        "variant": "D4",
        "trim": "R-Design",
        "year": 2019,
        "first_registration_date": date(2019, 4, 2),
        "mileage_km": 121000,
        "fuel_type": "diesel",
        "transmission": "automatic",
        "drivetrain": "FWD",
        "body_type": "wagon",
        "color": "silver",
        "price_eur": Decimal("23900.00"),
        "currency": "EUR",
        "vat_deductible": True,
        "damaged": False,
        "accident_history": "No known accident history",
        "service_history": "Full service history",
        "description": "Mock Volvo wagon listing for Sweden resale validation.",
        "image_urls": [],
    },
]

SEED_COMPARABLES = [
    ("VW", "Golf", "GTD", 2018, 124000, "diesel", "automatic", "GTD", Decimal("229000.00"), "Stockholm", "dealer", 18),
    ("VW", "Golf", "GTD", 2017, 132000, "diesel", "automatic", "GTD", Decimal("218000.00"), "Malmo", "dealer", 32),
    ("VW", "Passat GTE", "Variant", 2020, 104000, "plug-in hybrid", "automatic", "GTE", Decimal("299000.00"), "Goteborg", "dealer", 21),
    ("VW", "Passat GTE", "Variant", 2019, 113000, "plug-in hybrid", "automatic", "GTE", Decimal("279000.00"), "Uppsala", "dealer", 28),
    ("BMW", "320d Touring", "G21", 2019, 139000, "diesel", "automatic", "M Sport", Decimal("319000.00"), "Stockholm", "dealer", 36),
    ("BMW", "320d Touring", "G21", 2020, 126000, "diesel", "automatic", "M Sport", Decimal("339000.00"), "Helsingborg", "dealer", 42),
    ("Audi", "A4 Avant", "B9", 2018, 151000, "diesel", "automatic", "S-Line", Decimal("285000.00"), "Vasteras", "private", 48),
    ("Audi", "A4 Avant", "B9", 2019, 138000, "diesel", "automatic", "quattro", Decimal("305000.00"), "Stockholm", "dealer", 34),
    ("Volvo", "V60", "D4", 2019, 129000, "diesel", "automatic", "R-Design", Decimal("329000.00"), "Linkoping", "dealer", 22),
    ("Volvo", "V60", "D4", 2020, 118000, "diesel", "automatic", "Inscription", Decimal("345000.00"), "Goteborg", "dealer", 27),
]

MODEL_RESEARCH = [
    ("Audi", "A4 Avant", "B9", "2014-2020", ["S-Line", "quattro"], ["manual base trim"], "Check gearbox and quattro service history.", 82, 80, 78, "Strong resale but private sellers increase risk.", Decimal("18500"), Decimal("22000"), Decimal("275000"), Decimal("315000")),
    ("Volvo", "V60", "D4", "2015-2020", ["R-Design", "Inscription"], ["fleet base cars"], "Confirm import equipment and service records.", 88, 72, 84, "Swedish brand trust supports resale.", Decimal("22000"), Decimal("25000"), Decimal("315000"), Decimal("355000")),
]

ESTIMATED_SWEDISH_PRICES = {
    "mock-de-vw-golf-gtd-2018": Decimal("226000.00"),
    "mock-de-vw-passat-gte-2020": Decimal("292000.00"),
    "mock-de-bmw-320d-touring-2019": Decimal("326000.00"),
    "mock-de-audi-a4-avant-2018": Decimal("296000.00"),
    "mock-de-volvo-v60-d4-2019": Decimal("337000.00"),
}


def _seed_cost_assumptions(db: Session) -> CostAssumption:
    existing = db.scalars(select(CostAssumption).limit(1)).first()
    if existing:
        return existing

    assumption = CostAssumption(**DEFAULT_COST_ASSUMPTIONS)
    db.add(assumption)
    db.flush()
    return assumption


def _seed_listings(db: Session) -> dict[str, CarListing]:
    for listing in SEED_LISTINGS:
        existing = db.scalars(
            select(CarListing).where(
                CarListing.source == listing["source"],
                CarListing.source_listing_id == listing["source_listing_id"],
            )
        ).first()
        if existing is None:
            db.add(CarListing(**listing))

    db.flush()
    source_ids = [listing["source_listing_id"] for listing in SEED_LISTINGS]
    listings = db.scalars(
        select(CarListing).where(CarListing.source_listing_id.in_(source_ids))
    ).all()
    return {listing.source_listing_id: listing for listing in listings}


def _seed_comparables(db: Session) -> None:
    if db.scalars(select(SwedishComparable.id).limit(1)).first():
        return

    comparables = [
        SwedishComparable(
            source="mock_swedish_market",
            listing_url=f"https://example.com/swedish-comparable/{index}",
            brand=brand,
            model=model,
            variant=variant,
            year=year,
            mileage_km=mileage_km,
            fuel_type=fuel_type,
            transmission=transmission,
            trim=trim,
            price_sek=price_sek,
            location=location,
            seller_type=seller_type,
            listing_age_days=listing_age_days,
        )
        for index, (
            brand,
            model,
            variant,
            year,
            mileage_km,
            fuel_type,
            transmission,
            trim,
            price_sek,
            location,
            seller_type,
            listing_age_days,
        ) in enumerate(SEED_COMPARABLES, start=1)
    ]
    db.add_all(comparables)


def _seed_model_research(db: Session) -> None:
    research_objects = [
        ModelResearch(
            brand=row[0],
            model=row[1],
            variant=row[2],
            good_years=row[3],
            strong_trims=row[4],
            weak_trims=row[5],
            common_issues=row[6],
            swedish_demand_score=row[7],
            german_supply_score=row[8],
            liquidity_score=row[9],
            risk_notes=row[10],
            target_buy_price_min=row[11],
            target_buy_price_max=row[12],
            target_sell_price_min=row[13],
            target_sell_price_max=row[14],
        )
        for row in MODEL_RESEARCH
    ]
    research_objects.extend([
        build_bmw_320d_touring_seed(),
        build_vw_golf_variant_mk7_seed(),
        build_vw_passat_gte_variant_seed(),
    ])

    for research in research_objects:
        existing = db.scalars(
            select(ModelResearch).where(
                ModelResearch.brand == research.brand,
                ModelResearch.model == research.model,
                ModelResearch.variant == research.variant,
            )
        ).first()
        if existing is not None:
            continue

        db.add(research)


def _average_listing_age_for_model(db: Session, listing: CarListing) -> int:
    ages = db.scalars(
        select(SwedishComparable.listing_age_days).where(
            SwedishComparable.brand == listing.brand,
            SwedishComparable.model == listing.model,
        )
    ).all()
    known_ages = [age for age in ages if age is not None]
    if not known_ages:
        return 45
    return round(sum(known_ages) / len(known_ages))


def _comparable_count_for_model(db: Session, listing: CarListing) -> int:
    return len(
        db.scalars(
            select(SwedishComparable.id).where(
                SwedishComparable.brand == listing.brand,
                SwedishComparable.model == listing.model,
            )
        ).all()
    )


def _model_liquidity_score(db: Session, listing: CarListing) -> int:
    research = db.scalars(
        select(ModelResearch).where(
            ModelResearch.brand == listing.brand,
            ModelResearch.model == listing.model,
            ModelResearch.variant == listing.variant,
        )
    ).first()
    return research.liquidity_score if research else 70


def _seed_deals(db: Session, listings_by_source_id: dict[str, CarListing], assumptions: CostAssumption) -> list[Deal]:
    if db.scalars(select(Deal.id).limit(1)).first():
        return db.scalars(select(Deal)).all()

    deals: list[Deal] = []
    for source_listing_id, listing in listings_by_source_id.items():
        profit = calculate_profit(
            ProfitCalculationInput(
                purchase_price_eur=listing.price_eur,
                eur_to_sek_rate=assumptions.eur_to_sek_rate,
                estimated_swedish_price_sek=ESTIMATED_SWEDISH_PRICES[source_listing_id],
                transport_cost_sek=assumptions.default_transport_cost_sek,
                registration_cost_sek=assumptions.default_registration_cost_sek,
                inspection_cost_sek=assumptions.default_inspection_cost_sek,
                repair_buffer_sek=assumptions.default_repair_buffer_sek,
                tax_cost_sek=assumptions.default_tax_cost_sek,
                other_costs_sek=assumptions.default_other_costs_sek,
                desired_profit_sek=assumptions.minimum_profit_threshold_sek,
            )
        )
        comparable_count = _comparable_count_for_model(db, listing)
        scoring = score_deal(
            DealScoringInput(
                expected_profit_sek=float(profit.expected_profit_sek),
                comparable_count=comparable_count,
                mileage_difference_km=12_000,
                year_difference=1,
                trim_matches=True,
                seller_type=listing.seller_type,
                has_service_history=bool(listing.service_history and "partial" not in listing.service_history.lower()),
                damaged=listing.damaged,
                accident_history=bool(listing.accident_history and "minor" in listing.accident_history.lower()),
                missing_data_points=0,
                average_listing_age_days=_average_listing_age_for_model(db, listing),
                model_popularity_score=_model_liquidity_score(db, listing),
            )
        )
        deal = Deal(
            foreign_listing_id=listing.id,
            estimated_swedish_price_sek=ESTIMATED_SWEDISH_PRICES[source_listing_id],
            purchase_price_sek=profit.purchase_price_sek,
            transport_cost_sek=assumptions.default_transport_cost_sek,
            registration_cost_sek=assumptions.default_registration_cost_sek,
            inspection_cost_sek=assumptions.default_inspection_cost_sek,
            repair_buffer_sek=assumptions.default_repair_buffer_sek,
            tax_cost_sek=assumptions.default_tax_cost_sek,
            other_costs_sek=assumptions.default_other_costs_sek,
            total_landed_cost_sek=profit.total_landed_cost_sek,
            expected_profit_sek=profit.expected_profit_sek,
            margin_percent=profit.margin_percent,
            confidence_score=scoring.confidence_score,
            risk_score=scoring.risk_score,
            liquidity_score=scoring.liquidity_score,
            deal_grade=scoring.deal_grade,
            status="new",
            notes="Seeded mock opportunity for Phase 2 local MVP.",
            explanation=scoring.explanation,
            risk_flags=scoring.risk_flags,
        )
        deals.append(deal)

    db.add_all(deals)
    db.flush()
    return deals


def _seed_alerts(db: Session, deals: list[Deal]) -> None:
    if db.scalars(select(Alert.id).limit(1)).first() or not deals:
        return

    best_deal = max(deals, key=lambda deal: deal.expected_profit_sek)
    db.add(
        Alert(
            deal_id=best_deal.id,
            alert_type="high_confidence_opportunity",
            message=(
                "Mock opportunity exceeds the minimum Phase 2 profit threshold "
                f"with grade {best_deal.deal_grade}."
            ),
            sent=False,
        )
    )


def seed_database(db: Session) -> None:
    assumptions = _seed_cost_assumptions(db)
    listings_by_source_id = _seed_listings(db)
    _seed_comparables(db)
    _seed_model_research(db)
    db.flush()
    deals = _seed_deals(db, listings_by_source_id, assumptions)
    _seed_alerts(db, deals)
    db.commit()
