"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState, useTransition } from "react";

import { updateSettings } from "../lib/api";
import type { CostSettings } from "../lib/api";

const fields: Array<[keyof CostSettings, string]> = [
  ["eur_to_sek_rate", "EUR/SEK rate"],
  ["default_transport_cost_sek", "Transport cost SEK"],
  ["default_registration_cost_sek", "Registration cost SEK"],
  ["default_inspection_cost_sek", "Inspection cost SEK"],
  ["default_repair_buffer_sek", "Repair buffer SEK"],
  ["default_tax_cost_sek", "Tax cost SEK"],
  ["default_other_costs_sek", "Other costs SEK"],
  ["minimum_profit_threshold_sek", "Minimum profit SEK"],
  ["minimum_confidence_score", "Minimum confidence score"]
];

export function SettingsForm({ settings }: { settings: CostSettings }) {
  const router = useRouter();
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage(null);
    setError(null);
    const formData = new FormData(event.currentTarget);
    const payload: Partial<CostSettings> = {};
    fields.forEach(([field]) => {
      const value = formData.get(field);
      if (typeof value === "string" && value !== "") {
        payload[field] = Number(value) as never;
      }
    });

    startTransition(async () => {
      try {
        await updateSettings(payload);
        setMessage("Settings saved. New calculations will use these assumptions.");
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
          <h2>Cost assumptions</h2>
          <p>These values feed manual deal calculations.</p>
        </div>
      </div>
      <form className="manual-form" onSubmit={onSubmit}>
        {fields.map(([field, label]) => (
          <label key={field}>
            {label}
            <input
              name={field}
              type="number"
              step={field === "eur_to_sek_rate" ? "0.01" : "1"}
              defaultValue={settings[field] as number}
            />
          </label>
        ))}
        <button type="submit" disabled={isPending}>
          {isPending ? "Saving..." : "Save settings"}
        </button>
      </form>
      {message ? <p className="form-message success-message">{message}</p> : null}
      {error ? <p className="form-message error-message">{error}</p> : null}
    </section>
  );
}
