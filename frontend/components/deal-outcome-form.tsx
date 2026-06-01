"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState, useTransition } from "react";

import { updateActualOutcome } from "../lib/client-api";
import type { ActualOutcome } from "../lib/api";

const fields: Array<[keyof ActualOutcome, string]> = [
  ["actual_purchase_price_sek", "Actual purchase SEK"],
  ["actual_transport_cost_sek", "Actual transport SEK"],
  ["actual_registration_cost_sek", "Actual registration SEK"],
  ["actual_repair_cost_sek", "Actual repair SEK"],
  ["actual_sale_price_sek", "Actual sale SEK"],
  ["days_to_sell", "Days to sell"]
];

export function DealOutcomeForm({
  dealId,
  outcome
}: {
  dealId: number;
  outcome: ActualOutcome;
}) {
  const router = useRouter();
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setMessage(null);
    const formData = new FormData(event.currentTarget);
    const payload: Partial<ActualOutcome> = {};

    fields.forEach(([field]) => {
      const value = formData.get(field);
      if (typeof value === "string" && value !== "") {
        payload[field] = Number(value) as never;
      }
    });
    const lesson = formData.get("lesson_learned");
    if (typeof lesson === "string") {
      payload.lesson_learned = lesson;
    }

    startTransition(async () => {
      try {
        await updateActualOutcome(dealId, payload);
        setMessage("Actual outcome saved.");
        router.refresh();
      } catch (caughtError) {
        setError(caughtError instanceof Error ? caughtError.message : "Unknown error");
      }
    });
  }

  return (
    <section className="detail-card wide-detail-card">
      <h2>Actual outcome</h2>
      <p className="detail-copy">
        Track real purchase, import, repair, sale, and learning data once the
        deal moves beyond research.
      </p>
      <form className="actual-outcome-form" onSubmit={onSubmit}>
        {fields.map(([field, label]) => (
          <label key={field}>
            {label}
            <input
              name={field}
              type="number"
              defaultValue={outcome[field] ?? ""}
            />
          </label>
        ))}
        <label className="actual-wide-field">
          Lesson learned
          <textarea
            name="lesson_learned"
            rows={3}
            defaultValue={outcome.lesson_learned ?? ""}
          />
        </label>
        <button type="submit" disabled={isPending}>
          {isPending ? "Saving..." : "Save actual outcome"}
        </button>
      </form>
      {outcome.actual_total_cost_sek !== null ? (
        <p className="form-message success-message">
          Actual total cost: {Math.round(outcome.actual_total_cost_sek).toLocaleString("sv-SE")} SEK
          {outcome.actual_profit_sek !== null
            ? ` · Actual profit: ${Math.round(outcome.actual_profit_sek).toLocaleString("sv-SE")} SEK`
            : ""}
        </p>
      ) : null}
      {message ? <p className="form-message success-message">{message}</p> : null}
      {error ? <p className="form-message error-message">{error}</p> : null}
    </section>
  );
}
