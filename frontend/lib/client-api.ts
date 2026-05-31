import { API_BASE_URL, type Listing, type ListingCreate, type Opportunity } from "./api";

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
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
  return postJson<Listing>("/api/listings", payload);
}

export async function calculateDeal(
  listingId: number,
  estimatedSwedishPriceSek: number
): Promise<Opportunity> {
  return postJson<Opportunity>("/api/deals/calculate", {
    listing_id: listingId,
    estimated_swedish_price_sek: estimatedSwedishPriceSek
  });
}
