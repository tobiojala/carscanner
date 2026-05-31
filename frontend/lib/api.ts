const API_BASE_URL =
  process.env.API_BASE_URL ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://localhost:8000";

export type Opportunity = {
  id: number;
  year: number;
  make: string;
  model: string;
  trim: string | null;
  source_market: string;
  target_market: string;
  asking_price: number;
  estimated_market_price: number;
  mileage: number;
  estimated_spread: number;
  created_at: string;
};

export type DashboardSummary = {
  total_listings: number;
  average_spread: number;
  best_spread: number;
  best_listing: Opportunity | null;
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
