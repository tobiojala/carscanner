from decimal import Decimal
from typing import Any

from app.models import ModelResearch

BMW_320D_TOURING_PROFILE: dict[str, Any] = {
    "brand": "BMW",
    "model": "320d Touring",
    "generation": "F31 LCI / early G21",
    "target_market": "Sweden",
    "preferred_years": [2018, 2019, 2020, 2021],
    "acceptable_years": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    "preferred_mileage_range": {"min": 60000, "max": 150000},
    "acceptable_mileage_range": {"min": 30000, "max": 190000},
    "preferred_colors": ["black", "grey", "silver", "white"],
    "weak_colors": ["red", "brown", "gold", "green", "unusual wrap colors"],
    "preferred_trims": ["M Sport", "Luxury Line", "xDrive Touring"],
    "acceptable_trims": ["Sport Line", "Advantage", "Business", "well-equipped base trim"],
    "high_value_options": [
        "panoramic roof",
        "Head-Up Display",
        "tow hitch",
        "adaptive cruise control",
        "Professional navigation",
        "LED headlights",
        "Harman Kardon audio",
        "xDrive",
        "sport seats",
        "heated seats",
        "parking sensors",
        "reverse camera",
        "digital service history",
    ],
    "risk_flags": [
        "missing service history",
        "accident history",
        "high owner count",
        "damaged vehicle",
        "mileage above 200000 km",
        "low equipment level",
        "unusual color",
        "manual transmission on higher-priced cars",
        "timing chain concerns on poorly maintained diesel engines",
        "DPF or EGR issues",
        "import history uncertainty",
        "suspiciously low price",
    ],
    "swedish_desirability_factors": [
        "Touring wagon body style is highly practical for Swedish buyers.",
        "BMW diesel wagons have good demand when service history is clear.",
        "M Sport and Luxury Line improve resale appeal.",
        "xDrive improves desirability for Swedish winter conditions.",
        "Neutral colors are easier to resell.",
        "Panoramic roof, Head-Up Display, tow hitch, adaptive cruise, and Professional navigation signal high equipment level.",
        "Lower mileage examples support stronger resale pricing.",
    ],
    "liquidity_score": 82,
    "risk_score": 38,
    "confidence_score": 68,
    "target_buy_price_eur": {"min": 16500, "max": 24500},
    "target_sell_price_sek": {"min": 300000, "max": 345000},
    "research_notes": [
        "Use conservative pricing because Swedish resale depends heavily on trim, service history, mileage, and xDrive availability.",
        "Best candidates are well-equipped Touring cars with M Sport or Luxury Line, neutral colors, automatic transmission, and documented service history.",
        "Avoid cars above 200000 km unless purchase price is unusually attractive and service history is excellent.",
        "F31 LCI cars can be attractive if bought cheaply; early G21 cars have stronger desirability but require stricter buy-price discipline.",
        "Verify equipment from individual listing text and photos before scoring.",
        "Manual validation should compare against Swedish BMW 320d Touring listings with similar year, mileage, trim, drivetrain, and equipment.",
    ],
}


def build_bmw_320d_touring_seed() -> ModelResearch:
    preferred_years = BMW_320D_TOURING_PROFILE["preferred_years"]
    acceptable_years = BMW_320D_TOURING_PROFILE["acceptable_years"]
    preferred_mileage = BMW_320D_TOURING_PROFILE["preferred_mileage_range"]
    acceptable_mileage = BMW_320D_TOURING_PROFILE["acceptable_mileage_range"]
    preferred_trims = BMW_320D_TOURING_PROFILE["preferred_trims"]
    acceptable_trims = BMW_320D_TOURING_PROFILE["acceptable_trims"]
    high_value_options = BMW_320D_TOURING_PROFILE["high_value_options"]
    risk_flags = BMW_320D_TOURING_PROFILE["risk_flags"]
    desirability = BMW_320D_TOURING_PROFILE["swedish_desirability_factors"]
    research_notes = BMW_320D_TOURING_PROFILE["research_notes"]
    buy_price = BMW_320D_TOURING_PROFILE["target_buy_price_eur"]
    sell_price = BMW_320D_TOURING_PROFILE["target_sell_price_sek"]

    return ModelResearch(
        brand="BMW",
        model="320d Touring",
        variant="G21",
        good_years=(
            f"Preferred {min(preferred_years)}-{max(preferred_years)}; "
            f"acceptable {min(acceptable_years)}-{max(acceptable_years)}; "
            f"preferred mileage {preferred_mileage['min']}-{preferred_mileage['max']} km; "
            f"acceptable mileage {acceptable_mileage['min']}-{acceptable_mileage['max']} km."
        ),
        strong_trims=[*preferred_trims, *high_value_options],
        weak_trims=[
            "base trim",
            "low equipment level",
            "manual transmission on premium-priced cars",
            *acceptable_trims,
        ],
        common_issues="; ".join(risk_flags),
        swedish_demand_score=84,
        german_supply_score=76,
        liquidity_score=BMW_320D_TOURING_PROFILE["liquidity_score"],
        risk_notes=" ".join([*desirability, *research_notes]),
        target_buy_price_min=Decimal(str(buy_price["min"])),
        target_buy_price_max=Decimal(str(buy_price["max"])),
        target_sell_price_min=Decimal(str(sell_price["min"])),
        target_sell_price_max=Decimal(str(sell_price["max"])),
    )
