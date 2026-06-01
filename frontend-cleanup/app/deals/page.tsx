import Link from "next/link";
import { AppNav } from "../../components/app-nav";
import { CsvTools } from "../../components/listing-import-csv";
import { DealsTable } from "../../components/deals-table";
import { PipelineBoard } from "../../components/pipeline-board";
import { getOpportunities, type OpportunityFilters } from "../../lib/api";

export const dynamic = "force-dynamic";

const STAGES = [
  { label: "All",        value: ""           },
  { label: "New",        value: "new"        },
  { label: "Opportunity",value: "opportunity" },
  { label: "Reviewing",  value: "reviewing"  },
  { label: "Contacted",  value: "contacted"  },
  { label: "Purchased",  value: "purchased"  },
  { label: "Sold",       value: "sold"       },
];

const sekFormatter = new Intl.NumberFormat("sv-SE", {
  style: "currency",
  currency: "SEK",
  maximumFractionDigits: 0,
});

const eurFormatter = new Intl.NumberFormat("de-DE", {
  style: "currency",
  currency: "EUR",
  maximumFractionDigits: 0,
});

interface Props {
  searchParams: {
    stage?: string;
    view?: string;
    model?: string;
    sort?: string;
  };
}

export default async function DealsPage({ searchParams }: Props) {
  const stage = searchParams.stage ?? "";
  const view = searchParams.view ?? "table";   // "table" | "pipeline"
  const model = searchParams.model ?? "";

  const filters: OpportunityFilters = {
    ...(stage && { stage }),
    ...(model && { model }),
  };

  const opportunities = await getOpportunities(filters);

  return (
    <div className="page-root">
      <AppNav />

      <main className="page-main">
        <div className="page-header">
          <div>
            <h1 className="page-title">Deals</h1>
            <p className="page-subtitle">
              {opportunities.length} listing{opportunities.length !== 1 ? "s" : ""}
              {stage ? ` · ${STAGES.find(s => s.value === stage)?.label}` : ""}
            </p>
          </div>

          <div className="page-actions">
            {/* View toggle: table vs pipeline board */}
            <div className="view-toggle">
              <Link
                href={`/deals?stage=${stage}&view=table`}
                className={view === "table" ? "view-toggle-active" : ""}
              >
                Table
              </Link>
              <Link
                href={`/deals?stage=${stage}&view=pipeline`}
                className={view === "pipeline" ? "view-toggle-active" : ""}
              >
                Pipeline
              </Link>
            </div>

            <CsvTools />
          </div>
        </div>

        {/* Stage tab strip */}
        <div className="stage-tabs">
          {STAGES.map(({ label, value }) => (
            <Link
              key={value}
              href={`/deals?stage=${value}&view=${view}`}
              className={`stage-tab ${stage === value ? "stage-tab-active" : ""}`}
            >
              {label}
            </Link>
          ))}
        </div>

        {/* Content */}
        {view === "pipeline" ? (
          <PipelineBoard opportunities={opportunities} />
        ) : (
          <DealsTable
            opportunities={opportunities}
            sekFormatter={sekFormatter}
            eurFormatter={eurFormatter}
          />
        )}
      </main>
    </div>
  );
}
