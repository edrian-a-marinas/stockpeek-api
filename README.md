# StockPeek — Project Brief

_This is the very first document. Written before any planning, before any tech decisions, before any roadmap. Just enough to decide: is this worth doing at all._

## The Problem

People who casually follow stocks often just want to check how a few companies are doing — without any intention of actually buying or selling right now. But the only way to do that today is by logging into a real brokerage or trading platform, the same account that holds actual money and real financial access.

That means every quick check-in — just to see if a stock went up or down — comes with the same login, the same exposure, and the same risk as if they were about to make a real trade. There's no lightweight way to just look, without opening the door to the account where real money lives.

## Who Has This Problem

Everyday casual stock watchers — people who follow a handful of companies out of interest, but don't trade often. This is especially relevant for people using shared or public devices, or anyone who simply prefers not to keep a trading account logged in or accessible more often than necessary.

## Concepts

A simple account lets users build and save a personal watchlist of up to 12 stocks, view current prices and price history, and remove stocks they no longer track — all without touching a real trading account, so the security risk of frequent brokerage logins simply doesn't apply. A market hours widget shows whether the market is open, in both Philippine and US time, so users know if the price they're seeing is live.


## How It Covers Everything

Since the account has no real money or trading functionality, there's nothing sensitive to protect beyond a simple login — directly removing the security exposure the Problem describes. Users get exactly what they need for casual monitoring: a personal watchlist, live-ish prices, and history charts, without ever going near an actual trading platform.

## Stacks:
Backend: Python, Django, PostgreSQL, MongoDB, Redis, Celery, Twelve Data API, LLM API
Frontend: TypeScript, React, Vite, TanStack (Query, Table), Zod, TailwindCSS

## Limitations of This Project

_(As built solo, with no real client.)_

- Intentionally excludes any trading, payment, or real brokerage connection — this is a viewing-only tool by design, not a financial platform, so it doesn't handle real transactions, portfolios, or account balances
- Stock data relies on a free-tier API with rate limits and periodic refresh (not true real-time), which is also why watchlists are capped at 12 stocks — keeping the number of tracked symbols manageable within free-tier request limits, and historical depth is limited compared to paid financial data providers
- The AI-generated stock insights (company overview, long-term relevance, risks) are for reference only, not financial advice — they're based on general AI knowledge, not licensed financial analysis, and should not be treated as investment guidance
