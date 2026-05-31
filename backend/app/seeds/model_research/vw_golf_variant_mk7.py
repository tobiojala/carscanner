from decimal import Decimal
from typing import Any

from app.models import ModelResearch

VW_GOLF_VARIANT_MK7_PROFILE: dict[str, Any] = {
    "brand": "Volkswagen",
    "model": "Golf Variant",
    "generation": "Mk7 / Mk7.5",
    "target_market": "Sweden",
    "preferred_years": [2017, 2018, 2019, 2020],
    "acceptable_years": [2015, 2016, 2017, 2018, 2019, 2020],
    "preferred_mileage_range": {"min": 50000, "max": 140000},
    "acceptable_mileage_range": {"min": 30000, "max": 190000},
    "preferred_colors": ["black", "grey", "silver", "white"],
    "weak_colors": ["brown", "red", "gold", "green", "unusual wrap colors"],
    "preferred_trims": [
        "R-Line",
        "GTD",
        "Highline",
        "well-equipped Mk7.5 Variant",
    ],
    "acceptable_trims": [
        "Comfortline",
        "Business",
        "Alltrack if priced conservatively",
        "well-equipped base trim",
    ],
    "preferred_engines": ["1.5 TSI", "1.4 TSI", "2.0 TDI", "GTD 2.0 TDI"],
    "acceptable_engines": [
        "1.6 TDI",
        "1.0 TSI if low mileage and cheap",
        "hybrid only if specification and pricing are clearly attractive",
    ],
    "high_value_options": [
        "DSG automatic",
        "adaptive cruise control",
        "tow hitch",
        "LED headlights",
        "Discover Pro navigation",
        "rear camera",
        "heated seats",
        "parking sensors",
        "digital cockpit",
        "winter wheels",
        "full service history",
        "dealer listing",
        "R-Line exterior package",
        "sports seats",
    ],
    "risk_flags": [
        "accident history",
        "missing service history",
        "very basic equipment",
        "manual gearbox unless purchase price is very attractive",
        "high owner count",
        "mileage above 190000 km",
        "damaged car",
        "weak engine and trim combination",
        "DSG service uncertainty",
        "diesel emissions or DPF issues",
        "timing belt or major service due",
        "suspiciously low price",
        "unusual color",
    ],
    "swedish_desirability_factors": [
        "Golf Variant has strong family wagon practicality for Swedish buyers.",
        "Low running costs support commuter demand.",
        "Neutral colors improve liquidity.",
        "2017+ Mk7.5 facelift cars are more desirable and easier to resell.",
        "DSG automatic improves resale appeal.",
        "R-Line, GTD, and Highline trims command stronger interest.",
        "Tow hitch and winter wheels increase practical Swedish appeal.",
        "Adaptive cruise, LED headlights, Discover Pro, rear camera, and heated seats support a pricing premium.",
        "Petrol TSI cars may appeal to urban buyers with lower annual mileage.",
        "2.0 TDI and GTD can appeal to long-distance commuters if service history is strong.",
        "Dealer listings and full service history improve confidence.",
    ],
    "liquidity_score": 86,
    "risk_score": 34,
    "confidence_score": 72,
    "target_buy_price_eur": {"min": 10500, "max": 18500},
    "target_sell_price_sek": {"min": 210000, "max": 240000},
    "research_notes": [
        "Use conservative assumptions because Golf Variant pricing is sensitive to mileage, trim, engine, DSG, and equipment level.",
        "Best import candidates are neutral-color Mk7.5 Variant cars with DSG, R-Line, GTD, or Highline trim, full service history, and practical options.",
        "Avoid very basic manual cars unless purchase price is low enough to compensate for weaker Swedish resale demand.",
        "Mileage above 190000 km should materially reduce confidence unless service history is excellent and price is very attractive.",
        "Diesel cars can work for commuter buyers, but DPF/emissions risk and local demand should be checked against Swedish comparables.",
        "Petrol 1.4 TSI and 1.5 TSI cars may have broader private-buyer appeal if running costs are low and equipment level is strong.",
        "Search filters indicate Germany-only, wagon body, non-damaged vehicles, neutral colors, 2015+ model years, hybrid fuel filter, and mileage capped around 200000 km; verify actual engine and fuel type on each individual listing.",
        "Manual validation should compare each candidate against Swedish Golf Variant listings with similar year, mileage, engine, gearbox, trim, and equipment.",
        "A target buy price above 18500 EUR should only be considered for unusually strong GTD/R-Line/Highline examples with low mileage and excellent equipment.",
    ],
}


def build_vw_golf_variant_mk7_seed() -> ModelResearch:
    preferred_years = VW_GOLF_VARIANT_MK7_PROFILE["preferred_years"]
    acceptable_years = VW_GOLF_VARIANT_MK7_PROFILE["acceptable_years"]
    preferred_mileage = VW_GOLF_VARIANT_MK7_PROFILE["preferred_mileage_range"]
    acceptable_mileage = VW_GOLF_VARIANT_MK7_PROFILE["acceptable_mileage_range"]
    preferred_trims = VW_GOLF_VARIANT_MK7_PROFILE["preferred_trims"]
    acceptable_trims = VW_GOLF_VARIANT_MK7_PROFILE["acceptable_trims"]
    preferred_engines = VW_GOLF_VARIANT_MK7_PROFILE["preferred_engines"]
    acceptable_engines = VW_GOLF_VARIANT_MK7_PROFILE["acceptable_engines"]
    high_value_options = VW_GOLF_VARIANT_MK7_PROFILE["high_value_options"]
    risk_flags = VW_GOLF_VARIANT_MK7_PROFILE["risk_flags"]
    desirability = VW_GOLF_VARIANT_MK7_PROFILE["swedish_desirability_factors"]
    research_notes = VW_GOLF_VARIANT_MK7_PROFILE["research_notes"]
    buy_price = VW_GOLF_VARIANT_MK7_PROFILE["target_buy_price_eur"]
    sell_price = VW_GOLF_VARIANT_MK7_PROFILE["target_sell_price_sek"]

    return ModelResearch(
        brand="VW",
        model="Golf",
        variant="Variant",
        good_years=(
            f"Preferred {min(preferred_years)}-{max(preferred_years)}; "
            f"acceptable {min(acceptable_years)}-{max(acceptable_years)}; "
            f"preferred mileage {preferred_mileage['min']}-{preferred_mileage['max']} km; "
            f"acceptable mileage {acceptable_mileage['min']}-{acceptable_mileage['max']} km."
        ),
        strong_trims=[*preferred_trims, *preferred_engines, *high_value_options],
        weak_trims=[
            "very basic equipment",
            "manual gearbox unless priced aggressively",
            "weak engine/spec combination",
            *acceptable_trims,
            *acceptable_engines,
        ],
        common_issues="; ".join(risk_flags),
        swedish_demand_score=86,
        german_supply_score=84,
        liquidity_score=VW_GOLF_VARIANT_MK7_PROFILE["liquidity_score"],
        risk_notes=" ".join(
            [
                f"Risk score {VW_GOLF_VARIANT_MK7_PROFILE['risk_score']}; confidence score {VW_GOLF_VARIANT_MK7_PROFILE['confidence_score']}.",
                *desirability,
                *research_notes,
            ]
        ),
        target_buy_price_min=Decimal(str(buy_price["min"])),
        target_buy_price_max=Decimal(str(buy_price["max"])),
        target_sell_price_min=Decimal(str(sell_price["min"])),
        target_sell_price_max=Decimal(str(sell_price["max"])),
    )
