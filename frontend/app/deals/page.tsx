import Link from "next/link";

import { AppNav } from "../../components/app-nav";
import { CsvTools } from "../../components/csv-tools";
import { DealsTableWithCompare } from "../../components/compare/DealsTableWithCompare";
import { getOpportunities, type OpportunityFilters } from "../../lib/api";

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

function firstParam(value: string | string[] | undefined) {
  return Array.isArray(value) ? value[0] : value;
}

type PageProps = {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
};

export default async function DealsPage({ searchParams }: PageProps) {
  const params = await searchParams;
  const filters: OpportunityFilters = {
    model: firstParam(params.model),
    min_profit_sek: firstParam(params.min_profit_sek),
    min_confidence: firstParam(params.min_confidence),
    source: firstParam(params.source),
    seller_type: firstParam(params.seller_type),
    fuel_type: firstParam(params.fuel_type),
    transmission: firstParam(params.transmission),
    status_filter: firstParam(params.status_filter)
  };
  const opportunities = await getOpportunities(filters);

  return (
    <main className="page">
      <AppNav />
      <section className="hero">
        <div>
          <p className="eyebrow">Deal scanner</p>
          <h1>Filter opportunities</h1>
          <p className="subtitle">
            Narrow the Germany-to-Sweden mock pipeline by model, profit,
            confidence, source, seller type, fuel, transmission, and status.
          </p>
        </div>
      </section>

      <CsvTools opportunities={opportunities} />

      <section className="filter-card">
        <form className="filter-form">
          <label>
            Model
            <input name="model" defaultValue={filters.model ?? ""} placeholder="Golf" />
          </label>
          <label>
            Min profit SEK
            <input
              name="min_profit_sek"
              type="number"
              defaultValue={filters.min_profit_sek ?? ""}
              placeholder="20000"
            />
          </label>
          <label>
            Min confidence
            <input
              name="min_confidence"
              type="number"
              defaultValue={filters.min_confidence ?? ""}
              placeholder="70"
            />
          </label>
          <label>
            Source
            <input name="source" defaultValue={filters.source ?? ""} placeholder="mobile.de" />
          </label>
          <label>
            Seller type
            <select name="seller_type" defaultValue={filters.seller_type ?? ""}>
              <option value="">Any</option>
              <option value="dealer">Dealer</option>
              <option value="private">Private</option>
            </select>
          </label>
          <label>
            Fuel
            <input name="fuel_type" defaultValue={filters.fuel_type ?? ""} placeholder="diesel" />
          </label>
          <label>
            Transmission
            <input
              name="transmission"
              defaultValue={filters.transmission ?? ""}
              placeholder="automatic"
            />
          </label>
          <label>
            Status
            <select name="status_filter" defaultValue={filters.status_filter ?? ""}>
              <option value="">Any</option>
              <option value="new">New</option>
              <option value="researching">Researching</option>
              <option value="contacted">Contacted</option>
              <option value="negotiating">Negotiating</option>
              <option value="bought">Bought</option>
              <option value="imported">Imported</option>
              <option value="listed_in_sweden">Listed in Sweden</option>
              <option value="sold">Sold</option>
              <option value="rejected">Rejected</option>
            </select>
          </label>
          <button type="submit">Apply filters</button>
          <Link className="clear-link" href="/deals">Clear</Link>
        </form>
      </section>

      <DealsTableWithCompare opportunities={opportunities} />

    </main>
  );
}
