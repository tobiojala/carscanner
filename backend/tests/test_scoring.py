from decimal import Decimal
import unittest

from app.scoring import DealScoringInput, ProfitCalculationInput, calculate_profit, score_deal


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


if __name__ == "__main__":
    unittest.main()
