import { AppNav } from "../../components/app-nav";
import { LinkIntakeForm } from "../../components/link-intake-form";

export default function LinkIntakePage() {
  return (
    <main className="page">
      <AppNav />
      <section className="hero">
        <div>
          <p className="eyebrow">Manual validation helper</p>
          <h1>Link intake</h1>
          <p className="subtitle">
            Paste mobile.de, AutoScout24, Blocket, or Bytbil URLs. The app will
            sort search links from listing links so you know what belongs in the
            manual input workflow.
          </p>
        </div>
      </section>
      <LinkIntakeForm />
    </main>
  );
}
