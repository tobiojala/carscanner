import Link from "next/link";

import type { CompareDealItem } from "../../lib/api";
import { ProfitBar } from "./ProfitBar";

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

type DealCompareCardProps = {
  deal: CompareDealItem;
  maxProfit: number;
  isBestProfit: boolean;
  isBestConfidence: boolean;
  isLowestRisk: boolean;
};

export function DealCompareCard({
  deal,
  maxProfit,
  isBestProfit,
  isBestConfidence,
  isLowestRisk
}: DealCompareCardProps) {
  return (
    <article className="compare-card">
      <div className="compare-card-header">
        <div>
          <Link className="vehicle detail-link" href={`/deals/${deal.id}`}>
            {deal.title}
          </Link>
          <p className="muted">
            {deal.source} · {numberFormatter.format(deal.mileage_km)} km · {deal.status}
          </p>
        </div>
        <span className="badge grade-badge">{deal.deal_grade}</span>
      </div>

      <div className="compare-badges">
        {isBestProfit ? <span className="badge positive-badge">Best profit</span> : null}
        {isBestConfidence ? <span className="badge positive-badge">Best confidence</span> : null}
        {isLowestRisk ? <span className="badge positive-badge">Lowest risk</span> : null}
      </div>

      <dl className="compare-metrics">
        <div>
          <dt>German price</dt>
          <dd>{eurFormatter.format(deal.price_eur)}</dd>
        </div>
        <div>
          <dt>Landed cost</dt>
          <dd>{sekFormatter.format(deal.total_landed_cost_sek)}</dd>
        </div>
        <div>
          <dt>Swedish estimate</dt>
          <dd>{sekFormatter.format(deal.estimated_swedish_price_sek)}</dd>
        </div>
        <div>
          <dt>Expected profit</dt>
          <dd className="positive">{sekFormatter.format(deal.expected_profit_sek)}</dd>
        </div>
        <div>
          <dt>Max bid</dt>
          <dd>{eurFormatter.format(deal.recommended_max_bid_eur)}</dd>
        </div>
        <div>
          <dt>Confidence / Risk</dt>
          <dd>
            {deal.confidence_score} / {deal.risk_score}
          </dd>
        </div>
      </dl>

      <ProfitBar value={deal.expected_profit_sek} max={maxProfit} />

      {deal.risk_flags.length > 0 ? (
        <div className="risk-list">
          {deal.risk_flags.slice(0, 4).map((risk) => (
            <span className="badge warning-badge" key={risk}>
              {risk}
            </span>
          ))}
        </div>
      ) : null}
    </article>
  );
}
