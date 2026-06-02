# Automation Roadmap

## Level 1 — Manual Input + AI Assist
User manually adds listings and Swedish comps.
AI helps extract trim, options, risks, and summary.
No scraping.

## Level 2 — CSV Import/Export
User imports listings from CSV.
Tool normalizes rows, calculates profit, scores deals, and exports to CSV/Google Sheets.

## Level 3 — Saved Search Profiles
User stores search filters and source URLs manually.
Profiles include model, year, mileage, country, fuel, transmission, color, options, and target margin.

## Level 4 — Scheduled Marketplace Scanning
Adapters run saved searches.
Duplicates are detected.
New listings are scored automatically.
Scraping limitations and legal risks must be documented.

## Level 5 — AI Deal Analyst
AI summarizes promising listings, detects risk flags, compares Swedish comps, suggests max bid, and drafts seller messages.
Deterministic profit calculation remains source of truth.

## Level 6 — Alerts
Send Telegram/email alerts for high-confidence deals.
Daily summary.
Thresholds per model.

## Level 7 — Browser Extension
When viewing mobile.de or AutoScout24, show:
- estimated Swedish value
- expected profit
- risk score
- save-to-dashboard action

## Rule
Do not build Level 4 before Levels 1–3 are clean and stable.
