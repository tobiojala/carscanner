from pydantic import BaseModel, Field


class DealScoringInput(BaseModel):
    expected_profit_sek: float
    comparable_count: int = Field(ge=0)
    mileage_difference_km: int = Field(default=0, ge=0)
    year_difference: int = Field(default=0, ge=0)
    trim_matches: bool = True
    seller_type: str = "dealer"
    has_service_history: bool = True
    damaged: bool = False
    accident_history: bool = False
    missing_data_points: int = Field(default=0, ge=0)
    average_listing_age_days: int = Field(default=45, ge=0)
    model_popularity_score: int = Field(default=70, ge=0, le=100)


class DealScoringResult(BaseModel):
    profit_score: int
    confidence_score: int
    risk_score: int
    liquidity_score: int
    final_score: int
    deal_grade: str
    explanation: str
    risk_flags: list[str]


def _clamp(value: int, minimum: int = 0, maximum: int = 100) -> int:
    return max(minimum, min(maximum, value))


def _profit_score(expected_profit_sek: float) -> int:
    if expected_profit_sek < 0:
        return 0
    if expected_profit_sek >= 50_000:
        return 100
    if expected_profit_sek >= 30_000:
        return 80
    if expected_profit_sek >= 20_000:
        return 60
    if expected_profit_sek >= 10_000:
        return 40
    return 20


def _deal_grade(final_score: int, risk_score: int) -> str:
    if final_score >= 88 and risk_score <= 30:
        return "A+"
    if final_score >= 78 and risk_score <= 45:
        return "A"
    if final_score >= 62:
        return "B"
    if final_score >= 45:
        return "C"
    return "D"


def score_deal(input_data: DealScoringInput) -> DealScoringResult:
    risk_flags: list[str] = []

    profit_score = _profit_score(input_data.expected_profit_sek)

    confidence_score = 35
    confidence_score += min(input_data.comparable_count, 6) * 8
    confidence_score -= min(input_data.mileage_difference_km // 10_000, 4) * 5
    confidence_score -= min(input_data.year_difference, 5) * 5
    confidence_score -= input_data.missing_data_points * 4
    if input_data.trim_matches:
        confidence_score += 8
    else:
        confidence_score -= 12
        risk_flags.append("weak trim match")
    if input_data.seller_type.lower() == "dealer":
        confidence_score += 5
    if input_data.has_service_history:
        confidence_score += 8
    else:
        confidence_score -= 12
        risk_flags.append("missing service history")
    confidence_score = _clamp(confidence_score)

    risk_score = 20
    if input_data.damaged:
        risk_score += 35
        risk_flags.append("damaged car")
    if input_data.accident_history:
        risk_score += 25
        risk_flags.append("accident history")
    if not input_data.has_service_history:
        risk_score += 15
    if input_data.seller_type.lower() == "private":
        risk_score += 10
        risk_flags.append("private seller")
    if input_data.mileage_difference_km > 50_000:
        risk_score += 10
        risk_flags.append("large mileage difference to comps")
    if input_data.comparable_count < 2:
        risk_score += 15
        risk_flags.append("low number of Swedish comparables")
    if input_data.expected_profit_sek > 0 and profit_score <= 40:
        risk_score += 5
        risk_flags.append("thin profit buffer")
    risk_score = _clamp(risk_score)

    liquidity_score = input_data.model_popularity_score
    if input_data.comparable_count >= 5:
        liquidity_score += 10
    if input_data.average_listing_age_days <= 30:
        liquidity_score += 10
    elif input_data.average_listing_age_days >= 75:
        liquidity_score -= 15
    liquidity_score = _clamp(liquidity_score)

    final_score = round(
        profit_score * 0.4
        + confidence_score * 0.3
        + liquidity_score * 0.2
        + (100 - risk_score) * 0.1
    )
    final_score = _clamp(final_score)
    deal_grade = _deal_grade(final_score, risk_score)

    explanation = (
        f"Grade {deal_grade}: profit score {profit_score}, confidence "
        f"{confidence_score}, liquidity {liquidity_score}, risk {risk_score}."
    )

    return DealScoringResult(
        profit_score=profit_score,
        confidence_score=confidence_score,
        risk_score=risk_score,
        liquidity_score=liquidity_score,
        final_score=final_score,
        deal_grade=deal_grade,
        explanation=explanation,
        risk_flags=risk_flags,
    )
