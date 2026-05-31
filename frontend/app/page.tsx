import { getDashboardSummary, getOpportunities } from "../lib/api";

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

async function loadDashboardData() {
  try {
    const [summary, opportunities] = await Promise.all([
      getDashboardSummary(),
      getOpportunities()
    ]);

    return { summary, opportunities, error: null };
  } catch (error) {
    return { summary: null, opportunities: [], error };
  }
}

export default async function DashboardPage() {
  const { summary, opportunities, error } = await loadDashboardData();

  if (!summary) {
    return (
      <main className="page">
        <section className="hero">
          <div>
            <p className="eyebrow">Phase 2 local MVP</p>
            <h1>Car Arbitrage Scanner</h1>
            <p className="subtitle">
              Start the stack with <code>docker compose up --build</code> to
              load PostgreSQL, FastAPI, Alembic migrations, and mock data.
            </p>
          </div>
        </section>
        <div className="error">
          Unable to reach the backend API. {" "}
          {error instanceof Error ? error.message : "Unknown error"}
        </div>
      </main>
    );
  }

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Germany to Sweden mock scanner</p>
          <h1>Car Arbitrage Scanner</h1>
          <p className="subtitle">
            Phase 2 uses seeded mobile.de and AutoScout24-style listings for VW
            Golf, VW Passat GTE, BMW 320d Touring, Audi A4 Avant, and Volvo V60.
            Scraping is intentionally not implemented yet.
          </p>
        </div>
        <aside className="status-card">
          <span>Local stack</span>
          <strong>API + Postgres ready</strong>
        </aside>
      </section>

      <section className="metrics" aria-label="Dashboard summary">
        <article className="metric-card">
          <p className="metric-label">Cars scanned today</p>
          <p className="metric-value">{summary.cars_scanned_today}</p>
        </article>
        <article className="metric-card">
          <p className="metric-label">Active opportunities</p>
          <p className="metric-value">{summary.active_opportunities}</p>
        </article>
        <article className="metric-card">
          <p className="metric-label">Avg expected profit</p>
          <p className="metric-value">
            {formatSek(summary.average_expected_profit_sek)}
          </p>
        </article>
        <article className="metric-card">
          <p className="metric-label">Best model this week</p>
          <p className="metric-value metric-text">
            {summary.best_model_this_week ?? "No data"}
          </p>
        </article>
        <article className="metric-card">
          <p className="metric-label">High-confidence deals</p>
          <p className="metric-value">{summary.high_confidence_deals}</p>
        </article>
        <article className="metric-card">
          <p className="metric-label">Best opportunity</p>
          <p className="metric-value metric-text">
            {summary.best_opportunity
              ? `${summary.best_opportunity.brand} ${summary.best_opportunity.model}`
              : "No data"}
          </p>
        </article>
      </section>

      <section className="table-card">
        <div className="table-header">
          <div>
            <h2>Mock deal opportunities</h2>
            <p>
              Seeded Phase 2 deals with conservative landed-cost calculation and
              deterministic scoring.
            </p>
          </div>
          {summary.best_opportunity ? (
            <p className="positive">
              Top profit: {formatSek(summary.best_opportunity.expected_profit_sek)}
            </p>
          ) : null}
        </div>

        <table>
          <thead>
            <tr>
              <th>Vehicle</th>
              <th>Source</th>
              <th>German price</th>
              <th>Swedish estimate</th>
              <th>Landed cost</th>
              <th>Profit</th>
              <th>Scores</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {opportunities.map((opportunity) => (
              <tr key={opportunity.id}>
                <td>
                  <div className="vehicle">
                    {opportunity.year} {opportunity.brand} {opportunity.model}
                  </div>
                  <div className="muted">
                    {opportunity.trim ?? opportunity.variant ?? "Unknown trim"} · {" "}
                    {numberFormatter.format(opportunity.mileage_km)} km
                  </div>
                </td>
                <td>
                  <div>{opportunity.source}</div>
                  <div className="muted">
                    {opportunity.seller_country} · {opportunity.seller_type}
                  </div>
                </td>
                <td>{formatEur(opportunity.price_eur)}</td>
                <td>{formatSek(opportunity.estimated_swedish_price_sek)}</td>
                <td>{formatSek(opportunity.total_landed_cost_sek)}</td>
                <td>
                  <div className="positive">
                    {formatSek(opportunity.expected_profit_sek)}
                  </div>
                  <div className="muted">{opportunity.margin_percent}% margin</div>
                </td>
                <td>
                  <div className="badge-row">
                    <span className="badge grade-badge">
                      {opportunity.deal_grade}
                    </span>
                    <span className={scoreClass(opportunity.confidence_score)}>
                      C {opportunity.confidence_score}
                    </span>
                    <span className={scoreClass(opportunity.risk_score, true)}>
                      R {opportunity.risk_score}
                    </span>
                  </div>
                </td>
                <td>
                  <span className="badge neutral-badge">{opportunity.status}</span>
                  {opportunity.risk_flags.length > 0 ? (
                    <div className="muted">{opportunity.risk_flags.join(", ")}</div>
                  ) : null}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}
