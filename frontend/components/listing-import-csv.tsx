"use client";

import { useRouter } from "next/navigation";
import { ChangeEvent, useState, useTransition } from "react";

import { importListingsCsv } from "../lib/api";
import type { Opportunity } from "../lib/api";

const exportHeaders = [
  "id",
  "brand",
  "model",
  "variant",
  "year",
  "source",
  "seller_country",
  "seller_type",
  "price_eur",
  "purchase_price_sek",
  "estimated_swedish_price_sek",
  "total_landed_cost_sek",
  "expected_profit_sek",
  "margin_percent",
  "confidence_score",
  "risk_score",
  "liquidity_score",
  "deal_grade",
  "status",
  "reject_reason"
];

function csvEscape(value: unknown) {
  const stringValue = value === null || value === undefined ? "" : String(value);
  return `"${stringValue.replaceAll('"', '""')}"`;
}

export function CsvTools({ opportunities }: { opportunities: Opportunity[] }) {
  const router = useRouter();
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  function exportCsv() {
    const rows = opportunities.map((deal) =>
      exportHeaders.map((header) => csvEscape(deal[header as keyof Opportunity])).join(",")
    );
    const csv = [exportHeaders.join(","), ...rows].join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "car-arbitrage-deals.csv";
    link.click();
    URL.revokeObjectURL(url);
  }

  function importCsv(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }
    setMessage(null);
    setError(null);
    startTransition(async () => {
      try {
        const text = await file.text();
        const result = await importListingsCsv(text);
        setMessage(`Imported ${result.imported_count} listings.${result.errors?.length ? ` ${result.errors.length} rows had errors.` : ""}`);
        router.refresh();
      } catch (caughtError) {
        setError(caughtError instanceof Error ? caughtError.message : "Unknown error");
      } finally {
        event.target.value = "";
      }
    });
  }

  return (
    <section className="csv-tools-card">
      <div>
        <h2>CSV tools</h2>
        <p className="muted">
          Import German listing rows or export the currently filtered scanner view.
        </p>
      </div>
      <div className="csv-actions">
        <label className="csv-upload">
          {isPending ? "Importing..." : "Import listings CSV"}
          <input type="file" accept=".csv,text/csv" onChange={importCsv} disabled={isPending} />
        </label>
        <button type="button" onClick={exportCsv}>
          Export current deals CSV
        </button>
      </div>
      {message ? <p className="form-message success-message">{message}</p> : null}
      {error ? <p className="form-message error-message">{error}</p> : null}
    </section>
  );
}
