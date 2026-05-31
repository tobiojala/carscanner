export const API_BASE_URL =
  process.env.API_BASE_URL ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://localhost:8000";

export type LinkIntakeItem = {
  url: string;
  source: string;
  link_type: string;
  source_listing_id: string | null;
  seller_country: string | null;
  notes: string[];
};

export type LinkIntakeResponse = {
  items: LinkIntakeItem[];
};

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

export type CostSettings = {
  id: number;
  eur_to_sek_rate: number;
  default_transport_cost_sek: number;
  default_registration_cost_sek: number;
  default_inspection_cost_sek: number;
  default_repair_buffer_sek: number;
  default_tax_cost_sek: number;
  default_other_costs_sek: number;
  minimum_profit_threshold_sek: number;
  minimum_confidence_score: number;
  updated_at: string;
};

export type ModelResearch = {
  id: number;
  brand: string;
  model: string;
  variant: string | null;
  good_years: string | null;
  strong_trims: string[];
  weak_trims: string[];
  common_issues: string | null;
  swedish_demand_score: number;
  german_supply_score: number;
  liquidity_score: number;
  risk_notes: string | null;
  target_buy_price_min: number | null;
  target_buy_price_max: number | null;
  target_sell_price_min: number | null;
  target_sell_price_max: number | null;
  created_at: string;
  updated_at: string;
};

export type OpportunityFilters = {
  model?: string;
  min_profit_sek?: string;
  min_confidence?: string;
  source?: string;
  seller_type?: string;
  fuel_type?: string;
  transmission?: string;
  status_filter?: string;
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

export async function getOpportunities(
  filters: OpportunityFilters = {}
): Promise<Opportunity[]> {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value) {
      params.set(key, value);
    }
  });
  const query = params.toString();
  return getJson<Opportunity[]>(`/api/opportunities${query ? `?${query}` : ""}`);
}

export async function getDealDetail(dealId: number): Promise<DealDetail> {
  return getJson<DealDetail>(`/api/deals/${dealId}`);
}

export async function getSettings(): Promise<CostSettings> {
  return getJson<CostSettings>("/api/settings");
}

export async function getModelResearch(): Promise<ModelResearch[]> {
  return getJson<ModelResearch[]>("/api/model-research");
}
