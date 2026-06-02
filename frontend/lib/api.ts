/*
 * Car Arbitrage Scanner
 * Copyright (c) 2026 Tobias Bergmark
 * All rights reserved.
 */
import { API_BASE_URL } from "./types";
import type { ActualOutcome, Comparable, ComparableCreate, CompareDealsResponse, CostSettings, DashboardSummary, DealDetail, LinkIntakeResponse, Listing, ListingCreate, ModelResearch, Opportunity, OpportunityFilters } from "./types";

async function requestJson<T>(
  path: string,
  method: "POST" | "PATCH",
  body: unknown
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Backend request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function createListing(payload: ListingCreate): Promise<Listing> {
  return requestJson<Listing>("/api/listings", "POST", payload);
}

export async function calculateDeal(
  listingId: number,
  estimatedSwedishPriceSek: number
): Promise<Opportunity> {
  return requestJson<Opportunity>("/api/deals/calculate", "POST", {
    listing_id: listingId,
    estimated_swedish_price_sek: estimatedSwedishPriceSek
  });
}

export async function updateDealStatus(
  dealId: number,
  status: string,
  rejectReason?: string,
  rejectNotes?: string
): Promise<Opportunity> {
  return requestJson<Opportunity>(`/api/deals/${dealId}/status`, "PATCH", {
    status,
    reject_reason: rejectReason,
    reject_notes: rejectNotes
  });
}

export async function updateSettings(
  payload: Partial<CostSettings>
): Promise<CostSettings> {
  return requestJson<CostSettings>("/api/settings", "PATCH", payload);
}

export async function previewLinks(urls: string[]): Promise<LinkIntakeResponse> {
  return requestJson<LinkIntakeResponse>("/api/link-intake/preview", "POST", {
    urls
  });
}

export async function createComparable(
  payload: ComparableCreate
): Promise<Comparable> {
  return requestJson<Comparable>("/api/comparables", "POST", payload);
}

export async function updateActualOutcome(
  dealId: number,
  payload: Partial<ActualOutcome>
): Promise<DealDetail> {
  return requestJson<DealDetail>(`/api/deals/${dealId}/actual-outcome`, "PATCH", payload);
}

export async function importListingsCsv(csvText: string) {
  const response = await fetch(`${API_BASE_URL}/api/listings/import-csv`, {
    method: "POST",
    headers: {
      "Content-Type": "text/csv"
    },
    body: csvText
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Backend request failed: ${response.status}`);
  }

  return response.json();
}


// Server-side fetch functions (used by App Router server components)
async function serverFetch<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to fetch ${path}: ${res.status}`);
  return res.json() as Promise<T>;
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
  return serverFetch<DashboardSummary>("/api/dashboard");
}

export async function getOpportunities(filters?: OpportunityFilters): Promise<Opportunity[]> {
  const params = new URLSearchParams();
  if (filters?.model) params.set("model", filters.model);
  if (filters?.min_profit_sek) params.set("min_profit_sek", String(filters.min_profit_sek));
  if (filters?.min_confidence) params.set("min_confidence", String(filters.min_confidence));
  if (filters?.source) params.set("source", filters.source);
  if (filters?.seller_type) params.set("seller_type", filters.seller_type);
  if (filters?.fuel_type) params.set("fuel_type", filters.fuel_type);
  if (filters?.transmission) params.set("transmission", filters.transmission);
  if (filters?.status_filter) params.set("status_filter", filters.status_filter);
  const qs = params.toString();
  return serverFetch<Opportunity[]>(`/api/opportunities${qs ? `?${qs}` : ""}`);
}

export async function getDealDetail(dealId: number): Promise<DealDetail> {
  return serverFetch<DealDetail>(`/api/deals/${dealId}`);
}

export async function getSettings(): Promise<CostSettings> {
  return serverFetch<CostSettings>("/api/settings");
}

export async function getModelResearch(): Promise<ModelResearch[]> {
  return serverFetch<ModelResearch[]>("/api/model-research");
}

export async function getComparables(): Promise<Comparable[]> {
  return serverFetch<Comparable[]>("/api/comparables");
}

export async function compareDeals(dealIds: number[]): Promise<CompareDealsResponse> {
  const res = await fetch(`${API_BASE_URL}/api/compare/deals`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ deal_ids: dealIds }),
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`Compare failed: ${res.status}`);
  return res.json() as Promise<CompareDealsResponse>;
}
