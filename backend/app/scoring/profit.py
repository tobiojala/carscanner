"""
Car Arbitrage Scanner
Copyright (c) 2026 Tobias Bergmark
All rights reserved.
"""
from decimal import Decimal, ROUND_HALF_UP

from pydantic import BaseModel, Field

MONEY_QUANT = Decimal("0.01")
PERCENT_QUANT = Decimal("0.01")


class ProfitCalculationInput(BaseModel):
    purchase_price_eur: Decimal = Field(ge=0)
    eur_to_sek_rate: Decimal = Field(gt=0)
    estimated_swedish_price_sek: Decimal = Field(ge=0)
    transport_cost_sek: Decimal = Field(default=Decimal("8000"), ge=0)
    registration_cost_sek: Decimal = Field(default=Decimal("4000"), ge=0)
    inspection_cost_sek: Decimal = Field(default=Decimal("2500"), ge=0)
    repair_buffer_sek: Decimal = Field(default=Decimal("10000"), ge=0)
    tax_cost_sek: Decimal = Field(default=Decimal("0"), ge=0)
    other_costs_sek: Decimal = Field(default=Decimal("3000"), ge=0)
    desired_profit_sek: Decimal = Field(default=Decimal("20000"), ge=0)


class ProfitCalculationResult(BaseModel):
    purchase_price_sek: Decimal
    total_landed_cost_sek: Decimal
    expected_profit_sek: Decimal
    margin_percent: Decimal
    break_even_price_sek: Decimal
    recommended_max_bid_eur: Decimal


def _money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)


def _percent(value: Decimal) -> Decimal:
    return value.quantize(PERCENT_QUANT, rounding=ROUND_HALF_UP)


def calculate_profit(input_data: ProfitCalculationInput) -> ProfitCalculationResult:
    purchase_price_sek = _money(input_data.purchase_price_eur * input_data.eur_to_sek_rate)
    side_costs_sek = (
        input_data.transport_cost_sek
        + input_data.registration_cost_sek
        + input_data.inspection_cost_sek
        + input_data.repair_buffer_sek
        + input_data.tax_cost_sek
        + input_data.other_costs_sek
    )
    total_landed_cost_sek = _money(purchase_price_sek + side_costs_sek)
    expected_profit_sek = _money(
        input_data.estimated_swedish_price_sek - total_landed_cost_sek
    )
    margin_percent = Decimal("0")
    if total_landed_cost_sek > 0:
        margin_percent = _percent(expected_profit_sek / total_landed_cost_sek * 100)

    recommended_max_bid_eur = _money(
        (
            input_data.estimated_swedish_price_sek
            - input_data.desired_profit_sek
            - side_costs_sek
        )
        / input_data.eur_to_sek_rate
    )

    return ProfitCalculationResult(
        purchase_price_sek=purchase_price_sek,
        total_landed_cost_sek=total_landed_cost_sek,
        expected_profit_sek=expected_profit_sek,
        margin_percent=margin_percent,
        break_even_price_sek=total_landed_cost_sek,
        recommended_max_bid_eur=recommended_max_bid_eur,
    )
