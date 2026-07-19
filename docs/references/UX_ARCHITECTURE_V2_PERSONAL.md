# Portfolio Manager — Personal Edition UX Architecture (v2)

**Scope change from v1:** this is not an enterprise/professional terminal. It is a single-user, personal, daily-use desktop app for one long-term investor. Every decision below is filtered through one test: *will this realistically get used weekly?* If a v1 idea fails that test, it's cut — not simplified, cut.

---

## 0. What Changed, and a Few Pushbacks

Before redesigning, three of your calls deserve a second look — not to overrule them, but because "personal app" doesn't automatically mean "remove," and I'd rather flag the trade-off than silently comply or silently ignore it.

**1. Tax — I'd split this decision rather than remove it wholesale.**
"Tax optimization" and a "Tax Lot Optimizer" are correctly cut — that's advisory/planning software, not a thing you check weekly. But **cost basis and realized gain/loss are not tax features, they're portfolio facts** — the same numbers your brokerage already shows you, and you need them the moment you're deciding whether to sell something. Removing the *concept* entirely means a holding's detail view can't answer "what would I owe/gain if I sold this today," which feels like a real personal-investor need, not an enterprise one. My recommendation: cut the standalone **Tax section, the optimizer, and any document/forms management** entirely (you're right that those are advisory, seasonal, not weekly) — but keep **unrealized/realized gain as a plain field on the Holdings and Transactions screens**, no dedicated section required. That satisfies your instruction (no Tax section exists) without quietly losing information you'll want.

**2. Notification Center — agreed, cut, but the underlying need doesn't disappear.**
You're right that a bell-icon notification center is overkill for one user checking one app daily. But you *are* asking for a Dividend Calendar, and "what's coming up this week" is exactly what a notification center exists to answer. Rather than building a notification system to serve one section, I've made the **Dashboard itself the answer** — a "This Week" panel surfaces upcoming dividends and any import that needs review, in place of alerts. Same information, zero extra infrastructure.

**3. Multi-user/household — correctly cut, and I'd go further.** Since this was already a single-user assumption glossed as "future scalability" in v1, removing it isn't a simplification of existing UI, it's just declining to build speculative infrastructure. Agreed with no changes needed.

**A cut I'm proposing that you didn't ask for: drop "Accounts" and "Reports" as top-level sidebar sections.**
- *Accounts* as its own nav item made sense for an enterprise tool tracking many clients/entities. For one person, "which account is this in" is a **filter on Holdings/Transactions**, not a destination you navigate to independently. Folding it into Portfolio removes a whole sidebar section without losing any capability.
- *Report Builder* as a dedicated screen assumes recurring, configurable, scheduled reporting — that's an enterprise/advisor pattern. A personal investor wants "export what I'm looking at right now," which I've turned into a contextual **Export** action on Analytics/Dividends screens instead of a section of its own.

Net effect: **v1 had 11 sidebar sections. v2 has 5.**

---

## 1. Sidebar Navigation

```
▾ DASHBOARD

▾ PORTFOLIO
    Holdings
    Transactions
    Accounts

▾ DIVIDENDS
    Overview
    Calendar
    History

▾ ANALYTICS
    Performance
    Allocation

  IMPORT
  SETTINGS
```

**Purpose:** get to any of the five things you actually do — check status, look at a holding, look at income, look at performance, or bring in new data — in one click, with nothing else competing for attention.

**Main widgets:** a fixed, non-collapsing list of 5 top-level items. Portfolio and Dividends expand to sub-views; Analytics expands to two; Import and Settings are flat singletons with no children.

**Layout:** left rail, ~200px wide, collapsible to an icon strip (`Ctrl+B`) for users who want more workspace width — kept from v1 because it costs nothing and some sessions (deep-diving one chart) genuinely want the space back.

**User workflow:** click a top-level item to open/focus its default view as a tab; click a sub-item to open that specific view. No item is ever more than two clicks from the sidebar.

**Keyboard shortcuts:**

| Action | Shortcut |
|---|---|
| Toggle sidebar | `Ctrl+B` |
| Jump to Dashboard | `Ctrl+1` |
| Jump to Portfolio (Holdings) | `Ctrl+2` |
| Jump to Dividends (Overview) | `Ctrl+3` |
| Jump to Analytics (Performance) | `Ctrl+4` |
| Jump to Import | `Ctrl+5` |

**Why each element exists:** every remaining item survives the weekly-use test directly. Nothing is here "because professional software has it" — Watchlists is gone because your portfolio *is* your watchlist (agreed, and it also removes an entire parallel data model — a security could previously exist as both a watchlist entry and a holding, which is a source of bugs, not just clutter); Tax, Notifications, and Reports are gone per §0; Accounts is gone as a top-level item because it's a filter, not a destination.

---

## 2. Dashboard

**Purpose:** answer "how am I doing, and is there anything I need to look at" in under 10 seconds, with zero clicks. This is the screen you'll open the most by an order of magnitude, so it earns the most restraint — nothing goes here that isn't true every single day.

**Main widgets:**

| Widget | Content |
|---|---|
| Net Worth header | Total value, day change ($ and %), since-inception return |
| Allocation snapshot | Small donut/bar — asset class or sector breakdown, click-through to Analytics → Allocation |
| Top movers | Today's 3–5 largest $ movers among your holdings |
| This Week panel | Upcoming dividend payments (next 7 days) + any pending import awaiting review — replaces the Notification Center per §0 |
| Recent transactions | Last 5–8 transactions, click-through to full Transaction list |

**Layout:**
```
┌───────────────────────────────────────────────────┐
│  Net Worth: $XXX,XXX      Today: +$XXX (+0.4%)      │
├───────────────────────────┬─────────────────────────┤
│  Allocation (donut)        │  This Week               │
│                             │  • AAPL div $12 — Wed    │
│                             │  • Import pending review │
├───────────────────────────┼─────────────────────────┤
│  Top Movers                 │  Recent Transactions     │
│  NVDA +2.1% ($312)          │  ...                     │
└───────────────────────────┴─────────────────────────┘
```

**User workflow:** open app → glance at net worth + This Week → click a mover or a dividend line to jump straight into Security detail or Dividends → close, or leave dashboard as the resting tab.

**Keyboard shortcuts:** `Ctrl+1` to return here from anywhere; `R` refreshes prices while focused (mirrors `Ctrl+R` global shortcut).

**Why each element exists:** Net worth and day change are the one number you actually check daily — everything else on the screen exists to answer the *next* question that number raises (why did it move → Top Movers; what's coming → This Week; what did I just do → Recent Transactions). Nothing configurable, no widget picker — a personal dashboard that requires setup before it's useful has failed at being a dashboard.

*Cut from v1:* no separate "Portfolio Overview" vs. Dashboard distinction — v1 had them as different screens under different sections; for one portfolio, there's no reason Dashboard and Portfolio Overview should be two different things.

---

## 3. Portfolio Section

The section you'll live in for anything hands-on: what you hold, what you did, where it sits.

### 3a. Holdings

**Purpose:** the definitive list of everything you currently own, with enough live context to decide whether to act on any position without leaving the screen.

**Main widgets:** sortable grid — Security, Quantity, Avg Cost, Current Price, Market Value, Unrealized Gain ($ and %), Day Change, Account (filterable), % of Portfolio. Row click opens Security Detail in a new tab; row expand (or a toggle) reveals lots without a separate screen.

**Layout:** single full-width grid, filter bar pinned above it (by account, by sector, search-within), no side panel by default — the grid *is* the screen, consistent with a spreadsheet-literate user's expectations.

**User workflow:** scan for anything red/notable → click into a specific holding for its chart/history → or select multiple rows for a quick comparison (kept from v1's Compare concept, but as a lightweight in-grid selection rather than a dedicated Portfolio Compare screen — for one person's own holdings, "compare" is really just "look at two rows side by side," not a standalone analytical mode).

**Keyboard shortcuts:** `Ctrl+2` opens Holdings; arrow keys navigate rows; `Enter` opens the selected row's Security Detail; `Ctrl+F` filters within the grid.

**Why each element exists:** every column answers a decision you'd actually make ("is this up or down," "how much of my portfolio is this," "what account is it in for withdrawal purposes"). No columns for metrics (beta, sector P/E, analyst ratings) that belong to research tools, not a personal ledger of what you own.

### 3b. Transactions

**Purpose:** the source-of-truth log of every buy, sell, dividend, and transfer — both for trusting your numbers and for quickly logging a trade you just made elsewhere.

**Main widgets:** chronological grid (Date, Type, Security, Quantity, Price, Amount, Account), filter bar, inline "New Transaction" entry (slide-in panel, not a separate screen — kept directly from v1, this pattern earns its place regardless of app scope).

**Layout:** identical grid pattern to Holdings for consistency — one navigation/interaction model across the app instead of a different paradigm per screen.

**User workflow:** most common path is `Ctrl+N` from *anywhere* in the app → fill Date/Type/Security/Quantity/Price → save → done in under 15 seconds without ever navigating to this screen at all. The screen itself is mainly for review/reconciliation and for editing a past entry.

**Keyboard shortcuts:** `Ctrl+N` new transaction (global); `Ctrl+D` duplicate selected row (useful for recurring buys); `Delete` removes a row (always confirms).

**Why each element exists:** this is the one place data integrity is non-negotiable — every number on Dashboard, Holdings, and Dividends is derived from this log, so it needs to be fast to add to and impossible to lose from. No "advanced" fields are hidden away here the way they might be in an enterprise import tool — fees, notes, and account are all one screen away, because for a personal ledger, friction on data entry is friction you'll feel every week.

### 3c. Accounts

**Purpose:** a light, purely organizational view — which brokerage/account holds what, and each account's balance — demoted from a top-level nav item (§0) to a tab within Portfolio since it's a filter/grouping concept, not a distinct activity.

**Main widgets:** simple list — Account name, type, current balance, holding count. Click an account filters Holdings/Transactions to it.

**Layout:** compact list, no grid complexity — this screen intentionally stays small.

**User workflow:** mainly used once per account when adding it, and occasionally to sanity-check "does Schwab's total match what I imported."

**Keyboard shortcuts:** none dedicated — this isn't a screen worth memorizing a shortcut for, which is itself evidence it's correctly demoted rather than top-level.

**Why each element exists:** you still need to know your accounts exist and reconcile them, but the *activity* of managing accounts is inherently low-frequency (add once, glance occasionally) — exactly the profile of something that shouldn't cost a sidebar slot.

---

## 4. Analytics Section

Cut down from v1's five screens (Performance, Allocation, Risk, Cash Flow, Scenario) to two. Here's the reasoning per cut, not just the result:

- **Risk Analysis (correlation matrices, VaR)** — this is genuinely advisor/institutional-grade analysis. A personal long-term investor checking weekly doesn't need a covariance matrix; if you ever want it, it's a good candidate for a future "advanced" toggle, not a permanent nav item today.
- **Cash Flow Analysis** — mostly overlaps with Dividends (income) and Transactions (contributions/withdrawals already visible there); a dedicated screen would just be re-slicing data you can already see, so it's folded in rather than duplicated.
- **Scenario/What-If** — a planning tool, not a weekly-use tool by nature (you use it before a decision, not on a schedule). Cut for now; worth reconsidering only if you find yourself wanting to model rebalancing regularly.

### 4a. Performance

**Purpose:** answer "am I actually beating just holding an index fund" — the single question that justifies tracking performance at all for a long-term investor.

**Main widgets:** time-weighted return chart with a benchmark overlay (S&P 500 by default, changeable), date-range selector (1M/3M/1Y/YTD/All/Custom), a small summary row (return %, vs. benchmark, best/worst period).

**Layout:** one large chart dominates the screen; the summary row sits above it, always visible without scrolling.

**User workflow:** open, glance at the line relative to the benchmark line, adjust date range occasionally, close. This is a look-and-leave screen, not a manipulate-heavy one.

**Keyboard shortcuts:** `Ctrl+4` opens Performance; number keys `1`/`3`/`Y` etc. could map to date-range presets while the chart has focus.

**Why each element exists:** the benchmark overlay is the whole point — a return number with nothing to compare it to doesn't answer the actual question you're asking every time you check performance.

### 4b. Allocation

**Purpose:** answer "is my portfolio still shaped the way I intend it to be" — the second question a long-term investor actually checks periodically.

**Main widgets:** breakdown by asset class, sector, and (if you hold any) geography — toggle between the three via tabs, not three separate screens. Click a slice to filter Holdings to it.

**Layout:** single chart area (donut or bar, your call — no color decisions made here per prior scope) with the breakdown-type toggle above it.

**User workflow:** open, check nothing has drifted uncomfortably, click through to Holdings if something looks off, close.

**Keyboard shortcuts:** none beyond navigation — this is a glance screen.

**Why each element exists:** three breakdown types as tabs (not three nav items) because they're the same question asked three ways, not three different activities.

---

## 5. Dividends Section

This is the new first-class citizen, and it deserves the most structural thought since it's the one genuinely new part of the app. Your list of ideas is good but is a feature list, not yet a screen list — several of those items are *views of the same data*, not separate screens. I've grouped them into three screens rather than eight to avoid rebuilding the exact sprawl you're trying to cut elsewhere.

| Your listed idea | Where it lives |
|---|---|
| Upcoming dividends | Overview + Calendar |
| Dividend history | History |
| Monthly / Annual dividend income | Overview (both, same screen — see below) |
| Dividend calendar | Calendar |
| Dividend growth | History (as a per-company trend, not a separate screen) |
| Dividend by company / by sector | Overview & History (as groupings/filters, not separate screens) |
| Yield on Cost | Overview + on each Holding row |
| Portfolio Dividend Yield | Overview |
| Dividend reinvestment tracking | History + Transactions (a DRIP is just a transaction type) |

### 5a. Overview

**Purpose:** the "how much income am I actually generating" screen — the dividend-investor equivalent of the Dashboard.

**Main widgets:**
- Monthly income bar chart (last 12 months) — the single most-checked dividend metric for someone tracking income
- Annual income total (this year vs. last year, plain comparison)
- Portfolio Dividend Yield (weighted average across holdings) and Yield on Cost side by side — deliberately paired, since the gap between the two *is* the story of your reinvestment/growth over time
- Income by company and by sector — two small breakdowns beneath the chart, not separate screens, since "who's paying me" is one glance, not a workflow

**Layout:**
```
┌───────────────────────────────────────────────────┐
│  Monthly Dividend Income (bar chart, 12mo)          │
├───────────────────────────┬─────────────────────────┤
│  This Year: $X,XXX          │  Yield: 2.1%             │
│  Last Year: $X,XXX          │  Yield on Cost: 3.4%     │
├───────────────────────────┼─────────────────────────┤
│  By Company (top 5)         │  By Sector               │
└───────────────────────────┴─────────────────────────┘
```

**User workflow:** open weekly-ish to watch the monthly bar chart grow, click a company/sector slice to filter History to it.

**Keyboard shortcuts:** `Ctrl+3` opens Dividends → Overview.

**Why each element exists:** Yield vs. Yield on Cost side-by-side is the one piece of "insight" I'd insist on keeping even under a simplicity mandate — it's not a vanity metric, it's the number that tells a long-term dividend investor whether their old buys are quietly outperforming their yield-at-purchase, which is the entire thesis of the strategy.

### 5b. Calendar

**Purpose:** "when is money arriving" — a literal calendar view, since dividend timing (ex-date, pay-date) is inherently a date-oriented question that a bar chart can't answer well.

**Main widgets:** month-grid calendar, each day showing expected/confirmed dividend payments; list view toggle for anyone who prefers a scannable list over a grid.

**Layout:** standard calendar grid, current month by default, with prev/next navigation; a compact list rendering as the alternate view (toggle, not a separate screen).

**User workflow:** mostly glanced at via the Dashboard's "This Week" panel; opened directly when you want to look further ahead than a week (e.g., "what's coming in next month").

**Keyboard shortcuts:** `←`/`→` to move between months while focused.

**Why each element exists:** this is the one item from your list that genuinely needs its own screen rather than folding into Overview — a calendar is a distinct interaction pattern (date-grid) that doesn't fit inside a dashboard-style card.

### 5c. History

**Purpose:** the detailed, filterable record — every dividend ever received, per company, with growth trend and reinvestment status. This is the "prove it" screen behind Overview's summary numbers.

**Main widgets:** grid (Date, Company, Amount, Type [cash/reinvested], Yield at time of payment), filterable by company/sector/date range; per-company view shows a small growth sparkline (dividend per share over time) when filtered to one company.

**Layout:** grid-first, consistent with Holdings/Transactions — same interaction model reused again rather than invented fresh.

**User workflow:** filter to one company after noticing something in Overview → see its full payment history and growth trend → done.

**Keyboard shortcuts:** `Ctrl+F` filters within grid, same convention as Holdings/Transactions.

**Why each element exists:** "dividend growth" from your list becomes a *filtered view* of History rather than its own screen, because growth-over-time for one company is exactly what a sparkline over the History grid already shows — a dedicated "Dividend Growth" screen would just be History with one company pre-selected.

**Note on reinvestment:** DRIP transactions are just Transactions with `Type = Reinvested Dividend`, already visible in Portfolio → Transactions. History surfaces them filtered/tagged for dividend-specific review, but there's deliberately no separate reinvestment-tracking data model — one transaction log, multiple views onto it, which is the same principle that eliminated Watchlists as a parallel structure.

---

## 6. Import Section

**Purpose:** get statement data into the app with confidence that nothing was mis-imported or silently dropped — this remains, unlike Reports, because bringing in real data is a distinct enough workflow (file selection, matching, review) to deserve its own screen, even for one user.

**Main widgets:** file picker + account selector (the only truly modal step — see below), followed by an inline Review list: matched rows (auto-accepted), new rows (highlighted), ambiguous rows (flagged, need your input — e.g., an unrecognized ticker or a possible duplicate).

**Layout:**
```
Step 1 (modal): Select file → Select account → Continue
Step 2 (tab, not modal): Review — grid of staged rows,
   grouped by status (New / Matched / Needs Review),
   Confirm Import button enabled once all "Needs Review" rows are resolved
```

**User workflow:** `Ctrl+I` → pick file/account → review staged rows (accept defaults, resolve flagged ones) → confirm → rows land in Transactions and Holdings/Dividends recompute immediately.

**Keyboard shortcuts:** `Ctrl+I` opens Import; `Enter` accepts the focused row's suggested match during review; `Ctrl+Enter` confirms the whole batch once ready.

**Why each element exists:** kept as a two-step modal-then-review pattern directly from v1 because the reasoning doesn't change with app scope — a personal user is exactly as harmed by a silent bad import as an enterprise one, arguably more so since there's no admin to catch it. The only real change from v1 is scale: no separate "Import Wizard" vs. "Import Review" *sections* — for one user's occasional imports, they're steps of one flow, not two destinations.

---

## 7. Settings

**Purpose:** the handful of things you set once and rarely touch again — deliberately the least designed-for screen in the app, because a settings screen you visit often is usually a sign something should have been a first-class feature instead.

**Main widgets (as tabs within one screen, not separate nav items):**
- **General** — base currency, date format, default landing screen (Dashboard vs. last-open tab)
- **Accounts & Connections** — add/remove/rename accounts (the actual CRUD; the Portfolio → Accounts tab is the *view*, this is the *management*)
- **Data & Backup** — local database location, manual backup/restore, no cloud sync (consistent with offline-first)
- **Shortcuts** — view/reassign keyboard shortcuts
- **About** — version, licenses

**Layout:** simple tabbed panel, no sidebar-within-sidebar.

**User workflow:** visited during initial setup, occasionally to add an account or trigger a backup, essentially never otherwise.

**Keyboard shortcuts:** none — consistent with the philosophy that infrequent screens don't need memorized shortcuts; reachable via Command Palette or a menu-bar item instead.

**Why each element exists:** every tab maps to a real, if infrequent, need (currency for correct math, accounts for data entry, backup for the offline-first promise, shortcuts because this whole app is keyboard-first). Nothing speculative (no "Appearance" theme system, no notification preferences, since there are no notifications to configure) — a settings screen with toggles for features that don't exist is worse than no settings screen at all.

---

## Summary — v1 → v2

| v1 (11 sections) | v2 (5 sections) | Disposition |
|---|---|---|
| Dashboard | Dashboard | Kept, merged with old "Portfolio Overview" |
| Portfolios | *(folded into Portfolio)* | Personal app has one portfolio, not many to manage |
| Accounts | Portfolio → Accounts | Demoted from top-level to a filter/tab |
| Transactions | Portfolio → Transactions | Kept |
| Holdings | Portfolio → Holdings | Kept |
| Analytics (5 screens) | Analytics (2 screens) | Risk & Scenario cut, Cash Flow folded into Dividends/Transactions |
| Watchlists | — | **Removed**, per your instruction — portfolio is the watchlist |
| Tax (3 screens) | — | **Removed** as a section; realized/unrealized gain kept as fields, not a screen |
| Reports | — | **Removed**, replaced by contextual Export actions |
| Import/Export | Import | Kept, Export made contextual instead of a destination |
| Settings | Settings | Kept, notification prefs removed (nothing to configure) |
| *(new)* | Dividends (3 screens) | **Added**, your core new requirement |

**Net result:** 11 sidebar sections and ~24 total screens in v1 → **5 sections and 12 screens in v2**, with a genuinely new, well-structured Dividends module rather than a flat list of 11 loosely-related dividend ideas.
