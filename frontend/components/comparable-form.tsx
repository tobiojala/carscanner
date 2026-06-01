"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState, useTransition } from "react";

import { createComparable } from "../lib/client-api";

type ComparableFormDefaults = {
  brand?: string;
  model?: string;
  variant?: string | null;
  year?: number;
  fuel_type?: string | null;
  transmission?: string | null;
  trim?: string | null;
};

type ComparableFormProps = {
  defaults?: ComparableFormDefaults;
  compact?: boolean;
};

export function ComparableForm({ defaults = {}, compact = false }: ComparableFormProps) {
  const router = useRouter();
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage(null);
    setError(null);
    const formData = new FormData(event.currentTarget);

    const value = (field: string) => String(formData.get(field) ?? "").trim();
    const optionalNumber = (field: string) => {
      const rawValue = value(field);
      return rawValue ? Number(rawValue) : undefined;
    };

    startTransition(async () => {
      try {
        const comparable = await createComparable({
          source: value("source") || "manual",
          listing_url: value("listing_url") || undefined,
          brand: value("brand"),
          model: value("model"),
          variant: value("variant") || undefined,
          year: Number(value("year")),
          mileage_km: optionalNumber("mileage_km"),
          fuel_type: value("fuel_type") || undefined,
          transmission: value("transmission") || undefined,
          trim: value("trim") || undefined,
          price_sek: Number(value("price_sek")),
          location: value("location") || undefined,
          seller_type: value("seller_type") || undefined,
          listing_age_days: optionalNumber("listing_age_days")
        });
        setMessage(
          `Added comparable ${comparable.year} ${comparable.brand} ${comparable.model}.`
        );
        event.currentTarget.reset();
        router.refresh();
      } catch (caughtError) {
        setError(caughtError instanceof Error ? caughtError.message : "Unknown error");
      }
    });
  }

  return (
    <section className={compact ? "inline-form-card" : "form-card"}>
      <div className="table-header compact-header">
        <div>
          <h2>Add Swedish comparable</h2>
          <p>
            Enter Blocket or Bytbil comps manually. Matching brand/model comps
            appear on deal detail pages and improve future scoring confidence.
          </p>
        </div>
      </div>
      <form className="manual-form" onSubmit={onSubmit}>
        <label>
          Source
          <input name="source" defaultValue="manual" />
        </label>
        <label>
          Listing URL
          <input name="listing_url" placeholder="https://www.blocket.se/..." />
        </label>
        <label>
          Brand
          <input name="brand" defaultValue={defaults.brand ?? ""} required />
        </label>
        <label>
          Model
          <input name="model" defaultValue={defaults.model ?? ""} required />
        </label>
        <label>
          Variant
          <input name="variant" defaultValue={defaults.variant ?? ""} />
        </label>
        <label>
          Trim
          <input name="trim" defaultValue={defaults.trim ?? ""} />
        </label>
        <label>
          Year
          <input name="year" type="number" defaultValue={defaults.year ?? ""} required />
        </label>
        <label>
          Mileage km
          <input name="mileage_km" type="number" />
        </label>
        <label>
          Fuel
          <input name="fuel_type" defaultValue={defaults.fuel_type ?? ""} />
        </label>
        <label>
          Transmission
          <input name="transmission" defaultValue={defaults.transmission ?? ""} />
        </label>
        <label>
          Price SEK
          <input name="price_sek" type="number" required />
        </label>
        <label>
          Location
          <input name="location" placeholder="Stockholm" />
        </label>
        <label>
          Seller type
          <select name="seller_type" defaultValue="dealer">
            <option value="dealer">Dealer</option>
            <option value="private">Private</option>
          </select>
        </label>
        <label>
          Listing age days
          <input name="listing_age_days" type="number" />
        </label>
        <button type="submit" disabled={isPending}>
          {isPending ? "Saving..." : "Add comparable"}
        </button>
      </form>
      {message ? <p className="form-message success-message">{message}</p> : null}
      {error ? <p className="form-message error-message">{error}</p> : null}
    </section>
  );
}
