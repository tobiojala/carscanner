from decimal import Decimal

from pydantic import BaseModel, Field


class ActualOutcomeInput(BaseModel):
    actual_purchase_price_sek: Decimal = Field(ge=0)
    actual_transport_cost_sek: Decimal = Field(ge=0)
    actual_registration_cost_sek: Decimal = Field(ge=0)
    actual_repair_cost_sek: Decimal = Field(ge=0)
    actual_sale_price_sek: Decimal | None = Field(default=None, ge=0)


class ActualOutcomeResult(BaseModel):
    actual_total_cost_sek: Decimal
    actual_profit_sek: Decimal | None


def calculate_actual_outcome(input_data: ActualOutcomeInput) -> ActualOutcomeResult:
    total_cost = (
        input_data.actual_purchase_price_sek
        + input_data.actual_transport_cost_sek
        + input_data.actual_registration_cost_sek
        + input_data.actual_repair_cost_sek
    )
    actual_profit = None
    if input_data.actual_sale_price_sek is not None:
        actual_profit = input_data.actual_sale_price_sek - total_cost

    return ActualOutcomeResult(
        actual_total_cost_sek=total_cost,
        actual_profit_sek=actual_profit,
    )
