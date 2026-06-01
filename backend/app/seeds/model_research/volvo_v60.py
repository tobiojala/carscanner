from decimal import Decimal
from typing import Any

from app.models import ModelResearch

VOLVO_V60_PROFILE: dict[str, Any] = {
    "brand": "Volvo",
    "model": "V60",
    "generation": "V60 I facelift / V60 II",
    "target_market": "Sweden",
    "preferred_years": [2018, 2019, 2020, 2021, 2022],
    "acceptable_years": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    "preferred_mileage_range": {"min": 60000, "max": 150000},
    "acceptable_mileage_range": {"min": 30000, "max": 190000},
    "preferred_colors": ["black", "grey", "silver", "white"],
    "weak_colors": ["brown", "gold", "green", "red", "unusual wrap colors"],
    "preferred_trims": [
        "R-Design",
        "Inscription",
        "Momentum Advanced",
        "well-equipped V60 II",
        "dealer-listed family specification",
    ],
    "acceptable_trims": [
        "Momentum",
        "Business",
        "Kinetic if priced conservatively",
        "well-equipped base trim",
    ],
    "preferred_engines": ["D4", "D5", "T5", "B4 diesel", "B5 petrol"],
    "acceptable_engines": [
        "D3 if well equipped and priced low",
        "T4 if low mileage and strong equipment",
        "manual only if significantly discounted",
    ],
    "high_value_options": [
        "automatic gearbox",
        "auxiliary heater",
        "Head-Up Display",
        "panoramic roof",
        "electric seats",
        "adaptive cruise control",
        "Pilot Assist",
        "tow hitch",
        "LED headlights",
        "winter package",
        "heated seats",
        "heated steering wheel",
        "parking camera",
        "360 camera",
        "navigation",
        "premium audio",
        "full Volvo service history",
        "dealer listing",
        "low owner count",
    ],
    "risk_flags": [
        "accident history",
        "missing service history",
        "high owner count",
        "damaged vehicle",
        "mileage above 190000 km",
        "weak equipment level",
        "imported multiple times",
        "poor maintenance records",
        "automatic gearbox service uncertainty",
        "diesel emissions or DPF issues",
        "AdBlue or EGR issues on diesel cars",
        "suspiciously low price",
        "manual gearbox on premium-priced car",
        "missing winter equipment",
        "unclear ownership history",
    ],
    "swedish_desirability_factors": [
        "Volvo brand trust is very strong in Sweden and improves buyer confidence.",
        "V60 wagon body style has strong family and commuter appeal.",
        "R-Design trim creates a clear resale premium.",
        "Inscription trim appeals to buyers seeking comfort and equipment.",
        "Momentum is acceptable as a baseline if equipment and price are strong.",
        "D4 is a familiar and desirable Swedish-market engine when service history is complete.",
        "T5 can be attractive for buyers wanting petrol power and lower diesel-risk exposure.",
        "Auxiliary heater has meaningful value in the Swedish winter market.",
        "Pilot Assist and adaptive cruise increase desirability on newer cars.",
        "Tow hitch adds practical value for Swedish wagon buyers.",
        "Neutral colors improve liquidity and reduce resale friction.",
        "Full Volvo service history materially improves confidence.",
        "Dealer listings and low owner count support stronger resale trust.",
    ],
    "liquidity_score": 87,
    "risk_score": 36,
    "confidence_score": 72,
    "target_buy_price_eur": {"min": 19000, "max": 26500},
    "target_sell_price_sek": {"min": 315000, "max": 355000},
    "research_notes": [
        "Use conservative resale assumptions because V60 pricing depends heavily on generation, trim, mileage, equipment, service history, and engine.",
        "Best candidates are neutral-color V60 II cars with R-Design or Inscription trim, automatic gearbox, auxiliary heater, Pilot Assist, adaptive cruise, tow hitch, and full Volvo service history.",
        "D4 remains attractive in Sweden when maintenance history is clear, but diesel emissions and high-mileage drivetrain risks should be checked.",
        "T5 petrol cars can have strong desirability if priced correctly and well equipped.",
        "Auxiliary heater, winter package, heated seats, heated steering wheel, and tow hitch should receive a Swedish-market practicality premium.",
        "Avoid weakly equipped cars unless the purchase price is low enough to compensate for slower resale.",
        "Cars above 190000 km should be discounted conservatively unless service history is excellent and major maintenance is documented.",
        "Imported multiple times or unclear ownership history should reduce confidence.",
        "Search filters indicate Germany-only, wagon body, neutral colors, 2015+ model years, diesel or petrol fuel, automatic gearbox, and premium equipment filters such as auxiliary heater, electric seats, Head-Up Display, and sunroof.",
        "Manual validation should compare each candidate against Swedish Volvo V60 listings with similar generation, year, mileage, trim, engine, gearbox, and winter equipment.",
        "A target buy price above 26500 EUR should only be considered for unusually strong low-mileage V60 II R-Design or Inscription examples with excellent equipment and complete Volvo service history.",
    ],
}


def build_volvo_v60_seed() -> ModelResearch:
    preferred_years = VOLVO_V60_PROFILE["preferred_years"]
    acceptable_years = VOLVO_V60_PROFILE["acceptable_years"]
    preferred_mileage = VOLVO_V60_PROFILE["preferred_mileage_range"]
    acceptable_mileage = VOLVO_V60_PROFILE["acceptable_mileage_range"]
    preferred_trims = VOLVO_V60_PROFILE["preferred_trims"]
    acceptable_trims = VOLVO_V60_PROFILE["acceptable_trims"]
    preferred_engines = VOLVO_V60_PROFILE["preferred_engines"]
    acceptable_engines = VOLVO_V60_PROFILE["acceptable_engines"]
    high_value_options = VOLVO_V60_PROFILE["high_value_options"]
    risk_flags = VOLVO_V60_PROFILE["risk_flags"]
    desirability = VOLVO_V60_PROFILE["swedish_desirability_factors"]
    research_notes = VOLVO_V60_PROFILE["research_notes"]
    buy_price = VOLVO_V60_PROFILE["target_buy_price_eur"]
    sell_price = VOLVO_V60_PROFILE["target_sell_price_sek"]

    return ModelResearch(
        brand="Volvo",
        model="V60",
        variant="D4",
        good_years=(
            f"Preferred {min(preferred_years)}-{max(preferred_years)}; "
            f"acceptable {min(acceptable_years)}-{max(acceptable_years)}; "
            f"preferred mileage {preferred_mileage['min']}-{preferred_mileage['max']} km; "
            f"acceptable mileage {acceptable_mileage['min']}-{acceptable_mileage['max']} km."
        ),
        strong_trims=[*preferred_trims, *preferred_engines, *high_value_options],
        weak_trims=[
            "weak equipment level",
            "manual gearbox unless significantly discounted",
            "missing winter equipment",
            "unclear ownership history",
            *acceptable_trims,
            *acceptable_engines,
        ],
        common_issues="; ".join(risk_flags),
        swedish_demand_score=88,
        german_supply_score=72,
        liquidity_score=VOLVO_V60_PROFILE["liquidity_score"],
        risk_notes=" ".join(
            [
                f"Risk score {VOLVO_V60_PROFILE['risk_score']}; confidence score {VOLVO_V60_PROFILE['confidence_score']}.",
                *desirability,
                *research_notes,
            ]
        ),
        target_buy_price_min=Decimal(str(buy_price["min"])),
        target_buy_price_max=Decimal(str(buy_price["max"])),
        target_sell_price_min=Decimal(str(sell_price["min"])),
        target_sell_price_max=Decimal(str(sell_price["max"])),
    )
