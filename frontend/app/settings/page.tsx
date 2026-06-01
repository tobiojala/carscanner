import { AppNav } from "../../components/app-nav";
import { SettingsForm } from "../../components/settings-form";
import { getSettings } from "../../lib/api";

export const dynamic = "force-dynamic";

export default async function SettingsPage() {
  const settings = await getSettings();

  return (
    <main className="page">
      <AppNav />
      <section className="hero">
        <div>
          <p className="eyebrow">Settings</p>
          <h1>Cost assumptions</h1>
          <p className="subtitle">
            Tune conservative import costs and thresholds before adding manual
            listings.
          </p>
        </div>
      </section>
      <SettingsForm settings={settings} />
    </main>
  );
}
