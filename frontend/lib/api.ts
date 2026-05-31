const API_BASE_URL =
  process.env.API_BASE_URL ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://localhost:8000";

export type Opportunity = {
  id: number;
  listing_id: number;
  source: string;
  listing_url: string | null;
  seller_country: string;
  seller_type: string;
  brand: string;
  model: string;
  variant: string | null;
  trim: string | null;
  year: number;
  mileage_km: number;
  fuel_type: string | null;
  transmission: string | null;
  price_eur: number;
  purchase_price_sek: number;
  estimated_swedish_price_sek: number;
  total_landed_cost_sek: number;
  expected_profit_sek: number;
  margin_percent: number;
  confidence_score: number;
  risk_score: number;
  liquidity_score: number;
  deal_grade: string;
  status: string;
  risk_flags: string[];
  explanation: string | null;
  created_at: string;
};

export type DashboardSummary = {
  cars_scanned_today: number;
  active_opportunities: number;
  average_expected_profit_sek: number;
  best_model_this_week: string | null;
  high_confidence_deals: number;
  best_opportunity: Opportunity | null;
};

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`Backend request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
  return getJson<DashboardSummary>("/api/dashboard");
}

export async function getOpportunities(): Promise<Opportunity[]> {
  return getJson<Opportunity[]>("/api/opportunities");
}
