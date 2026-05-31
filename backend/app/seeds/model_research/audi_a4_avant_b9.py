from decimal import Decimal
from typing import Any

from app.models import ModelResearch

AUDI_A4_AVANT_B9_PROFILE: dict[str, Any] = {
    "brand": "Audi",
    "model": "A4 Avant",
    "generation": "B9",
    "target_market": "Sweden",
    "preferred_years": [2017, 2018, 2019, 2020, 2021],
    "acceptable_years": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    "preferred_mileage_range": {"min": 60000, "max": 150000},
    "acceptable_mileage_range": {"min": 30000, "max": 190000},
    "preferred_colors": ["black", "grey", "silver", "white"],
    "weak_colors": ["brown", "gold", "green", "red", "unusual wrap colors"],
    "preferred_trims": [
        "S-Line",
        "quattro",
        "Sport",
        "Design",
        "well-equipped company lease return",
    ],
    "acceptable_trims": ["Business", "Advanced", "Proline", "well-equipped base trim"],
    "preferred_engines": ["2.0 TDI", "40 TDI", "45 TDI quattro", "2.0 TFSI", "40 TFSI"],
    "acceptable_engines": [
        "35 TDI if well equipped",
        "35 TFSI if low mileage and priced conservatively",
        "manual only if significantly discounted",
    ],
    "high_value_options": [
        "S-Tronic automatic",
        "quattro",
        "Virtual Cockpit",
        "electric seats",
        "panoramic roof",
        "adaptive cruise control",
        "Matrix LED headlights",
        "LED headlights",
        "tow hitch",
        "Bang & Olufsen audio",
        "Navigation Plus",
        "rear camera",
        "parking sensors",
        "heated seats",
        "sport seats",
        "winter wheels",
        "full Audi service history",
        "dealer listing",
        "low owner count",
    ],
    "risk_flags": [
        "accident history",
        "missing service history",
        "oil consumption issues",
        "high owner count",
        "damaged vehicle",
        "mileage above 190000 km",
        "weak equipment level",
        "imported multiple times",
        "S-Tronic service uncertainty",
        "quattro drivetrain service uncertainty",
        "suspiciously low price",
        "unusual color",
        "manual gearbox on premium-priced car",
    ],
    "swedish_desirability_factors": [
        "Avant wagon body style has strong Swedish family and commuter appeal.",
        "Premium wagon demand is strong when equipment level and service history are credible.",
        "quattro materially improves desirability in Sweden due winter conditions.",
        "S-Line trim supports a clear resale premium.",
        "S-Tronic automatic is expected by many buyers in this segment.",
        "Virtual Cockpit, Matrix LED headlights, Navigation Plus, rear camera, and Bang & Olufsen audio support stronger pricing.",
        "Tow hitch and winter wheels improve practical Swedish appeal.",
        "Neutral colors improve liquidity and reduce resale friction.",
        "2017+ B9 cars are easier to position than early high-mile examples.",
        "Dealer listings and full Audi service history increase confidence.",
    ],
    "liquidity_score": 84,
    "risk_score": 40,
    "confidence_score": 70,
    "target_buy_price_eur": {"min": 18500, "max": 26000},
    "target_sell_price_sek": {"min": 275000, "max": 315000},
    "research_notes": [
        "Use conservative resale assumptions because Audi A4 Avant pricing depends heavily on quattro, S-Line, mileage, service history, and equipment level.",
        "Best candidates are neutral-color Avant cars with S-Line, quattro, S-Tronic, Virtual Cockpit, Matrix LED headlights, Navigation Plus, rear camera, and full Audi service history.",
        "quattro should receive a meaningful Swedish desirability premium, especially when paired with S-Line and automatic transmission.",
        "Avoid high-mileage or weakly equipped cars unless purchase price is low enough to compensate for slower resale.",
        "Oil consumption history and drivetrain service documentation should be checked before assigning high confidence.",
        "Imported multiple times or unclear ownership history should reduce confidence and increase risk.",
        "Search filters indicate Germany-only, wagon body, neutral colors, 2015+ model years, diesel or petrol fuel, automatic or semi-automatic transmission, and premium equipment filters such as electric seats and sunroof.",
        "Manual validation should compare each candidate against Swedish Audi A4 Avant listings with similar generation, year, mileage, engine, quattro status, trim, and equipment.",
        "A target buy price above 26000 EUR should only be considered for unusually strong low-mileage S-Line quattro cars with excellent equipment and service history.",
    ],
}


def build_audi_a4_avant_b9_seed() -> ModelResearch:
    preferred_years = AUDI_A4_AVANT_B9_PROFILE["preferred_years"]
    acceptable_years = AUDI_A4_AVANT_B9_PROFILE["acceptable_years"]
    preferred_mileage = AUDI_A4_AVANT_B9_PROFILE["preferred_mileage_range"]
    acceptable_mileage = AUDI_A4_AVANT_B9_PROFILE["acceptable_mileage_range"]
    preferred_trims = AUDI_A4_AVANT_B9_PROFILE["preferred_trims"]
    acceptable_trims = AUDI_A4_AVANT_B9_PROFILE["acceptable_trims"]
    preferred_engines = AUDI_A4_AVANT_B9_PROFILE["preferred_engines"]
    acceptable_engines = AUDI_A4_AVANT_B9_PROFILE["acceptable_engines"]
    high_value_options = AUDI_A4_AVANT_B9_PROFILE["high_value_options"]
    risk_flags = AUDI_A4_AVANT_B9_PROFILE["risk_flags"]
    desirability = AUDI_A4_AVANT_B9_PROFILE["swedish_desirability_factors"]
    research_notes = AUDI_A4_AVANT_B9_PROFILE["research_notes"]
    buy_price = AUDI_A4_AVANT_B9_PROFILE["target_buy_price_eur"]
    sell_price = AUDI_A4_AVANT_B9_PROFILE["target_sell_price_sek"]

    return ModelResearch(
        brand="Audi",
        model="A4 Avant",
        variant="B9",
        good_years=(
            f"Preferred {min(preferred_years)}-{max(preferred_years)}; "
            f"acceptable {min(acceptable_years)}-{max(acceptable_years)}; "
            f"preferred mileage {preferred_mileage['min']}-{preferred_mileage['max']} km; "
            f"acceptable mileage {acceptable_mileage['min']}-{acceptable_mileage['max']} km."
        ),
        strong_trims=[*preferred_trims, *preferred_engines, *high_value_options],
        weak_trims=[
            "weak equipment level",
            "manual gearbox on premium-priced car",
            "imported multiple times",
            "mileage above 190000 km",
            *acceptable_trims,
            *acceptable_engines,
        ],
        common_issues="; ".join(risk_flags),
        swedish_demand_score=84,
        german_supply_score=80,
        liquidity_score=AUDI_A4_AVANT_B9_PROFILE["liquidity_score"],
        risk_notes=" ".join(
            [
                f"Risk score {AUDI_A4_AVANT_B9_PROFILE['risk_score']}; confidence score {AUDI_A4_AVANT_B9_PROFILE['confidence_score']}.",
                *desirability,
                *research_notes,
            ]
        ),
        target_buy_price_min=Decimal(str(buy_price["min"])),
        target_buy_price_max=Decimal(str(buy_price["max"])),
        target_sell_price_min=Decimal(str(sell_price["min"])),
        target_sell_price_max=Decimal(str(sell_price["max"])),
    )
