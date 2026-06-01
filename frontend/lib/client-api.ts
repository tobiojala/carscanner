import {
  API_BASE_URL,
  type Comparable,
  type ComparableCreate,
  type CostSettings,
  type Listing,
  type LinkIntakeResponse,
  type ListingCreate,
  type Opportunity
} from "./api";

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
  status: string
): Promise<Opportunity> {
  return requestJson<Opportunity>(`/api/deals/${dealId}/status`, "PATCH", {
    status
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
