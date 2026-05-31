# Car Arbitrage Scanner — Complete AI Co-Build Prompt Pack

## Project Name
Car Arbitrage Scanner

## One-Line Idea
A private web app that scans European car marketplaces, compares import purchase prices against Swedish resale markets, and identifies profitable buy-abroad/sell-in-Sweden opportunities.

## Core MVP Scope
- Source markets: mobile.de, AutoScout24
- Initial seller country: Germany only
- Target resale market: Sweden
- Swedish comparison sources: Blocket, Bytbil
- Initial car models: VW Golf, VW Passat GTE, BMW 320d Touring, Audi A4 Avant, Volvo V60
- Product type: internal/private web dashboard first

---

# 1. Master Prompt For ChatGPT / Claude

You are my senior product strategist, software architect, and full-stack developer. I am building a private car arbitrage scanner for the Swedish market.

The product scans car listings from mobile.de and AutoScout24, initially filtered to German sellers only. It compares those listings against Swedish resale listings from Blocket and Bytbil. The goal is to detect cars that can be bought abroad, imported to Sweden, and sold for profit after all costs.

The app should help me:
1. Find potentially undervalued cars in Germany.
2. Compare them with similar cars in Sweden.
3. Estimate total landed cost.
4. Estimate realistic Swedish resale price.
5. Calculate expected profit.
6. Score the deal based on confidence and risk.
7. Track listings through a deal pipeline.
8. Store market insights over time.
9. Alert me when high-confidence opportunities appear.

Important MVP constraints:
- Do not build a SaaS first.
- Build an internal tool first.
- Keep the scope narrow.
- Start with Germany to Sweden only.
- Start with five car models:
  - VW Golf
  - VW Passat GTE
  - BMW 320d Touring
  - Audi A4 Avant
  - Volvo V60
- Focus on validation and practical usefulness.
- Prioritize data quality and conservative profit estimates.

Recommended stack:
- Frontend: Next.js, TypeScript, Tailwind CSS, shadcn/ui
- Backend: Python, FastAPI
- Database: PostgreSQL
- Scraping/import: Playwright, Apify, or official APIs where available
- Queue/jobs: Celery, Redis, or simple cron jobs for MVP
- Hosting: Railway, Render, Fly.io, or Hetzner
- AI features: OpenAI/Claude for listing normalization, trim extraction, risk flags, and comparison summaries

Help me build this step by step. Always prefer practical MVP implementation over overengineering. When coding, give clean production-ready code with clear file paths.

---

# 2. Product Requirements Document Prompt

Create a complete Product Requirements Document for a private web app called Car Arbitrage Scanner.

The app identifies profitable car import opportunities from Germany to Sweden.

Include:
- Problem statement
- Target user
- Core use cases
- MVP scope
- Non-MVP scope
- User stories
- Functional requirements
- Non-functional requirements
- Data sources
- Marketplace limitations and legal risk notes
- Profit calculation logic
- Deal scoring system
- Confidence scoring system
- Database entities
- Dashboard pages
- Admin pages
- Alert system
- Future roadmap
- Success metrics

Make the PRD practical and technical enough that a developer can start building immediately.

---

# 3. Figma Design Prompt

Design a clean, professional dashboard UI for a private web app called Car Arbitrage Scanner.

The product helps identify profitable car import opportunities from Germany to Sweden.

Style:
- Modern SaaS dashboard
- Clean, data-heavy, trustworthy
- Scandinavian minimal design
- Dark sidebar, light main content
- Use cards, tables, filters, badges, and charts
- Prioritize clarity over decoration

Main pages:

1. Dashboard
- KPI cards:
  - Cars scanned today
  - Active opportunities
  - Average expected profit
  - Best model this week
  - High-confidence deals
- Recent high-profit deals table
- Model performance chart
- Alerts panel

2. Deal Scanner
- Main table with columns:
  - Image
  - Source
  - Brand
  - Model
  - Year
  - Mileage
  - German price
  - Estimated Swedish price
  - Total landed cost
  - Expected profit
  - Confidence
  - Risk
  - Status
- Filters:
  - Model
  - Year
  - Mileage
  - Profit minimum
  - Confidence
  - Source
  - Seller country
  - Fuel type
  - Transmission

3. Deal Detail Page
- Hero section with car image, title, source link
- Purchase price
- Swedish estimated resale value
- Cost breakdown
- Profit estimate
- Confidence score
- Risk flags
- Comparable Swedish listings
- AI summary
- Notes section
- Action buttons:
  - Save
  - Reject
  - Contact seller
  - Move to negotiation

4. Market Research
- Model-level analytics:
  - VW Golf
  - VW Passat GTE
  - BMW 320d Touring
  - Audi A4 Avant
  - Volvo V60
- Average German price
- Average Swedish price
- Spread
- Liquidity score
- Risk notes
- Best trims

5. Deal Pipeline
Kanban board with columns:
- New
- Researching
- Contacted
- Negotiating
- Bought
- Imported
- Listed in Sweden
- Sold
- Rejected

6. Settings
- Cost assumptions:
  - EUR/SEK rate
  - Transport cost
  - Registration cost
  - Inspection cost
  - Repair buffer
  - Desired minimum profit
- Alert rules
- Model watchlist

Components:
- KPI card
- Deal table row
- Profit badge
- Confidence badge
- Risk badge
- Cost breakdown card
- Comparable listing card
- Filter sidebar
- Deal pipeline card
- Alert card

Create desktop-first layouts, but ensure mobile responsive versions for quick deal checks.

---

# 4. Cursor / VS Code Build Prompt

You are my senior full-stack engineer. Build the MVP of Car Arbitrage Scanner.

Use this stack:
- Frontend: Next.js 14+, TypeScript, Tailwind CSS, shadcn/ui
- Backend API: FastAPI in Python
- Database: PostgreSQL
- ORM: SQLAlchemy
- Scraping/import layer: Python services with placeholder adapters first
- Auth: skip auth for local MVP
- Deployment later

Project structure:

car-arbitrage-scanner/
  frontend/
    app/
    components/
    lib/
    types/
  backend/
    app/
      main.py
      models.py
      schemas.py
      database.py
      routers/
      services/
      scrapers/
      scoring/
  docker-compose.yml
  README.md

Build:
1. PostgreSQL schema
2. FastAPI backend
3. CRUD endpoints for listings, deals, cost assumptions, model research, and market comps
4. Profit calculation engine
5. Deal scoring engine
6. Frontend dashboard
7. Deal scanner table
8. Deal detail page
9. Settings page for cost assumptions
10. Seed data using the five starter models:
   - VW Golf
   - VW Passat GTE
   - BMW 320d Touring
   - Audi A4 Avant
   - Volvo V60

Do not implement real scraping yet. Create placeholder importer services that accept JSON input and store normalized listings. Use mock data first.

Prioritize a working local MVP over perfect architecture.

Give me the complete file-by-file implementation.

---

# 5. Database Schema Prompt

Design a PostgreSQL database schema for Car Arbitrage Scanner.

Core entities:

1. car_listings
Fields:
- id
- source
- source_listing_id
- listing_url
- seller_country
- seller_type
- brand
- model
- variant
- trim
- year
- first_registration_date
- mileage_km
- fuel_type
- transmission
- drivetrain
- body_type
- color
- price_eur
- currency
- vat_deductible
- damaged
- accident_history
- service_history
- description
- image_urls
- scraped_at
- created_at
- updated_at

2. swedish_comparables
Fields:
- id
- source
- listing_url
- brand
- model
- variant
- year
- mileage_km
- fuel_type
- transmission
- trim
- price_sek
- location
- seller_type
- listing_age_days
- created_at

3. deals
Fields:
- id
- foreign_listing_id
- estimated_swedish_price_sek
- purchase_price_sek
- transport_cost_sek
- registration_cost_sek
- inspection_cost_sek
- repair_buffer_sek
- tax_cost_sek
- other_costs_sek
- total_landed_cost_sek
- expected_profit_sek
- margin_percent
- confidence_score
- risk_score
- liquidity_score
- deal_grade
- status
- notes
- created_at
- updated_at

4. model_research
Fields:
- id
- brand
- model
- variant
- good_years
- strong_trims
- weak_trims
- common_issues
- swedish_demand_score
- german_supply_score
- liquidity_score
- risk_notes
- target_buy_price_min
- target_buy_price_max
- target_sell_price_min
- target_sell_price_max
- created_at
- updated_at

5. cost_assumptions
Fields:
- id
- eur_to_sek_rate
- default_transport_cost_sek
- default_registration_cost_sek
- default_inspection_cost_sek
- default_repair_buffer_sek
- default_tax_cost_sek
- minimum_profit_threshold_sek
- minimum_confidence_score
- updated_at

6. alerts
Fields:
- id
- deal_id
- alert_type
- message
- sent
- sent_at
- created_at

Include:
- indexes
- relationships
- enum suggestions
- SQLAlchemy models
- Alembic migration suggestion

---

# 6. Profit Engine Prompt

Create a Python profit calculation engine for Car Arbitrage Scanner.

Input:
- purchase_price_eur
- eur_to_sek_rate
- estimated_swedish_price_sek
- transport_cost_sek
- registration_cost_sek
- inspection_cost_sek
- repair_buffer_sek
- tax_cost_sek
- other_costs_sek
- desired_profit_sek

Output:
- purchase_price_sek
- total_landed_cost_sek
- expected_profit_sek
- margin_percent
- break_even_price_sek
- recommended_max_bid_eur

Formula:
purchase_price_sek = purchase_price_eur * eur_to_sek_rate

total_landed_cost_sek =
purchase_price_sek +
transport_cost_sek +
registration_cost_sek +
inspection_cost_sek +
repair_buffer_sek +
tax_cost_sek +
other_costs_sek

expected_profit_sek =
estimated_swedish_price_sek - total_landed_cost_sek

margin_percent =
expected_profit_sek / total_landed_cost_sek * 100

recommended_max_bid_eur =
(estimated_swedish_price_sek - desired_profit_sek - side_costs_sek) / eur_to_sek_rate

Conservative defaults:
- transport: 8000 SEK
- registration: 4000 SEK
- inspection: 2500 SEK
- repair buffer: 10000 SEK
- other costs: 3000 SEK
- desired minimum profit: 20000 SEK

Return a typed object or Pydantic schema.
Add unit tests.

---

# 7. Deal Scoring Prompt

Create a deal scoring engine for Car Arbitrage Scanner.

Calculate:

1. Profit score
- 50,000+ SEK = 100
- 30,000–49,999 SEK = 80
- 20,000–29,999 SEK = 60
- 10,000–19,999 SEK = 40
- below 10,000 SEK = 20
- negative profit = 0

2. Confidence score
Based on:
- number of Swedish comparable listings
- similarity between foreign listing and Swedish comps
- mileage difference
- year difference
- trim match
- seller type
- service history
- missing data penalty

3. Risk score
Higher risk if:
- damaged car
- accident history
- missing service history
- very high mileage
- suspiciously low price
- private seller
- weak trim match
- low number of comps

4. Liquidity score
Based on:
- model popularity
- number of Swedish listings
- average listing age
- wagon/SUV/hybrid desirability
- known Swedish demand

5. Final deal grade:
- A+ = high profit, high confidence, low risk
- A = strong deal
- B = possible deal
- C = weak deal
- D = avoid

Return:
- profit_score
- confidence_score
- risk_score
- liquidity_score
- final_score
- deal_grade
- explanation
- risk_flags

Write this in Python with clear functions and unit tests.

---

# 8. Listing Normalization AI Prompt

You are a car listing normalization assistant.

Given a raw car title and description, extract structured information.

Return only JSON.

Fields:
- brand
- model
- variant
- trim
- year
- mileage_km
- fuel_type
- transmission
- drivetrain
- body_type
- color
- vat_deductible
- damaged
- accident_history
- service_history
- key_options
- risk_flags
- confidence

Rules:
- Do not guess if data is missing.
- Use null for unknown values.
- Extract important options like:
  - M Sport
  - S-Line
  - R-Line
  - tow hitch
  - panoramic roof
  - adaptive cruise
  - navigation
  - leather
  - AWD
  - quattro
  - xDrive
- Identify signs of risk:
  - accident
  - damaged
  - export only
  - no service history
  - engine problem
  - gearbox problem
  - rebuilt
  - high number of owners

Input:
TITLE:
{{title}}

DESCRIPTION:
{{description}}

Return JSON only.

---

# 9. Comparable Matching Prompt

You are a car comparison assistant.

Compare a foreign car listing against Swedish comparable listings and estimate whether they are similar enough to use for pricing.

Foreign listing:
{{foreign_listing_json}}

Swedish comparables:
{{swedish_comparables_json}}

Evaluate:
- same brand/model
- similar variant
- similar year
- similar mileage
- similar trim
- same fuel type
- transmission
- body type
- equipment level
- seller type
- imported car penalty

Return JSON:
{
  "usable_comps": [],
  "rejected_comps": [],
  "estimated_swedish_price_sek": number,
  "confidence_score": number,
  "pricing_explanation": string,
  "warnings": []
}

Rules:
- Be conservative.
- Swedish imported cars may sell slightly lower than Swedish-original cars.
- Do not use comps that are too different.
- Explain uncertainty.

---

# 10. Frontend UI Build Prompt

Build the frontend for Car Arbitrage Scanner using Next.js, TypeScript, Tailwind CSS, and shadcn/ui.

Pages:
1. /dashboard
2. /deals
3. /deals/[id]
4. /market-research
5. /pipeline
6. /settings

Components:
- Sidebar navigation
- KPI cards
- Deal table
- Deal filters
- Profit badge
- Confidence badge
- Risk badge
- Cost breakdown card
- Comparable listings card
- Deal detail header
- Deal score panel
- Pipeline kanban board
- Settings form

Design style:
- Clean SaaS dashboard
- Scandinavian minimalism
- Dense but readable tables
- Strong use of badges
- Profit-positive rows should be visually obvious
- Risk warnings should be clear
- Desktop-first but responsive

Use mock data first. Add API integration later.

---

# 11. Backend API Prompt

Build a FastAPI backend for Car Arbitrage Scanner.

Required endpoints:

Listings:
- GET /api/listings
- GET /api/listings/{id}
- POST /api/listings
- PATCH /api/listings/{id}
- DELETE /api/listings/{id}

Deals:
- GET /api/deals
- GET /api/deals/{id}
- POST /api/deals/calculate
- PATCH /api/deals/{id}/status

Comparables:
- GET /api/comparables
- POST /api/comparables

Model Research:
- GET /api/model-research
- POST /api/model-research
- PATCH /api/model-research/{id}

Settings:
- GET /api/settings
- PATCH /api/settings

Alerts:
- GET /api/alerts
- POST /api/alerts/test

Include:
- SQLAlchemy models
- Pydantic schemas
- service layer
- error handling
- CORS config
- seed data
- README instructions

---

# 12. Scraper Adapter Prompt

Create a scraper adapter architecture for Car Arbitrage Scanner.

Important:
Do not hardcode marketplace logic into the main app.
Create source adapters.

Interface:
class MarketplaceAdapter:
    def search_listings(self, query: SearchQuery) -> list[RawListing]
    def parse_listing(self, raw: RawListing) -> NormalizedListing
    def get_listing_detail(self, url: str) -> RawListingDetail

Adapters:
- MobileDeAdapter
- AutoScout24Adapter
- BlocketAdapter
- BytbilAdapter

For MVP:
- create mock adapters
- create manual JSON importer
- create CSV importer

Later:
- add Playwright-based adapters
- add Apify-based adapters
- add API-based adapters if available

Include:
- rate limiting
- retry handling
- duplicate detection
- source_listing_id tracking
- country filters
- seller type filters
- logging
- scraper health status

---

# 13. AI Feature Prompt

Add AI-assisted listing analysis to Car Arbitrage Scanner.

Features:
1. Normalize raw listing title and description.
2. Extract trim and options.
3. Detect risk flags.
4. Compare German listing to Swedish comps.
5. Generate deal explanation.
6. Generate seller contact message in German.
7. Generate Swedish sales listing text.

Backend architecture:
- ai_service.py
- prompt templates
- JSON-only responses
- validation with Pydantic
- fallback if AI fails
- store AI output in database

Important:
- AI should not be the only pricing authority.
- AI should assist, explain, and flag uncertainty.
- Final profit calculation should be deterministic.

---

# 14. Seller Contact Prompt

Write a polite German message to a car seller.

Goal:
Ask about condition, service history, accident history, export possibility, and availability.

Car:
{{car_title}}
Price:
{{price}}
Listing URL:
{{url}}

Tone:
- polite
- serious buyer
- short
- clear
- not too pushy

Questions:
1. Is the car still available?
2. Does it have full service history?
3. Has it had any accidents or paintwork?
4. Are there any technical issues?
5. Is export to Sweden possible?
6. Can you send more photos or a VIN?

Return:
- German message
- English translation

---

# 15. Swedish Resale Listing Prompt

Write a Swedish Blocket-style car sales listing.

Car details:
{{car_json}}

Tone:
- trustworthy
- clear
- professional
- not too salesy

Include:
- headline
- short intro
- key specs
- equipment
- condition
- service history
- import status if relevant
- price
- contact call-to-action

Avoid exaggeration.
Make it sound like a serious seller.

---

# 16. Roadmap

## Phase 1 — Manual Validation
Duration: 1–3 weeks

Tasks:
- Create Google Sheet and Notion HQ
- Research 5 starter models
- Add 10 German and 10 Swedish listings per model
- Estimate margins manually
- Identify strongest patterns
- Decide if opportunity is real

Exit criteria:
- At least 10 realistic profitable opportunities found
- At least 3 models show repeatable spread
- Profit estimates survive conservative cost assumptions

## Phase 2 — Local MVP With Mock Data
Duration: 2–4 weeks

Tasks:
- Build database
- Build backend
- Build frontend
- Add manual listing input
- Add profit engine
- Add deal scoring
- Add market research pages

Exit criteria:
- You can manually add listings
- App calculates profit
- App ranks deals
- App tracks deal status

## Phase 3 — Importers
Duration: 2–6 weeks

Tasks:
- Add CSV import
- Add JSON import
- Add marketplace adapters
- Add duplicate detection
- Add scheduled jobs

Exit criteria:
- Listings can be imported repeatedly
- Duplicates are handled
- Deal scoring updates automatically

## Phase 4 — AI Analysis
Duration: 1–3 weeks

Tasks:
- Listing normalization
- Risk detection
- Comparable matching explanation
- Seller contact messages
- Swedish sales text

Exit criteria:
- AI improves workflow without replacing deterministic calculations

## Phase 5 — Alerts
Duration: 1 week

Tasks:
- Telegram/email alerts
- Alert thresholds
- Saved searches
- Daily summary

Exit criteria:
- High-confidence deals trigger alerts

## Phase 6 — Real-World Testing
Duration: ongoing

Tasks:
- Use tool daily
- Contact sellers
- Track actual costs
- Track actual resale prices
- Improve scoring

Exit criteria:
- First real import completed
- Actual profit/loss recorded

## Phase 7 — Browser Extension
Later

Features:
- Open mobile.de listing
- Extension shows Swedish estimated resale value
- Profit calculation overlay
- Risk flags
- Save to dashboard button

---

# 17. Starter Model Research Table

| Priority | Model | Why Start Here | Target Years | Notes |
|---|---|---|---|---|
| 1 | VW Golf | High liquidity, easy resale | 2014–2020 | GTD, Variant, DSG interesting |
| 2 | VW Passat GTE | Swedish hybrid demand | 2017–2021 | Watch battery/charging history |
| 3 | BMW 320d Touring | Premium wagon demand | 2014–2020 | M Sport preferred |
| 4 | Audi A4 Avant | Strong resale, family/premium | 2014–2020 | S-Line/quattro desirable |
| 5 | Volvo V60 | Swedish trust, wagon demand | 2015–2020 | D4/R-Design interesting |

---

# 18. Development Rules

Always follow these rules:
1. Build the simplest useful version first.
2. Avoid overengineering.
3. Manual input is acceptable in MVP.
4. Scraping is not the first priority.
5. Make profit calculations conservative.
6. Store every assumption.
7. Track actual outcomes.
8. Separate raw listing data from normalized data.
9. Separate deterministic calculations from AI opinions.
10. Build for Germany first, but keep database country-ready.

---

# 19. MVP Done Definition

The MVP is done when:
- I can add a foreign car listing manually.
- I can add Swedish comparable listings manually.
- The app calculates total landed cost.
- The app estimates expected profit.
- The app gives a deal grade.
- The app stores risk notes.
- The app tracks status from New to Sold.
- The app lets me compare models.
- The app works locally without real scraping.
- I can use it to make a real buy/no-buy decision.

---

# 20. First Cursor Command

Create a new monorepo called car-arbitrage-scanner with a Next.js frontend and FastAPI backend. Use PostgreSQL through Docker Compose. Implement the initial project structure, database connection, base models, seed data, and a simple dashboard page showing mock deal opportunities. Do not add scraping yet. Focus on getting the app running locally with clean architecture.

Include:
- docker-compose.yml
- backend FastAPI app
- frontend Next.js app
- README with setup steps
- seed data for VW Golf, VW Passat GTE, BMW 320d Touring, Audi A4 Avant, Volvo V60
- profit calculation utility
- deal scoring utility
- sample API endpoint returning deal opportunities

After creating the base, explain how to run it locally.
