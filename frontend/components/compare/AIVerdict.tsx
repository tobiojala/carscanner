"use client";

import { useState, useTransition } from "react";

import { API_BASE_URL, type CompareVerdictResponse } from "../../lib/api";

export function AIVerdict({ dealIds }: { dealIds: number[] }) {
  const [verdict, setVerdict] = useState<CompareVerdictResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  function analyze() {
    setError(null);
    startTransition(async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/compare/ai-verdict`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ deal_ids: dealIds })
        });
        if (!response.ok) {
          throw new Error(`Backend request failed: ${response.status}`);
        }
        setVerdict((await response.json()) as CompareVerdictResponse);
      } catch (caughtError) {
        setError(caughtError instanceof Error ? caughtError.message : "Unknown error");
      }
    });
  }

  return (
    <section className="detail-card compare-verdict-card">
      <div className="compare-card-header">
        <div>
          <h2>AI-style verdict</h2>
          <p className="muted">
            Deterministic local analysis runs only when you click. No marketplace scraping.
          </p>
        </div>
        <button type="button" onClick={analyze} disabled={isPending}>
          {isPending ? "Analyzing..." : "Analyze selected deals"}
        </button>
      </div>

      {error ? <p className="form-message error-message">{error}</p> : null}
      {verdict ? (
        <div className="compare-verdict-body">
          <p className="detail-copy">{verdict.verdict}</p>
          <div className="confidence-columns">
            <div>
              <h3>Reasons</h3>
              <ul>
                {verdict.reasons.map((reason) => (
                  <li key={reason}>{reason}</li>
                ))}
              </ul>
            </div>
            <div>
              <h3>Cautions</h3>
              <ul>
                {verdict.cautions.length > 0 ? (
                  verdict.cautions.map((caution) => <li key={caution}>{caution}</li>)
                ) : (
                  <li>No major cautions from the local heuristic.</li>
                )}
              </ul>
            </div>
          </div>
        </div>
      ) : null}
    </section>
  );
}
