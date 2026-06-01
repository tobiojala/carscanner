from decimal import Decimal
import unittest

from fastapi import HTTPException

from app.scoring import (
    ActualOutcomeInput,
    DealScoringInput,
    ProfitCalculationInput,
    calculate_actual_outcome,
    calculate_profit,
    score_deal,
)
from app.services.listing_service import import_listings_csv


class ProfitCalculationTests(unittest.TestCase):
    def test_calculates_profit_and_max_bid(self) -> None:
        result = calculate_profit(
            ProfitCalculationInput(
                purchase_price_eur=Decimal("15000"),
                eur_to_sek_rate=Decimal("11"),
                estimated_swedish_price_sek=Decimal("230000"),
                tax_cost_sek=Decimal("5000"),
            )
        )

        self.assertEqual(result.purchase_price_sek, Decimal("165000.00"))
        self.assertEqual(result.total_landed_cost_sek, Decimal("197500.00"))
        self.assertEqual(result.expected_profit_sek, Decimal("32500.00"))
        self.assertEqual(result.margin_percent, Decimal("16.46"))
        self.assertEqual(result.recommended_max_bid_eur, Decimal("16136.36"))


class DealScoringTests(unittest.TestCase):
    def test_scores_profitable_low_risk_deal(self) -> None:
        result = score_deal(
            DealScoringInput(
                expected_profit_sek=52_000,
                comparable_count=5,
                mileage_difference_km=8_000,
                year_difference=1,
                trim_matches=True,
                seller_type="dealer",
                has_service_history=True,
                model_popularity_score=85,
            )
        )

        self.assertEqual(result.profit_score, 100)
        self.assertIn(result.deal_grade, {"A+", "A"})
        self.assertLessEqual(result.risk_score, 30)

    def test_confidence_explanation_tracks_factors(self) -> None:
        result = score_deal(
            DealScoringInput(
                expected_profit_sek=12_000,
                comparable_count=1,
                mileage_difference_km=65_000,
                year_difference=3,
                trim_matches=False,
                seller_type="private",
                has_service_history=False,
                missing_data_points=2,
            )
        )

        self.assertEqual(result.confidence_explanation.score, result.confidence_score)
        self.assertIn("Trim match uncertain", result.confidence_explanation.negative_factors)
        self.assertIn("Service history missing or incomplete", result.confidence_explanation.missing_data)
        self.assertEqual(result.confidence_explanation.comparable_count, 1)


class ActualOutcomeTests(unittest.TestCase):
    def test_calculates_actual_profit_when_sale_price_exists(self) -> None:
        result = calculate_actual_outcome(
            ActualOutcomeInput(
                actual_purchase_price_sek=Decimal("200000"),
                actual_transport_cost_sek=Decimal("8000"),
                actual_registration_cost_sek=Decimal("4000"),
                actual_repair_cost_sek=Decimal("12000"),
                actual_sale_price_sek=Decimal("245000"),
            )
        )

        self.assertEqual(result.actual_total_cost_sek, Decimal("224000"))
        self.assertEqual(result.actual_profit_sek, Decimal("21000"))


class CsvImportValidationTests(unittest.TestCase):
    def test_csv_import_requires_expected_columns(self) -> None:
        with self.assertRaises(HTTPException) as error:
            import_listings_csv(None, "brand,model\nBMW,320d")  # type: ignore[arg-type]

        self.assertEqual(error.exception.status_code, 422)
        self.assertIn("Missing required columns", str(error.exception.detail))


if __name__ == "__main__":
    unittest.main()
