import { AppNav } from "../../components/app-nav";
import { getModelResearch } from "../../lib/api";

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

function formatRange(
  min: number | null,
  max: number | null,
  formatter: Intl.NumberFormat
) {
  if (min === null || max === null) {
    return "Not set";
  }
  return `${formatter.format(min)} - ${formatter.format(max)}`;
}

export default async function MarketResearchPage() {
  const rows = await getModelResearch();

  return (
    <main className="page">
      <AppNav />
      <section className="hero">
        <div>
          <p className="eyebrow">Market research</p>
          <h1>Starter model analytics</h1>
          <p className="subtitle">
            Seeded research for the five Phase 2 starter models. Use this to
            guide manual buy/no-buy checks before real importers exist.
          </p>
        </div>
      </section>

      <section className="research-grid">
        {rows.map((row) => (
          <article className="detail-card" key={row.id}>
            <p className="metric-label">{row.brand}</p>
            <h2>
              {row.model} {row.variant ?? ""}
            </h2>
            <dl className="detail-list">
              <div>
                <dt>Good years</dt>
                <dd>{row.good_years ?? "Unknown"}</dd>
              </div>
              <div>
                <dt>Buy range</dt>
                <dd>{formatRange(row.target_buy_price_min, row.target_buy_price_max, eurFormatter)}</dd>
              </div>
              <div>
                <dt>Sell range</dt>
                <dd>{formatRange(row.target_sell_price_min, row.target_sell_price_max, sekFormatter)}</dd>
              </div>
              <div>
                <dt>Demand / supply</dt>
                <dd>{row.swedish_demand_score} / {row.german_supply_score}</dd>
              </div>
              <div>
                <dt>Liquidity</dt>
                <dd>{row.liquidity_score}</dd>
              </div>
            </dl>
            <div className="risk-list">
              {row.strong_trims.map((trim) => (
                <span className="badge positive-badge" key={trim}>{trim}</span>
              ))}
            </div>
            {row.risk_notes ? <p className="detail-copy">{row.risk_notes}</p> : null}
          </article>
        ))}
      </section>
    </main>
  );
}
