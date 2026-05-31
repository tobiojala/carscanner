import { getDashboardSummary, getOpportunities } from "../lib/api";

export const dynamic = "force-dynamic";

const currencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0
});

const numberFormatter = new Intl.NumberFormat("en-US");

function formatCurrency(value: number) {
  return currencyFormatter.format(value);
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
            <p className="eyebrow">Local dashboard</p>
            <h1>Car Arbitrage Scanner</h1>
            <p className="subtitle">
              Start the stack with <code>docker compose up --build</code> to
              load the API, PostgreSQL, and seed data.
            </p>
          </div>
        </section>
        <div className="error">
          Unable to reach the backend API.{" "}
          {error instanceof Error ? error.message : "Unknown error"}
        </div>
      </main>
    );
  }

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Local dashboard</p>
          <h1>Car Arbitrage Scanner</h1>
          <p className="subtitle">
            Seeded opportunities show how the app will track price spreads
            between source and target markets. Scraping can be added behind the
            backend service layer later.
          </p>
        </div>
        <aside className="status-card">
          <span>Backend API</span>
          <strong>Connected</strong>
        </aside>
      </section>

      <section className="metrics" aria-label="Dashboard summary">
        <article className="metric-card">
          <p className="metric-label">Seed listings</p>
          <p className="metric-value">{summary.total_listings}</p>
        </article>
        <article className="metric-card">
          <p className="metric-label">Average spread</p>
          <p className="metric-value">
            {formatCurrency(summary.average_spread)}
          </p>
        </article>
        <article className="metric-card">
          <p className="metric-label">Best spread</p>
          <p className="metric-value">{formatCurrency(summary.best_spread)}</p>
        </article>
      </section>

      <section className="table-card">
        <div className="table-header">
          <div>
            <h2>Seeded opportunities</h2>
            <p>Initial PostgreSQL data loaded by the FastAPI service.</p>
          </div>
          {summary.best_listing ? (
            <p className="positive">
              Best: {summary.best_listing.year} {summary.best_listing.make}{" "}
              {summary.best_listing.model}
            </p>
          ) : null}
        </div>

        <table>
          <thead>
            <tr>
              <th>Vehicle</th>
              <th>Route</th>
              <th>Mileage</th>
              <th>Ask</th>
              <th>Market</th>
              <th>Spread</th>
            </tr>
          </thead>
          <tbody>
            {opportunities.map((listing) => (
              <tr key={listing.id}>
                <td>
                  <div className="vehicle">
                    {listing.year} {listing.make} {listing.model}
                  </div>
                  <div className="muted">{listing.trim ?? "Base trim"}</div>
                </td>
                <td>
                  <div>{listing.source_market}</div>
                  <div className="muted">to {listing.target_market}</div>
                </td>
                <td>{numberFormatter.format(listing.mileage)}</td>
                <td>{formatCurrency(listing.asking_price)}</td>
                <td>{formatCurrency(listing.estimated_market_price)}</td>
                <td className="positive">
                  {formatCurrency(listing.estimated_spread)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}
