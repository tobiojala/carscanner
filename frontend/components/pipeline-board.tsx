"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";

import { updateDealStatus } from "../lib/client-api";
import type { Opportunity } from "../lib/api";

const statuses = [
  ["new", "New"],
  ["researching", "Researching"],
  ["contacted", "Contacted"],
  ["negotiating", "Negotiating"],
  ["bought", "Bought"],
  ["imported", "Imported"],
  ["listed_in_sweden", "Listed in Sweden"],
  ["sold", "Sold"],
  ["rejected", "Rejected"]
];

const sekFormatter = new Intl.NumberFormat("sv-SE", {
  style: "currency",
  currency: "SEK",
  maximumFractionDigits: 0
});

export function PipelineBoard({ opportunities }: { opportunities: Opportunity[] }) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  function moveDeal(dealId: number, status: string) {
    setError(null);
    startTransition(async () => {
      try {
        await updateDealStatus(dealId, status);
        router.refresh();
      } catch (caughtError) {
        setError(caughtError instanceof Error ? caughtError.message : "Unknown error");
      }
    });
  }

  return (
    <>
      {error ? <p className="form-message error-message">{error}</p> : null}
      <section className="pipeline-board" aria-busy={isPending}>
        {statuses.map(([status, label]) => {
          const deals = opportunities.filter((opportunity) => opportunity.status === status);
          return (
            <article className="pipeline-column" key={status}>
              <h2>{label}</h2>
              <p className="muted">{deals.length} deals</p>
              <div className="pipeline-cards">
                {deals.map((deal) => (
                  <div className="pipeline-card" key={deal.id}>
                    <Link className="vehicle detail-link" href={`/deals/${deal.id}`}>
                      {deal.brand} {deal.model}
                    </Link>
                    <p className="muted">
                      {deal.year} · {deal.trim ?? deal.variant ?? "Unknown trim"}
                    </p>
                    <p className="positive">{sekFormatter.format(deal.expected_profit_sek)}</p>
                    <select
                      value={deal.status}
                      onChange={(event) => moveDeal(deal.id, event.target.value)}
                      disabled={isPending}
                    >
                      {statuses.map(([value, statusLabel]) => (
                        <option key={value} value={value}>
                          {statusLabel}
                        </option>
                      ))}
                    </select>
                  </div>
                ))}
              </div>
            </article>
          );
        })}
      </section>
    </>
  );
}
