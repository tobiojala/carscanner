"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState, useTransition } from "react";

import { calculateDeal, createListing } from "../lib/client-api";

type FormState = {
  brand: string;
  model: string;
  variant: string;
  trim: string;
  year: string;
  mileage_km: string;
  price_eur: string;
  estimated_swedish_price_sek: string;
  source: string;
  seller_type: string;
  fuel_type: string;
  transmission: string;
  service_history: string;
};

const initialState: FormState = {
  brand: "VW",
  model: "Golf",
  variant: "GTD",
  trim: "GTD DSG",
  year: "2018",
  mileage_km: "118000",
  price_eur: "15900",
  estimated_swedish_price_sek: "226000",
  source: "manual",
  seller_type: "dealer",
  fuel_type: "diesel",
  transmission: "automatic",
  service_history: "Full service history"
};

export function ManualListingForm() {
  const router = useRouter();
  const [form, setForm] = useState<FormState>(initialState);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  function updateField(field: keyof FormState, value: string) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage(null);
    setError(null);

    startTransition(async () => {
      try {
        const listing = await createListing({
          source: form.source || "manual",
          seller_country: "DE",
          seller_type: form.seller_type || "dealer",
          brand: form.brand,
          model: form.model,
          variant: form.variant || undefined,
          trim: form.trim || undefined,
          year: Number(form.year),
          mileage_km: Number(form.mileage_km),
          price_eur: Number(form.price_eur),
          fuel_type: form.fuel_type || undefined,
          transmission: form.transmission || undefined,
          service_history: form.service_history || undefined,
          description: "Manual listing added from the Phase 2 dashboard."
        });
        const opportunity = await calculateDeal(
          listing.id,
          Number(form.estimated_swedish_price_sek)
        );
        setMessage(
          `Added ${listing.brand} ${listing.model} and calculated ${Math.round(
            opportunity.expected_profit_sek
          ).toLocaleString("sv-SE")} SEK expected profit.`
        );
        router.refresh();
      } catch (caughtError) {
        setError(caughtError instanceof Error ? caughtError.message : "Unknown error");
      }
    });
  }

  return (
    <section className="form-card">
      <div className="table-header compact-header">
        <div>
          <h2>Add manual German listing</h2>
          <p>
            Step 1 MVP input: create a foreign listing and immediately calculate
            a mock deal from your Swedish resale estimate.
          </p>
        </div>
      </div>

      <form className="manual-form" onSubmit={onSubmit}>
        <label>
          Brand
          <input
            value={form.brand}
            onChange={(event) => updateField("brand", event.target.value)}
            required
          />
        </label>
        <label>
          Model
          <input
            value={form.model}
            onChange={(event) => updateField("model", event.target.value)}
            required
          />
        </label>
        <label>
          Variant
          <input
            value={form.variant}
            onChange={(event) => updateField("variant", event.target.value)}
          />
        </label>
        <label>
          Trim
          <input
            value={form.trim}
            onChange={(event) => updateField("trim", event.target.value)}
          />
        </label>
        <label>
          Year
          <input
            type="number"
            value={form.year}
            onChange={(event) => updateField("year", event.target.value)}
            required
          />
        </label>
        <label>
          Mileage km
          <input
            type="number"
            value={form.mileage_km}
            onChange={(event) => updateField("mileage_km", event.target.value)}
            required
          />
        </label>
        <label>
          German price EUR
          <input
            type="number"
            value={form.price_eur}
            onChange={(event) => updateField("price_eur", event.target.value)}
            required
          />
        </label>
        <label>
          Swedish estimate SEK
          <input
            type="number"
            value={form.estimated_swedish_price_sek}
            onChange={(event) =>
              updateField("estimated_swedish_price_sek", event.target.value)
            }
            required
          />
        </label>
        <label>
          Source
          <input
            value={form.source}
            onChange={(event) => updateField("source", event.target.value)}
          />
        </label>
        <label>
          Seller type
          <select
            value={form.seller_type}
            onChange={(event) => updateField("seller_type", event.target.value)}
          >
            <option value="dealer">Dealer</option>
            <option value="private">Private</option>
          </select>
        </label>
        <label>
          Fuel
          <input
            value={form.fuel_type}
            onChange={(event) => updateField("fuel_type", event.target.value)}
          />
        </label>
        <label>
          Transmission
          <input
            value={form.transmission}
            onChange={(event) => updateField("transmission", event.target.value)}
          />
        </label>
        <label className="wide-field">
          Service history
          <input
            value={form.service_history}
            onChange={(event) => updateField("service_history", event.target.value)}
          />
        </label>
        <button type="submit" disabled={isPending}>
          {isPending ? "Calculating..." : "Add listing and calculate deal"}
        </button>
      </form>

      {message ? <p className="form-message success-message">{message}</p> : null}
      {error ? <p className="form-message error-message">{error}</p> : null}
    </section>
  );
}
