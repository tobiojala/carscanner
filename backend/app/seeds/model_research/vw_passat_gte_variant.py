from decimal import Decimal
from typing import Any

from app.models import ModelResearch

VW_PASSAT_GTE_VARIANT_PROFILE: dict[str, Any] = {
    "brand": "Volkswagen",
    "model": "Passat GTE Variant",
    "generation": "B8 / B8 facelift",
    "target_market": "Sweden",
    "preferred_years": [2018, 2019, 2020, 2021, 2022],
    "acceptable_years": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    "preferred_mileage_range": {"min": 60000, "max": 150000},
    "acceptable_mileage_range": {"min": 30000, "max": 210000},
    "preferred_colors": ["black", "grey", "silver", "white"],
    "weak_colors": ["brown", "red", "gold", "green", "unusual wrap colors"],
    "preferred_trims": [
        "GTE",
        "GTE Executive",
        "GTE Advance",
        "facelift GTE Variant",
        "well-equipped company lease return",
    ],
    "acceptable_trims": [
        "standard GTE Variant",
        "Business",
        "Comfortline with strong equipment",
        "Highline with GTE package",
    ],
    "high_value_options": [
        "DSG automatic",
        "Digital Cockpit",
        "adaptive cruise control",
        "tow hitch",
        "panoramic roof",
        "Matrix LED headlights",
        "LED headlights",
        "heated seats",
        "rear camera",
        "Navigation Discover Pro",
        "parking sensors",
        "keyless entry",
        "electric tailgate",
        "winter wheels",
        "complete charging cable set",
        "full VW service history",
        "one-owner company car history",
    ],
    "risk_flags": [
        "missing charging cable",
        "missing service history",
        "poor battery documentation",
        "reported battery issues",
        "accident history",
        "high owner count",
        "imported multiple times",
        "mileage above 220000 km",
        "incomplete charging equipment",
        "unexplained hybrid system warning",
        "DSG service uncertainty",
        "suspiciously low price",
        "weak equipment level",
        "unusual color",
    ],
    "swedish_desirability_factors": [
        "Variant wagon body style is highly practical for Swedish family buyers.",
        "Plug-in hybrid drivetrain has strong Swedish demand when battery condition is credible.",
        "Neutral colors improve liquidity and reduce resale friction.",
        "2018+ and especially facelift cars can command a resale premium.",
        "DSG automatic is expected and supports resale appeal.",
        "Digital Cockpit, adaptive cruise, LED or Matrix headlights, and Discover Pro navigation signal a higher equipment level.",
        "Tow hitch and winter wheels improve practicality in Sweden.",
        "One-owner company lease returns can be attractive if service history is complete.",
        "Complete charging cables reduce buyer uncertainty.",
        "Full VW service history is important for confidence and pricing.",
    ],
    "liquidity_score": 88,
    "risk_score": 44,
    "confidence_score": 70,
    "target_buy_price_eur": {"min": 17500, "max": 25500},
    "target_sell_price_sek": {"min": 270000, "max": 315000},
    "battery_risk_notes": [
        "Battery condition and charging history should be verified before assigning a high confidence score.",
        "Missing charging cable is a meaningful negative signal and should reduce both confidence and expected resale value.",
        "Poor battery documentation increases uncertainty even if the vehicle drives normally.",
        "Check remaining battery or hybrid-system warranty where possible.",
        "High mileage plug-in hybrids should be discounted conservatively due to battery and drivetrain uncertainty.",
        "Facelift models may justify higher purchase prices only when battery documentation and service history are strong.",
    ],
    "research_notes": [
        "Use conservative resale estimates because Swedish buyers will heavily discount unclear battery condition or incomplete charging equipment.",
        "Best candidates are neutral-color GTE Variant cars with DSG, full VW service history, complete charging cables, adaptive cruise, Digital Cockpit, and LED or Matrix headlights.",
        "Company lease returns can be attractive if ownership, service, and charging equipment are well documented.",
        "Avoid cars above 220000 km unless purchase price is very low and hybrid system history is unusually clear.",
        "The search filters indicate Germany-only, non-damaged, wagon body, hybrid drivetrain, neutral colors, and mileage capped around 200000 km.",
        "2018+ cars should generally be preferred over earlier B8 examples due to buyer perception and stronger liquidity.",
        "Facelift cars can carry a Swedish resale premium but must still leave room for import costs, repair buffer, and minimum desired profit.",
        "Manual validation should compare against Swedish Passat GTE Variant listings with similar year, mileage, trim, battery documentation, and equipment level.",
    ],
}


def build_vw_passat_gte_variant_seed() -> ModelResearch:
    preferred_years = VW_PASSAT_GTE_VARIANT_PROFILE["preferred_years"]
    acceptable_years = VW_PASSAT_GTE_VARIANT_PROFILE["acceptable_years"]
    preferred_mileage = VW_PASSAT_GTE_VARIANT_PROFILE["preferred_mileage_range"]
    acceptable_mileage = VW_PASSAT_GTE_VARIANT_PROFILE["acceptable_mileage_range"]
    preferred_trims = VW_PASSAT_GTE_VARIANT_PROFILE["preferred_trims"]
    acceptable_trims = VW_PASSAT_GTE_VARIANT_PROFILE["acceptable_trims"]
    high_value_options = VW_PASSAT_GTE_VARIANT_PROFILE["high_value_options"]
    risk_flags = VW_PASSAT_GTE_VARIANT_PROFILE["risk_flags"]
    battery_notes = VW_PASSAT_GTE_VARIANT_PROFILE["battery_risk_notes"]
    desirability = VW_PASSAT_GTE_VARIANT_PROFILE["swedish_desirability_factors"]
    research_notes = VW_PASSAT_GTE_VARIANT_PROFILE["research_notes"]
    buy_price = VW_PASSAT_GTE_VARIANT_PROFILE["target_buy_price_eur"]
    sell_price = VW_PASSAT_GTE_VARIANT_PROFILE["target_sell_price_sek"]

    return ModelResearch(
        brand="VW",
        model="Passat GTE",
        variant="Variant",
        good_years=(
            f"Preferred {min(preferred_years)}-{max(preferred_years)}; "
            f"acceptable {min(acceptable_years)}-{max(acceptable_years)}; "
            f"preferred mileage {preferred_mileage['min']}-{preferred_mileage['max']} km; "
            f"acceptable mileage {acceptable_mileage['min']}-{acceptable_mileage['max']} km."
        ),
        strong_trims=[*preferred_trims, *high_value_options],
        weak_trims=[
            "low equipment level",
            "missing charging cable",
            "poor battery documentation",
            "mileage above 220000 km",
            *acceptable_trims,
        ],
        common_issues="; ".join([*risk_flags, *battery_notes]),
        swedish_demand_score=90,
        german_supply_score=78,
        liquidity_score=VW_PASSAT_GTE_VARIANT_PROFILE["liquidity_score"],
        risk_notes=" ".join(
            [
                f"Risk score {VW_PASSAT_GTE_VARIANT_PROFILE['risk_score']}; confidence score {VW_PASSAT_GTE_VARIANT_PROFILE['confidence_score']}.",
                *desirability,
                *battery_notes,
                *research_notes,
            ]
        ),
        target_buy_price_min=Decimal(str(buy_price["min"])),
        target_buy_price_max=Decimal(str(buy_price["max"])),
        target_sell_price_min=Decimal(str(sell_price["min"])),
        target_sell_price_max=Decimal(str(sell_price["max"])),
    )
