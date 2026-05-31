import { AppNav } from "../../components/app-nav";
import { PipelineBoard } from "../../components/pipeline-board";
import { getOpportunities } from "../../lib/api";

export const dynamic = "force-dynamic";

export default async function PipelinePage() {
  const opportunities = await getOpportunities();

  return (
    <main className="page">
      <AppNav />
      <section className="hero">
        <div>
          <p className="eyebrow">Deal pipeline</p>
          <h1>Status tracking</h1>
          <p className="subtitle">
            Move deals through the MVP pipeline from new to sold or rejected.
          </p>
        </div>
      </section>
      <PipelineBoard opportunities={opportunities} />
    </main>
  );
}
