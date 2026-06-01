import Link from "next/link";

import { AppNav } from "../../components/app-nav";
import { AIVerdict } from "../../components/compare/AIVerdict";
import { DealCompareCard } from "../../components/compare/DealCompareCard";
import { compareDeals } from "../../lib/api";

export const dynamic = "force-dynamic";

const sekFormatter = new Intl.NumberFormat("sv-SE", {
  style: "currency",
  currency: "SEK",
  maximumFractionDigits: 0
});

type PageProps = {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
};

function parseDealIds(params: Record<string, string | string[] | undefined>) {
  const raw = params.id;
  const values = Array.isArray(raw) ? raw : raw ? [raw] : [];
  return values
    .flatMap((value) => value.split(","))
    .map((value) => Number(value))
    .filter((value) => Number.isInteger(value));
}

export default async function ComparePage({ searchParams }: PageProps) {
  const params = await searchParams;
  const dealIds = parseDealIds(params);

  if (dealIds.length < 2) {
    return (
      <main className="page">
        <AppNav />
        <section className="hero">
          <div>
            <p className="eyebrow">Deal comparison</p>
            <h1>Select deals to compare</h1>
            <p className="subtitle">
              Go to the deal scanner and select 2-4 deals for a side-by-side comparison.
            </p>
            <Link className="compare-link-button" href="/deals">Open deal scanner</Link>
          </div>
        </section>
      </main>
    );
  }

  const comparison = await compareDeals(dealIds);
  const maxProfit = Math.max(...comparison.deals.map((deal) => deal.expected_profit_sek), 0);

  return (
    <main className="page">
      <AppNav />
      <section className="hero">
        <div>
          <p className="eyebrow">Deal comparison</p>
          <h1>Compare selected deals</h1>
          <p className="subtitle">
            Side-by-side profitability, risk, confidence, liquidity, and max-bid view for manual buy/no-buy decisions.
          </p>
        </div>
        <aside className="status-card">
          <span>Average expected profit</span>
          <strong>{sekFormatter.format(comparison.average_expected_profit_sek)}</strong>
        </aside>
      </section>

      <section className="compare-grid">
        {comparison.deals.map((deal) => (
          <DealCompareCard
            key={deal.id}
            deal={deal}
            maxProfit={maxProfit}
            isBestProfit={deal.id === comparison.best_profit_deal_id}
            isBestConfidence={deal.id === comparison.best_confidence_deal_id}
            isLowestRisk={deal.id === comparison.lowest_risk_deal_id}
          />
        ))}
      </section>

      <AIVerdict dealIds={comparison.deals.map((deal) => deal.id)} />
    </main>
  );
}
