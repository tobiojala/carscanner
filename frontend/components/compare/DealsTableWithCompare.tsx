"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

import type { Opportunity } from "../../lib/api";

const sekFormatter = new Intl.NumberFormat("sv-SE", {
  style: "currency",
  currency: "SEK",
  maximumFractionDigits: 0
});
const eurFormatter = new Intl.NumberFormat("de-DE", {
  style: "currency",
  currency: "EUR",
  maximumFractionDigits: 0
});
const numberFormatter = new Intl.NumberFormat("sv-SE");

export function DealsTableWithCompare({ opportunities }: { opportunities: Opportunity[] }) {
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const compareHref = useMemo(() => {
    const params = new URLSearchParams();
    selectedIds.forEach((id) => params.append("id", String(id)));
    return `/compare?${params.toString()}`;
  }, [selectedIds]);

  function toggleDeal(dealId: number) {
    setSelectedIds((current) => {
      if (current.includes(dealId)) {
        return current.filter((id) => id !== dealId);
      }
      if (current.length >= 4) {
        return current;
      }
      return [...current, dealId];
    });
  }

  return (
    <section className="table-card">
      <div className="table-header">
        <div>
          <h2>{opportunities.length} matching deals</h2>
          <p>Select 2-4 deals to compare side by side, or click a vehicle to open details.</p>
        </div>
        <div className="compare-selection-actions">
          <span className="muted">{selectedIds.length}/4 selected</span>
          <Link
            className={`compare-link-button ${selectedIds.length < 2 ? "disabled-link" : ""}`}
            href={selectedIds.length >= 2 ? compareHref : "#"}
            aria-disabled={selectedIds.length < 2}
          >
            Compare selected
          </Link>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Select</th>
            <th>Vehicle</th>
            <th>Source</th>
            <th>EUR</th>
            <th>Landed</th>
            <th>Profit</th>
            <th>Confidence</th>
            <th>Risk</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {opportunities.map((opportunity) => (
            <tr key={opportunity.id}>
              <td>
                <input
                  aria-label={`Compare ${opportunity.brand} ${opportunity.model}`}
                  type="checkbox"
                  checked={selectedIds.includes(opportunity.id)}
                  onChange={() => toggleDeal(opportunity.id)}
                  disabled={selectedIds.length >= 4 && !selectedIds.includes(opportunity.id)}
                />
              </td>
              <td>
                <Link className="vehicle detail-link" href={`/deals/${opportunity.id}`}>
                  {opportunity.year} {opportunity.brand} {opportunity.model}
                </Link>
                <div className="muted">
                  {opportunity.trim ?? opportunity.variant ?? "Unknown"} · {numberFormatter.format(opportunity.mileage_km)} km
                </div>
              </td>
              <td>{opportunity.source}</td>
              <td>{eurFormatter.format(opportunity.price_eur)}</td>
              <td>{sekFormatter.format(opportunity.total_landed_cost_sek)}</td>
              <td className="positive">{sekFormatter.format(opportunity.expected_profit_sek)}</td>
              <td>{opportunity.confidence_score}</td>
              <td>{opportunity.risk_score}</td>
              <td><span className="badge neutral-badge">{opportunity.status}</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
