import Link from "next/link";

import { AppNav } from "../../../components/app-nav";
import { ComparableForm } from "../../../components/comparable-form";
import { notFound } from "next/navigation";

import { getDealDetail } from "../../../lib/api";

export const dynamic = "force-dynamic";

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

function formatSek(value: number) {
  return sekFormatter.format(value);
}

function formatEur(value: number) {
  return eurFormatter.format(value);
}

function scoreClass(score: number, inverted = false) {
  const positive = inverted ? score <= 35 : score >= 75;
  const warning = inverted ? score <= 55 : score >= 55;

  if (positive) {
    return "badge positive-badge";
  }

  if (warning) {
    return "badge warning-badge";
  }

  return "badge danger-badge";
}

type PageProps = {
  params: Promise<{ id: string }>;
};

export default async function DealDetailPage({ params }: PageProps) {
  const { id } = await params;
  const dealId = Number(id);

  if (!Number.isInteger(dealId)) {
    notFound();
  }

  const detail = await getDealDetail(dealId).catch(() => null);

  if (!detail) {
    notFound();
  }

  const { opportunity, listing, cost_breakdown: costBreakdown } = detail;

  return (
    <main className="page">
      <AppNav />
      <section className="detail-hero">
        <div>
          <Link className="back-link" href="/">
            Back to dashboard
          </Link>
          <p className="eyebrow">Deal detail</p>
          <h1>
            {opportunity.year} {opportunity.brand} {opportunity.model}
          </h1>
          <p className="subtitle">
            {opportunity.trim ?? opportunity.variant ?? "Unknown trim"} from {" "}
            {opportunity.source} in {opportunity.seller_country}. This view
            keeps deterministic calculations separate from future AI or scraper
            opinions.
          </p>
        </div>
        <aside className="status-card detail-status-card">
          <span>Expected profit</span>
          <strong>{formatSek(opportunity.expected_profit_sek)}</strong>
          <div className="badge-row detail-badges">
            <span className="badge grade-badge">{opportunity.deal_grade}</span>
            <span className={scoreClass(opportunity.confidence_score)}>
              Confidence {opportunity.confidence_score}
            </span>
            <span className={scoreClass(opportunity.risk_score, true)}>
              Risk {opportunity.risk_score}
            </span>
          </div>
        </aside>
      </section>

      <section className="detail-grid">
        <article className="detail-card">
          <p className="metric-label">Purchase</p>
          <p className="metric-value">{formatEur(opportunity.price_eur)}</p>
          <dl className="detail-list">
            <div>
              <dt>Seller</dt>
              <dd>{opportunity.seller_type}</dd>
            </div>
            <div>
              <dt>Mileage</dt>
              <dd>{numberFormatter.format(opportunity.mileage_km)} km</dd>
            </div>
            <div>
              <dt>Fuel / transmission</dt>
              <dd>
                {opportunity.fuel_type ?? "Unknown"} / {" "}
                {opportunity.transmission ?? "Unknown"}
              </dd>
            </div>
          </dl>
        </article>

        <article className="detail-card">
          <p className="metric-label">Swedish resale estimate</p>
          <p className="metric-value">
            {formatSek(opportunity.estimated_swedish_price_sek)}
          </p>
          <dl className="detail-list">
            <div>
              <dt>Total landed cost</dt>
              <dd>{formatSek(opportunity.total_landed_cost_sek)}</dd>
            </div>
            <div>
              <dt>Margin</dt>
              <dd>{opportunity.margin_percent}%</dd>
            </div>
            <div>
              <dt>Status</dt>
              <dd>{opportunity.status}</dd>
            </div>
          </dl>
        </article>

        <article className="detail-card wide-detail-card">
          <p className="metric-label">Scoring explanation</p>
          <p className="detail-copy">
            {opportunity.explanation ?? "No scoring explanation available."}
          </p>
          <div className="risk-list">
            {opportunity.risk_flags.length > 0 ? (
              opportunity.risk_flags.map((flag) => (
                <span className="badge warning-badge" key={flag}>
                  {flag}
                </span>
              ))
            ) : (
              <span className="badge positive-badge">No risk flags</span>
            )}
          </div>
        </article>
      </section>

      <section className="detail-grid two-column-grid">
        <article className="detail-card">
          <h2>Cost breakdown</h2>
          <dl className="cost-list">
            <div>
              <dt>Purchase price</dt>
              <dd>{formatSek(costBreakdown.purchase_price_sek)}</dd>
            </div>
            <div>
              <dt>Transport</dt>
              <dd>{formatSek(costBreakdown.transport_cost_sek)}</dd>
            </div>
            <div>
              <dt>Registration</dt>
              <dd>{formatSek(costBreakdown.registration_cost_sek)}</dd>
            </div>
            <div>
              <dt>Inspection</dt>
              <dd>{formatSek(costBreakdown.inspection_cost_sek)}</dd>
            </div>
            <div>
              <dt>Repair buffer</dt>
              <dd>{formatSek(costBreakdown.repair_buffer_sek)}</dd>
            </div>
            <div>
              <dt>Tax</dt>
              <dd>{formatSek(costBreakdown.tax_cost_sek)}</dd>
            </div>
            <div>
              <dt>Other costs</dt>
              <dd>{formatSek(costBreakdown.other_costs_sek)}</dd>
            </div>
            <div className="total-row">
              <dt>Total landed cost</dt>
              <dd>{formatSek(costBreakdown.total_landed_cost_sek)}</dd>
            </div>
          </dl>
        </article>

        <article className="detail-card">
          <h2>Foreign listing</h2>
          <dl className="detail-list">
            <div>
              <dt>Source listing id</dt>
              <dd>{listing.source_listing_id}</dd>
            </div>
            <div>
              <dt>Service history</dt>
              <dd>{listing.service_history ?? "Unknown"}</dd>
            </div>
            <div>
              <dt>VAT deductible</dt>
              <dd>{listing.vat_deductible ? "Yes" : "No"}</dd>
            </div>
            <div>
              <dt>Damaged</dt>
              <dd>{listing.damaged ? "Yes" : "No"}</dd>
            </div>
          </dl>
          {listing.listing_url ? (
            <a className="external-link" href={listing.listing_url}>
              Open source listing
            </a>
          ) : null}
        </article>
      </section>


      <ComparableForm
        compact
        defaults={{
          brand: opportunity.brand,
          model: opportunity.model,
          variant: opportunity.variant,
          year: opportunity.year,
          fuel_type: opportunity.fuel_type,
          transmission: opportunity.transmission,
          trim: opportunity.trim
        }}
      />

      <section className="table-card">
        <div className="table-header">
          <div>
            <h2>Comparable Swedish listings</h2>
            <p>
              Current seed/manual comps matching {opportunity.brand} {" "}
              {opportunity.model}.
            </p>
          </div>
        </div>
        <table>
          <thead>
            <tr>
              <th>Vehicle</th>
              <th>Location</th>
              <th>Mileage</th>
              <th>Seller</th>
              <th>Age</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            {detail.comparables.length > 0 ? (
              detail.comparables.map((comparable) => (
                <tr key={comparable.id}>
                  <td>
                    <div className="vehicle">
                      {comparable.year} {comparable.brand} {comparable.model}
                    </div>
                    <div className="muted">
                      {comparable.trim ?? comparable.variant ?? "Unknown trim"}
                    </div>
                  </td>
                  <td>{comparable.location ?? "Unknown"}</td>
                  <td>
                    {comparable.mileage_km
                      ? `${numberFormatter.format(comparable.mileage_km)} km`
                      : "Unknown"}
                  </td>
                  <td>{comparable.seller_type ?? "Unknown"}</td>
                  <td>
                    {comparable.listing_age_days !== null
                      ? `${comparable.listing_age_days} days`
                      : "Unknown"}
                  </td>
                  <td className="positive">{formatSek(comparable.price_sek)}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={6}>No matching comparables yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </section>
    </main>
  );
}
