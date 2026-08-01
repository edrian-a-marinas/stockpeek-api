# StockPeek — Roadmap & Untold Details
_Everything not covered in the initial brief: stack reasoning, UI/UX decisions, and planned future features._

## Stack Explanations

**Backend**

- **Django** — Core framework for this project, chosen specifically to practice Django's native ecosystem (Models, Views, Forms, URLs, built-in Auth, Admin panel), separate from the FastAPI stack used across other projects.
- **PostgreSQL** — Primary relational database, storing structured data with clear relationships: Users, Watchlist items, and each user's static notes/rules per stock.
- **MongoDB** — Stores user activity logs (e.g., "added AAPL to watchlist," "removed TSLA") — event-style data that doesn't need strict relational structure, kept separate from the core relational data in PostgreSQL.
- **Redis** — Caching layer for stock prices. Since prices are shared across all users watching the same stock, Redis stores the latest fetched price with a timestamp, so repeated views don't trigger repeated external API calls.
- **Celery** — Handles background jobs, specifically the periodic refresh of cached stock prices (e.g., every 15-30 minutes) and any future scheduled tasks like notifications, without blocking the main app.
- **Twelve Data API** — External source for stock price and historical data, used on a free tier with daily request limits, which is why prices are cached and refreshed periodically instead of fetched live on every page view.
- **LLM API** — Used once per stock (not conversational) to generate a static overview: what the company does, its long-term relevance, and general risks. Output is cached per stock so it's not regenerated on every user view.

**Frontend**

- **React** — Core UI framework for building the interactive watchlist dashboard.
- **Vite** — Build tool for fast development and bundling, consistent with other projects.
- **TanStack Query** — Handles data fetching and caching on the frontend side, keeping the watchlist in sync with backend data without unnecessary re-fetching.
- **TanStack Table** — Renders the watchlist in a clean, sortable table format (price, change %, last updated, etc.).
- **Zod** — Validates form inputs client-side (e.g., adding a stock, writing a personal note) before sending requests to the backend.
- **TailwindCSS** — Styling framework for a clean, consistent UI without writing custom CSS from scratch.

## UI/UX Details Not Covered in the Brief

- **Last Updated Timestamp** — Since prices are refreshed periodically (not real-time) due to free-tier API limits, each stock displays a "Last updated: X minutes ago" label, so users always know how fresh the data is instead of assuming it's live.
- **Static Personal Rules/Notes** — Each user can attach a short personal note to a stock in their watchlist (e.g., "Never skip a month," "Buy no more than ₱5,000/month"). This is purely a static text display — no reminders, no enforcement, no interactivity — just a personal reference note the user writes for themselves.
- **AI-Generated Stock Insight** — Below each stock's price chart, a short AI-generated summary appears: what the company does, its long-term (10-year) relevance, and general risks. This is clearly labeled with a tooltip/disclaimer: "AI-generated, for reference only — not financial advice. Please do your own research."
- **Market Hours Widget** — A small always-visible indicator showing whether the market is currently open or closed, displayed in both Philippine Time and US Market Time, so users don't need to calculate the time difference themselves.

## Future Features (Not in Current Build)

- **Dividend Information** — Automatically detected per stock: the system checks if a company pays dividends, and if so, displays the dividend yield/history; stocks that don't pay dividends simply won't show this section.
- **Monthly Drop Notifications** — A notification system (via Celery background jobs) that alerts users if a watched stock drops significantly within a month, with a simple label (e.g., "Down 8% this month").
- **Expanded Watchlist Tiers** — If moved beyond a free-tier API in the future, the 12-stock cap could be relaxed for users who want to track more.
