"use client";
// Renamed from: components/compare/DealsTableWithCompare.tsx
// Moved to:     components/deals-table.tsx
//
// This is the deals list with checkbox-based compare selection.
// Compare subfolder is for compare-specific components only.

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

// Re-use whatever type your api.ts exports for opportunities
// Adjust the import path if your type is named differently
import type { CompareDealItem } from "../lib/api";

interface Props {
  opportunities: CompareDealItem[];
  sekFormatter: Intl.NumberFormat;
  eurFormatter: Intl.NumberFormat;
}

export function DealsTable({ opportunities, sekFormatter, eurFormatter }: Props) {
  const router = useRouter();
  const [selected, setSelected] = useState<Set<number>>(new Set());

  function toggle(id: number) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else if (next.size < 4) next.add(id);
      return next;
    });
  }

  function goCompare() {
    router.push(`/compare?ids=${Array.from(selected).join(",")}`);
  }

  if (opportunities.length === 0) {
    return (
      <div className="empty-state">
        No deals found for this filter.
      </div>
    );
  }

  return (
    <div className="deals-table-root">
      {/* Sticky compare bar — appears when 2+ selected */}
      {selected.size >= 2 && (
        <div className="compare-bar">
          <span>{selected.size} deals selected</span>
          <div className="compare-bar-actions">
            <button onClick={() => setSelected(new Set())} className="compare-bar-clear">
              Clear
            </button>
            <button onClick={goCompare} className="compare-bar-cta">
              Compare {selected.size} deals →
            </button>
          </div>
        </div>
      )}

      <table className="deals-table">
        <thead>
          <tr>
            <th className="col-check" />
            <th className="col-score">Score</th>
            <th className="col-car">Car</th>
            <th className="col-source">Source</th>
            <th className="col-price">Buy price</th>
            <th className="col-profit">Est. profit</th>
            <th className="col-margin">Margin</th>
            <th className="col-stage">Stage</th>
          </tr>
        </thead>
        <tbody>
          {opportunities.map((deal) => {
            const isSelected = selected.has(deal.id);
            const isDisabled = !isSelected && selected.size >= 4;
            const profitPositive = deal.expected_profit_sek >= 0;

            return (
              <tr
                key={deal.id}
                className={`deal-row ${isSelected ? "deal-row-selected" : ""} ${isDisabled ? "deal-row-disabled" : ""}`}
              >
                <td className="col-check">
                  <input
                    type="checkbox"
                    checked={isSelected}
                    disabled={isDisabled}
                    onChange={() => toggle(deal.id)}
                    aria-label={`Select ${deal.title}`}
                  />
                </td>

                <td className="col-score">
                  <span className={`score-badge score-${scoreLevel(deal.confidence_score)}`}>
                    {deal.confidence_score}
                  </span>
                </td>

                <td className="col-car">
                  <Link href={`/deals/${deal.id}`}>
                    <span className="deal-title">{deal.title}</span>
                    <span className="deal-meta">
                      {deal.year} · {deal.mileage_km.toLocaleString("sv-SE")} km
                    </span>
                  </Link>
                </td>

                <td className="col-source">
                  <span className="source-tag">{deal.source}</span>
                </td>

                <td className="col-price">
                  {eurFormatter.format(deal.price_eur)}
                </td>

                <td className={`col-profit ${profitPositive ? "profit-pos" : "profit-neg"}`}>
                  {sekFormatter.format(deal.expected_profit_sek)}
                </td>

                <td className="col-margin">
                  {deal.margin_percent.toFixed(1)}%
                </td>

                <td className="col-stage">
                  <span className={`stage-pill stage-${deal.stage ?? "new"}`}>
                    {deal.stage ?? "new"}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function scoreLevel(score: number): "high" | "mid" | "low" {
  if (score >= 70) return "high";
  if (score >= 50) return "mid";
  return "low";
}
