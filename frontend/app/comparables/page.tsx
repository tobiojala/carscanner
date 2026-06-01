import { AppNav } from "../../components/app-nav";
import { ComparableForm } from "../../components/comparable-form";
import { getComparables } from "../../lib/api";

export const dynamic = "force-dynamic";

const sekFormatter = new Intl.NumberFormat("sv-SE", {
  style: "currency",
  currency: "SEK",
  maximumFractionDigits: 0
});
const numberFormatter = new Intl.NumberFormat("sv-SE");

export default async function ComparablesPage() {
  const comparables = await getComparables();

  return (
    <main className="page">
      <AppNav />
      <section className="hero">
        <div>
          <p className="eyebrow">Swedish market comps</p>
          <h1>Comparable listings</h1>
          <p className="subtitle">
            Add Swedish resale listings manually from Blocket or Bytbil. These
            are used to support conservative pricing and confidence checks.
          </p>
        </div>
      </section>

      <ComparableForm />

      <section className="table-card">
        <div className="table-header">
          <div>
            <h2>{comparables.length} Swedish comparables</h2>
            <p>Newest manual and seed comparables.</p>
          </div>
        </div>
        <table>
          <thead>
            <tr>
              <th>Vehicle</th>
              <th>Source</th>
              <th>Location</th>
              <th>Mileage</th>
              <th>Seller</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            {comparables.map((comparable) => (
              <tr key={comparable.id}>
                <td>
                  <div className="vehicle">
                    {comparable.year} {comparable.brand} {comparable.model}
                  </div>
                  <div className="muted">
                    {comparable.trim ?? comparable.variant ?? "Unknown trim"}
                  </div>
                </td>
                <td>{comparable.source}</td>
                <td>{comparable.location ?? "Unknown"}</td>
                <td>
                  {comparable.mileage_km
                    ? `${numberFormatter.format(comparable.mileage_km)} km`
                    : "Unknown"}
                </td>
                <td>{comparable.seller_type ?? "Unknown"}</td>
                <td className="positive">{sekFormatter.format(comparable.price_sek)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}
