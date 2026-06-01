"use client";

import { FormEvent, useMemo, useState, useTransition } from "react";

import { previewLinks } from "../lib/client-api";
import type { LinkIntakeItem } from "../lib/api";

const exampleUrl =
  "https://suchen.mobile.de/fahrzeuge/search.html?dam=false&isSearchRequest=true&ms=3500%3B10%3B%3B&ref=quickSearch&s=Car&vc=Car";

export function LinkIntakeForm() {
  const [rawLinks, setRawLinks] = useState(exampleUrl);
  const [items, setItems] = useState<LinkIntakeItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  const groupedItems = useMemo(() => {
    return items.reduce<Record<string, LinkIntakeItem[]>>((groups, item) => {
      const key = `${item.source} · ${item.link_type}`;
      groups[key] = [...(groups[key] ?? []), item];
      return groups;
    }, {});
  }, [items]);

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    const urls = rawLinks
      .split(/\s+/)
      .map((url) => url.trim())
      .filter(Boolean);

    startTransition(async () => {
      try {
        const response = await previewLinks(urls);
        setItems(response.items);
      } catch (caughtError) {
        setError(caughtError instanceof Error ? caughtError.message : "Unknown error");
      }
    });
  }

  return (
    <section className="form-card">
      <div className="table-header compact-header">
        <div>
          <h2>Paste marketplace links</h2>
          <p>
            Search URLs are sorted as research queues. Individual listing URLs
            are the ones to open and manually enter into the dashboard form.
          </p>
        </div>
      </div>
      <form className="link-intake-form" onSubmit={onSubmit}>
        <label>
          Links, one per line or separated by spaces
          <textarea
            value={rawLinks}
            onChange={(event) => setRawLinks(event.target.value)}
            rows={7}
          />
        </label>
        <button type="submit" disabled={isPending}>
          {isPending ? "Sorting..." : "Sort links"}
        </button>
      </form>
      {error ? <p className="form-message error-message">{error}</p> : null}

      {Object.entries(groupedItems).length > 0 ? (
        <div className="link-results">
          {Object.entries(groupedItems).map(([group, groupItems]) => (
            <article className="detail-card" key={group}>
              <h2>{group}</h2>
              <div className="link-result-list">
                {groupItems.map((item) => (
                  <div className="link-result" key={item.url}>
                    <a href={item.url}>{item.url}</a>
                    <dl className="detail-list">
                      <div>
                        <dt>Seller country</dt>
                        <dd>{item.seller_country ?? "Unknown"}</dd>
                      </div>
                      <div>
                        <dt>Source listing id</dt>
                        <dd>{item.source_listing_id ?? "Not found"}</dd>
                      </div>
                    </dl>
                    <div className="risk-list">
                      {item.notes.map((note) => (
                        <span className="badge neutral-badge" key={note}>
                          {note}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </article>
          ))}
        </div>
      ) : null}
    </section>
  );
}
