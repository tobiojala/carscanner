export const API_BASE_URL =
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

export type Comparable = {
  id: number;
  source: string;
  listing_url: string | null;
  brand: string;
  model: string;
  variant: string | null;
  year: number;
  mileage_km: number | null;
  fuel_type: string | null;
  transmission: string | null;
  trim: string | null;
  price_sek: number;
  location: string | null;
  seller_type: string | null;
  listing_age_days: number | null;
  created_at: string;
};

export type Listing = {
  id: number;
  source: string;
  source_listing_id: string;
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
  body_type: string | null;
  price_eur: number;
  currency: string;
  vat_deductible: boolean;
  damaged: boolean;
  service_history: string | null;
  scraped_at: string;
  created_at: string;
};

export type ListingCreate = {
  source?: string;
  source_listing_id?: string;
  listing_url?: string;
  seller_country?: string;
  seller_type?: string;
  brand: string;
  model: string;
  variant?: string;
  trim?: string;
  year: number;
  mileage_km: number;
  fuel_type?: string;
  transmission?: string;
  body_type?: string;
  price_eur: number;
  vat_deductible?: boolean;
  damaged?: boolean;
  service_history?: string;
  description?: string;
};

export type CostBreakdown = {
  purchase_price_sek: number;
  transport_cost_sek: number;
  registration_cost_sek: number;
  inspection_cost_sek: number;
  repair_buffer_sek: number;
  tax_cost_sek: number;
  other_costs_sek: number;
  total_landed_cost_sek: number;
};

export type DealDetail = {
  opportunity: Opportunity;
  listing: Listing;
  cost_breakdown: CostBreakdown;
  comparables: Comparable[];
  notes: string | null;
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

export async function getDealDetail(dealId: number): Promise<DealDetail> {
  return getJson<DealDetail>(`/api/deals/${dealId}`);
}
