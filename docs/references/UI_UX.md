# UI_UX.md — Portfolio Manager (Personal Edition)
### Definitive Interaction & Design System Specification

**Status:** Developer-ready. Architecture is finalized per prior UX Architecture v2 (Personal). This document does not alter navigation, screen list, or scope — it specifies exactly how each finalized screen behaves and how the design system that skins them works.

**Out of scope for this document:** database schema, financial calculation logic, import/parsing algorithms. Where a spec references a value (e.g., "unrealized gain"), it assumes that value is supplied by the application layer and concerns itself only with how it's displayed and interacted with.

**Screen inventory this document covers** (matches the finalized sidebar exactly):

1. Dashboard
2. Portfolio → Holdings
3. Portfolio → Transactions
4. Portfolio → Accounts
5. Analytics → Performance
6. Analytics → Allocation
7. Dividends → Overview
8. Dividends → Calendar
9. Dividends → History
10. Import
11. Settings

---

## PART 1 — DESIGN SYSTEM

The design system is the shared vocabulary every screen below draws on. Screen specs reference these rules by name (e.g., "Primary Button," "Data Table") rather than re-describing them — the system exists specifically so no screen invents its own variant of a solved problem.

### 1.1 Typography Hierarchy

| Level | Role | Weight | Approx. size (pt) | Usage |
|---|---|---|---|---|
| Display | Net worth / hero numbers | Semibold | 28–32 | Dashboard net worth, single most important number on a screen — used once per screen, maximum |
| H1 | Screen title | Semibold | 20 | Top of every screen's content area (e.g., "Holdings") |
| H2 | Section/panel title | Semibold | 15 | Panel headers within a screen (e.g., "This Week," "By Sector") |
| H3 | Subsection / card title | Medium | 13 | Nested groupings, dialog section headers |
| Body | Default text | Regular | 13 | Table cells, form labels, descriptions |
| Body Emphasis | Emphasized body | Medium | 13 | Key table cells (e.g., gain/loss values), active states |
| Caption | Metadata, timestamps | Regular | 11 | "Last updated 2 min ago," column sub-labels, helper text |
| Numeric (tabular) | All financial figures | Regular/Medium | matches context | Always rendered in a tabular-figure (monospaced-digit) font variant so columns of numbers align vertically — this is a correctness rule, not a style preference, since misaligned decimal points in a financial grid are a legibility bug |

**Rules:**
- No more than 3 type levels visible on a single screen at once (e.g., Dashboard uses Display + H2 + Body — never introduces H1 mid-screen).
- Financial values never use Display or H1 styling outside the Dashboard net-worth header and Dividends Overview's income total — reserving the largest size for the one or two numbers per app that deserve it prevents every screen from shouting.
- Line height: 1.4× for body text, 1.2× for table rows (denser, since tables prioritize scanability of many rows over prose readability).

### 1.2 Spacing System

8px base unit, consistent across the app — no ad hoc spacing values anywhere in implementation.

| Token | Value | Usage |
|---|---|---|
| `space-1` | 4px | Icon-to-label gap, tight inline spacing |
| `space-2` | 8px | Default gap between related inline elements |
| `space-3` | 16px | Gap between form fields, table cell horizontal padding |
| `space-4` | 24px | Gap between distinct widgets/panels on a screen |
| `space-5` | 32px | Section-level separation (e.g., above a new H2 panel) |
| `space-6` | 48px | Screen-edge margins on wide viewports |

**Rules:**
- Table row height: 36px default (32px in "compact" density mode, a per-grid user toggle — see Table Design Rules).
- Toolbar height: fixed 44px across all screens.
- Sidebar width: 200px expanded / 56px icon-rail collapsed.

### 1.3 Card Design Rules

Used for: Dashboard panels, Dividends Overview panels, Settings tab content blocks.

- Corner radius: 8px.
- Padding: `space-4` (24px) on all sides.
- Border: 1px hairline, no drop shadow at rest — shadows are reserved for elevated/floating elements (popovers, dragged rows) so a shadow always means "this is temporarily above the surface," never decoration.
- A card always has exactly one H2 title at its top-left; actions (if any) align top-right of the same row.
- Cards never nest inside other cards.

### 1.4 Table (Data Grid) Design Rules

The single most-used component in the app (Holdings, Transactions, History, Accounts) — governed strictly for consistency.

- Header row: sticky on vertical scroll, `Body Emphasis` weight, sort indicator (▲/▼) rendered only on the active sort column.
- Row height: 36px default, 32px compact — user-togglable per grid via a density control in the toolbar, persisted per screen.
- Zebra striping: off by default (relies on hover/selection state instead — see 1.11/1.12) to keep grids calm at high row counts; may be enabled as a user preference in Settings → General.
- Numeric columns: right-aligned, tabular figures (1.1). Text columns: left-aligned. Date columns: left-aligned, consistent format from Settings → General.
- Gain/loss values: color-paired with a ▲/▼ glyph, never color alone (accessibility rule 1.13 / architecture §19).
- Column resize: drag column border, min width enforced per column to prevent truncating critical values (e.g., currency columns never shrink below width needed for the longest expected value).
- Column reorder: drag column header horizontally; column show/hide via right-click on header → checklist.
- Empty column state: em-dash (`—`), never a blank cell, so "no data" is visually distinct from "zero" (`0`/`$0.00` renders as an actual zero).

### 1.5 Dialog Design Rules

- Two types only, per architecture §12: **Modal** (destructive confirmations, irreversible settings, Import's file-selection step) and **Slide-in Panel** (Transaction Detail/Edit, New Transaction, filters).
- Modal max-width: 480px for confirmations, 640px for content dialogs (e.g., Import file/account selection). Always centered on the active window, dims background at 40% opacity.
- Modal always has: a title (H3), body content, and a right-aligned button row with **Cancel** (Secondary Button) left of the primary action (Primary or Destructive Button per 1.7).
- Slide-in Panel: fixed 400px width, slides from the right edge of the content area (not the whole window), pushes nothing — overlays with a light shadow, background remains visible and dimmed at 15% (light enough to still read context, per architecture §12's reasoning against fully blocking modals).
- Escape key closes any dialog/panel; unsaved-edit panels prompt via a small inline confirmation strip rather than a stacked second modal.

### 1.6 Form Design Rules

- Label position: above the field, `Body` weight, `space-1` gap to the field.
- Field height: 36px, matching table row height for visual rhythm consistency across the app.
- Required fields: no asterisk clutter — instead, the Save/Confirm button stays disabled until required fields are valid, with the first invalid field auto-focused on a failed submit attempt.
- Inline validation: appears on blur (not on every keystroke, which is distracting), red `Caption`-styled text directly under the field.
- Field grouping: related fields (e.g., Quantity + Price) sit on the same row when both are short numeric inputs; unrelated fields never share a row.
- Advanced/optional fields: collapsed behind a "Show more" text-link expander, never hidden in a separate tab within the same form (architecture §14's progressive disclosure applied at the component level).

### 1.7 Button Hierarchy

| Type | Usage | Visual |
|---|---|---|
| Primary | The one recommended action in a dialog/panel (Save, Confirm Import, Add Account) | Filled, highest contrast. Max one per dialog/panel. |
| Secondary | Alternative or dismissive action (Cancel, Back) | Outlined/ghost, same size as Primary |
| Destructive | Delete/remove actions | Filled, distinct from Primary (not by color choice here, but by requiring adjacent confirmation text — "Delete 3 transactions" — never a bare "Delete") |
| Tertiary / Text | Low-emphasis actions (Show more, Clear filter) | No border/fill, text-only, `Body Emphasis` |
| Icon Button | Toolbar actions, row-level quick actions | 32×32px hit target minimum even if the icon is smaller, for touch/precision tolerance |

**Rule:** every dialog and panel has exactly one Primary button. If a screen seems to need two equally-weighted actions, that's a signal the dialog is doing two jobs and should be split — flagged here as a design smell to watch for during implementation, not just a style rule.

### 1.8 Icon Usage

- Icon set: single consistent library across the app (implementation detail for the architect to select; this spec only governs usage rules).
- Icons always paired with a text label in the toolbar and menus at default window width (architecture §6); icon-only is permitted only in dense table row-actions and the collapsed sidebar rail, and always carries a tooltip.
- Icons never carry meaning alone for financial state (gain/loss, status) — always paired with color + text/glyph per 1.13.
- Consistent icon-to-glyph mapping is documented in a single icon registry file so the same concept (e.g., "export") never uses two different icons on different screens.

### 1.9 Status Indicators

| State | Treatment |
|---|---|
| Positive (gain, income up) | Green + ▲ + `+` prefix on the value |
| Negative (loss, income down) | Red/warm + ▼ + `-` prefix (never just parentheses, which is easy to miss at a glance) |
| Neutral / unchanged | Muted gray, no glyph |
| Pending (staged import row, unconfirmed transaction) | Amber dot + "Pending" `Caption` label |
| Needs attention (import row needing review, reconciliation mismatch) | Amber/orange left-border accent on the row, not a full-row fill (keeps the row's data legible while still standing out) |

### 1.10 Hover States

- Table rows: subtle background tint on hover (no border change, to avoid layout shift), cursor becomes pointer only over interactive cells (row itself, action icons).
- Buttons: 8% darken/lighten of base fill on hover, 150ms transition (see 1.14).
- Sidebar items: background tint + slight left-border accent on hover, distinct from the stronger accent used for the active/selected item.
- Chart data points: hover reveals a tooltip with exact value + date, never relies on a visible-at-rest data label that would clutter the chart.

### 1.11 Selection States

- Single row selection: full-row background tint (distinct, stronger than hover tint) + left-border accent bar.
- Multi-row selection: same tint applied to all selected rows; a persistent small toolbar/status strip appears above the table showing "{n} selected" with contextual bulk actions (matches architecture §18's bulk-operations pattern).
- Sidebar active item: filled background + left-border accent, persists regardless of hover elsewhere.
- Selection state survives sort/filter changes where the selected item is still present; if a filter removes the selected row from view, selection is cleared and the bulk-action strip disappears (no orphaned "1 selected" referring to an invisible row).

### 1.12 Keyboard Focus Rules

- Every interactive element has a visible focus ring (not just color — a 2px outline, so focus is legible for colorblind users per architecture §19) at all times when navigating via keyboard, including inside dense tables.
- Tab order follows visual/reading order (left-to-right, top-to-bottom) on every screen — verified per-screen at implementation time, never assumed from CSS/layout order.
- Focus is trapped within an open modal (Tab cycles only through the modal's controls) but is *not* trapped within a slide-in panel, since the panel is designed to coexist with the underlying screen rather than block it.
- On closing a dialog/panel, focus returns to the element that triggered it (e.g., closing a row's edit panel returns focus to that row), not to the top of the page.

### 1.13 Animation Guidelines

- Duration: 150ms for micro-interactions (hover, focus, button press), 250ms for structural transitions (slide-in panel open/close, tab switch fade).
- Easing: ease-out for things entering/appearing, ease-in for things leaving/dismissing — asymmetric timing so appearances feel snappy and dismissals feel settled rather than abrupt.
- No animation on data updates themselves (a price refreshing, a table re-sorting) beyond a brief (100ms) crossfade — financial figures changing should read as *updated*, not *animated*, to avoid any impression of manipulated/uncertain data.
- Respect OS-level "reduce motion" accessibility setting globally — all transitions above collapse to instant/near-instant (≤50ms) when that setting is on.
- Loading skeletons (architecture §17): a slow, subtle shimmer, never a spinner, for any first-paint load exceeding 300ms.

---

## PART 2 — SCREEN SPECIFICATIONS

---

### 2.1 Dashboard

**Purpose:** single-glance answer to "how am I doing and is there anything to look at," reachable with zero clicks after launch.

**Layout:** fixed 2×2-ish grid of cards below a full-width hero header (Net Worth). No user-configurable widget positions. Responsive down to a single column below ~900px width.

**Toolbar:** minimal — no contextual actions beyond a manual refresh icon button (right-aligned) and the persistent global zone (Search, Sync status, Settings) per the finalized architecture.

**Widgets:** Net Worth header (Display type), Allocation snapshot card, This Week card, Top Movers card, Recent Transactions card. Each is a Card (1.3) except the Net Worth header, which spans full width with no border/card treatment — it is the page, not a panel on the page.

**Tables:** Recent Transactions renders as a minimal table (no header row shown — 5–8 rows are self-evident without column labels reinforcing "Date / Type / Amount"); Top Movers is a compact list, not a full Table component.

**Context menus:** right-click on a Top Mover or Recent Transaction row surfaces a reduced menu — "Open," "Go to Security" / "Go to Transaction" only (no edit/delete here; Dashboard is read-oriented, per architecture §4 Journey A).

**Keyboard shortcuts:** `Ctrl+1` focuses/returns to Dashboard; `R` refreshes prices while the screen has focus (mirrors global `Ctrl+R`); arrow keys move focus between cards' primary rows for keyboard-only scanning.

**Mouse interactions:** click any row/slice to navigate (Allocation slice → Analytics/Allocation filtered; Mover/Transaction row → its detail); no drag interactions on this screen.

**Double-click behavior:** double-click a Top Mover or Recent Transaction row opens its detail in a *new* tab (single-click on this screen navigates the current tab; double-click is the "open in new tab" gesture consistently across the app — see 2.2 for the grid convention this mirrors).

**Right-click behavior:** see Context menus above; right-click on empty card space has no menu (nothing to act on).

**Drag & drop:** none on this screen.

**Empty states:** first-launch with zero accounts — the full card grid is replaced by a single centered panel: "Add your first account to see your portfolio here" with two Primary/Secondary buttons, *Import a Statement* and *Add Account Manually* (architecture §15). Once at least one account exists but has no transactions, cards render individually empty (e.g., This Week shows "Nothing scheduled this week" in Caption style) rather than blocking the whole dashboard.

**Loading states:** Net Worth and card contents render from local cache near-instantly (<100ms target, architecture §17); only the small "Last updated Xm ago" caption next to the refresh icon shows a live-fetch-in-progress pulse — no skeleton, no spinner, since cached data is already valid and displayed.

**Error states:** if a live price fetch fails, the affected values (Net Worth, Top Movers) show their last-known figures with a Caption note ("Prices as of [time], refresh failed") rather than an error banner — this is a non-blocking, informational-tier error (architecture §16 tier 1/2), never a dialog.

**Confirmation dialogs:** none — Dashboard performs no destructive actions directly.

**Toast notifications:** a brief toast confirms a manual refresh completed ("Prices updated"), auto-dismissing after 3s; no other toasts originate from this screen.

**Search/filter behavior:** none local to Dashboard; Global Search (`Ctrl+F`/`/`) and Command Palette (`Ctrl+K`) work identically here as everywhere.

**Sorting:** Top Movers is pre-sorted by absolute $ change descending, not user-sortable (it's a fixed-purpose summary, not a grid).

**Multi-selection behavior:** not applicable — no multi-select affordance on this screen.

**Navigation flow:** entry point for the whole app (default landing tab, configurable in Settings → General); exits into Security Detail, Transaction Detail, Analytics → Allocation, and Portfolio → Transactions depending on which card element was activated.

**Accessibility:** Net Worth header is announced as a single landmark heading; This Week list items are announced with their date and amount in one phrase ("AAPL dividend, twelve dollars, Wednesday") rather than three separate cell reads, since this card is a list, not a table, for assistive tech purposes.

**Developer implementation notes:** Dashboard should be implemented as a read-only aggregation view with no independent state beyond the manual-refresh trigger — it must never become a place where business logic or write operations live (Constitution: never place calculations inside widgets). All figures are pass-through renders of values computed by the application/domain layer.

---

### 2.2 Portfolio → Holdings

**Purpose:** definitive live list of everything currently owned, with enough context per row to decide whether to act, without leaving the screen.

**Layout:** full-width Data Table (1.4) below a slim filter bar; no side panel by default. Toolbar sits above the filter bar.

**Toolbar:** contextual zone (left): New Transaction, Import, density toggle (default/compact), Export (contextual, replaces v1's Report Builder per finalized architecture). Persistent zone (right): Search, Sync, Settings.

**Widgets:** filter bar (account dropdown, sector dropdown, free-text search-within-grid), the Holdings table itself, a summary strip pinned above the table showing selected-account or all-accounts total value (updates live with filters).

**Tables:** columns — Security, Quantity, Avg Cost, Current Price, Market Value, Unrealized Gain ($ / %), Day Change, Account, % of Portfolio. Default sort: Market Value descending. Row expand affordance (chevron, left of Security) reveals per-lot detail inline without navigating away.

**Context menus:** right-click a row:
```
Open Security
Add Transaction (Buy/Sell)…
─────────────
Compare With… (enabled only when 2+ rows selected)
─────────────
View Lots
─────────────
Hide from Dashboard
```
Right-click a column header: column show/hide checklist + "Reset columns."

**Keyboard shortcuts:** `Ctrl+2` opens Holdings; arrow keys navigate rows; `Enter` opens the focused row's Security Detail in the current tab; `Ctrl+Enter` opens it in a new tab; `Ctrl+F` focuses the in-grid filter; `Shift`/`Ctrl`+click or `Shift`+arrows extend selection.

**Mouse interactions:** single-click selects a row (no navigation on single-click, consistent with grid screens being review surfaces, distinct from Dashboard's summary rows); click the expand chevron reveals lots inline; click a column header sorts (click again reverses).

**Double-click behavior:** double-click a row opens Security Detail in a new tab — the universal grid convention across the app (Holdings, Transactions, History all share this).

**Right-click behavior:** see Context menus above.

**Drag & drop:** column reorder via header drag (1.4); no row drag-and-drop (holdings have no user-defined order to preserve).

**Empty states:** zero holdings with at least one account present — table area shows "No holdings yet in [Account/All Accounts]" with *Add Transaction* and *Import Statement* actions (architecture §15); zero holdings due to an active filter shows "No holdings match this filter" with a one-click *Clear filter* link, visually distinct from the true-empty case.

**Loading states:** table renders from local cache instantly; only the Current Price / Day Change columns show a per-cell subtle pulse if a live price fetch is in progress, never a full-table skeleton for an already-populated grid.

**Error states:** a row whose live price fetch failed shows its last-known price with a small amber dot on that cell (status indicator, 1.9) and a tooltip "Price as of [time]"; this never blocks sorting/interacting with the row.

**Confirmation dialogs:** none originate directly from this screen (Hide from Dashboard is reversible/non-destructive, no confirmation needed); Delete-type actions live on Transactions, not Holdings, since a holding is a derived position, not a directly deletable record.

**Toast notifications:** "Hidden from Dashboard" (with an Undo action) after that context-menu action; no other toasts native to this screen.

**Search/filter behavior:** in-grid filter matches security name/ticker as you type (debounced ~150ms), combinable with the account/sector dropdowns (AND logic); filter state persists per session but resets on app restart unless saved as a view (architecture §18).

**Sorting:** any column sortable, single-column sort only (no multi-column sort — unnecessary complexity for a personal-scale holdings list), indicator per 1.4.

**Multi-selection behavior:** `Shift`/`Ctrl`+click enables multi-select; selecting 2+ rows surfaces the bulk strip (1.11) with "Compare Selected" and "Export Selected" actions — no bulk-delete here (again, holdings aren't directly deletable).

**Navigation flow:** entered from Dashboard (Allocation slice, Top Mover), sidebar (`Ctrl+2`), or Global Search; exits to Security Detail (row open) or Analytics/Allocation (via the summary strip's "View allocation" link).

**Accessibility:** table exposes standard grid ARIA roles (row/cell/columnheader) so screen readers announce "row 3 of 42, Market Value, twelve thousand dollars" style navigation; expand chevrons are individually focusable and labeled "Expand lots for {security}."

**Developer implementation notes:** the summary strip must recompute reactively from the same filtered dataset the table displays — it should never be a separately-fetched aggregate that can drift out of sync with what's visibly filtered. Row expand (lots) should lazy-render its content only when first expanded, not pre-render for all rows, to keep large holdings lists performant.

---

### 2.3 Portfolio → Transactions

**Purpose:** the source-of-truth chronological log; fast to add to, safe to trust, easy to review/correct.

**Layout:** full-width Data Table below a filter bar, identical structural pattern to Holdings for consistency. The New Transaction Slide-in Panel (1.5) is the primary write surface, invocable from any screen.

**Toolbar:** contextual (left): New Transaction (Primary Button styling — this is the screen's, and arguably the app's, single most important action), Import, density toggle, Export. Persistent (right): standard.

**Widgets:** filter bar (account, type, date range, free-text search), the Transactions table, no summary strip (unlike Holdings — a running total of transactions isn't a meaningful number the way portfolio value is).

**Tables:** columns — Date, Type (Buy/Sell/Dividend/Reinvested Dividend/Transfer), Security, Quantity, Price, Amount, Account. Default sort: Date descending (most recent first — the natural reading order for a log).

**Context menus:** right-click a row:
```
Open Transaction
Edit…
Duplicate
─────────────
Go to Security
Go to Account
─────────────
Delete…          (Destructive, confirmation required)
```

**Keyboard shortcuts:** `Ctrl+2` then navigate to Transactions tab, or direct deep-link from Dashboard; `Ctrl+N` opens New Transaction panel from anywhere (global); `Ctrl+D` duplicates the selected row (pre-fills the panel with that row's values, date defaulted to today — built specifically for recurring buys); `Delete` deletes selected row(s), always confirms; `Ctrl+F` focuses in-grid filter.

**Mouse interactions:** single-click selects; double-click opens the row in the Edit Slide-in Panel (not a new tab — editing is the primary double-click intent here, distinct from Holdings/History where double-click opens Security Detail); column header click sorts.

**Double-click behavior:** opens Transaction Edit panel pre-populated, per above.

**Right-click behavior:** see Context menus.

**Drag & drop:** column reorder only; no row reordering (chronological order is derived from Date, not manually set).

**Empty states:** zero transactions in an otherwise-populated account — "No transactions in [Account] yet" with *Import Statement* / *Add Transaction* actions; filtered-to-empty shows the distinct "no matches, clear filter" pattern shared with Holdings.

**Loading states:** instant from local cache; no loading state applies to this screen beyond initial app launch (transactions are never live-fetched, only imported/entered).

**Error states:** a failed save from the New/Edit panel keeps the panel open with the user's entries intact and shows the specific field-level error (1.6) — never discards a partially-entered transaction (Constitution: never silently discard user data).

**Confirmation dialogs:** Delete — Modal, states "Delete this transaction?" with the transaction's date/security/amount restated in the body so the user confirms the *right* row, not just "are you sure" in the abstract; bulk delete states the count and a brief list (up to 5 rows, "+N more") of what's being removed.

**Toast notifications:** "Transaction added" / "Transaction updated" / "Transaction deleted" (with Undo for delete, 5s window) after each successful action from the panel or context menu.

**Search/filter behavior:** in-grid filter matches security, account name, and free-text comment field; date-range filter uses the same preset pattern as Analytics (1M/3M/1Y/YTD/All/Custom) for consistency.

**Sorting:** any column, single-column sort, defaults to Date descending as noted; re-sorting doesn't affect New Transaction's insertion point (new rows always land chronologically correctly regardless of current sort/filter view).

**Multi-selection behavior:** `Shift`/`Ctrl`+click; bulk strip surfaces "Delete Selected" (Destructive) and "Export Selected" only — no bulk-edit of transaction fields (editing many transactions' amounts at once is a data-integrity risk disproportionate to the convenience for a personal-scale ledger).

**Navigation flow:** entered from Dashboard (Recent Transactions), sidebar (`Ctrl+2` → Transactions tab), Holdings/Security Detail ("Go to Transactions"), or Import (post-confirmation). Exits to Security Detail, Account detail, or stays as the working screen during manual entry sessions.

**Accessibility:** New Transaction panel is fully keyboard-navigable field-to-field via Tab, with the Security field's autocomplete list navigable via arrow keys + Enter to select, matching standard combobox ARIA pattern.

**Developer implementation notes:** the New/Edit Transaction panel is a single shared component (form fields, validation, save logic) used both for creation and editing, differing only in initial field state and the verb on the Primary Button ("Add" vs. "Save") — do not fork this into two implementations. Duplicate should reuse the same component with a pre-filled, still-editable state, not a separate "quick add" path.

---

### 2.4 Portfolio → Accounts

**Purpose:** lightweight organizational view of which accounts exist and their current balance; intentionally the smallest screen in Portfolio.

**Layout:** simple vertical list (not a full Data Table — no sort/filter chrome needed at personal-account-count scale), each row a compact card-like strip.

**Toolbar:** contextual (left): Add Account only. No Export, no density toggle — this screen doesn't carry a table.

**Widgets:** the account list itself; no summary/aggregate widget (portfolio-level totals already live on Dashboard, not duplicated here).

**Tables:** not applicable — see list format above. Each row shows: Account name, Type (brokerage/bank/etc.), Current Balance, Holding Count.

**Context menus:** right-click an account row:
```
Open Account (filters Holdings/Transactions to it)
Rename…
─────────────
Import Statement…
─────────────
Archive Account
```
(Delete is intentionally absent from the quick menu — deleting an account with transaction history is a rare, high-consequence action routed through Settings → Accounts & Connections instead, per architecture's reasoning that destructive/rare actions shouldn't clutter a frequently-visited context menu; this screen's row-level menu favors the common cases.)

**Keyboard shortcuts:** none dedicated, consistent with the finalized architecture's decision that this low-frequency screen doesn't warrant memorized shortcuts.

**Mouse interactions:** click a row filters Portfolio → Holdings and Transactions to that account and navigates there; no in-place expansion.

**Double-click behavior:** same as single-click (navigate) — this list has no secondary "open vs. edit" distinction worth making with a double-click.

**Right-click behavior:** see Context menus.

**Drag & drop:** manual reordering of accounts via drag handle, purely cosmetic (display order only, no functional effect) — included because a user with several accounts will likely want their primary brokerage listed first.

**Empty states:** zero accounts — "No accounts yet" with a Primary *Add Account* button, and a secondary *Import a Statement* (which prompts for account creation as part of the flow if none exists) — consistent messaging with Dashboard's first-launch state.

**Loading states:** instant, local data only.

**Error states:** none specific to this screen beyond generic save failures, handled via inline Rename-field validation (name required, must be unique).

**Confirmation dialogs:** Archive Account — Modal, explains that archiving hides the account from active views without deleting its transaction history, distinguishing it clearly from delete (which lives in Settings and requires typing the account name to confirm, given its irreversibility).

**Toast notifications:** "Account added," "Account renamed," "Account archived" (with Undo for archive).

**Search/filter behavior:** none — list is short enough by design that filtering would be over-engineering for this screen's scale.

**Sorting:** manual (drag) order only, per Drag & Drop above; no column-sort concept since this isn't a table.

**Multi-selection behavior:** not applicable.

**Navigation flow:** entered from Portfolio sidebar tab or Settings → Accounts & Connections ("View accounts" link); exits to filtered Holdings/Transactions.

**Accessibility:** list items are focusable and activate on Enter, matching a standard listbox pattern; drag-reorder has a keyboard equivalent (select row, `Alt+↑`/`Alt+↓` to move) so reordering isn't mouse-only.

**Developer implementation notes:** this screen should read from the same Account entity Settings → Accounts & Connections manages — it is a *view* of that data, not a parallel store, matching the "one transaction log, multiple views" principle applied elsewhere in the architecture.

---

### 2.5 Analytics → Performance

**Purpose:** answer whether the portfolio is outperforming a simple benchmark — a look-and-leave screen, not a manipulate-heavy one.

**Layout:** single dominant chart area beneath a fixed summary row; date-range control sits above the chart, right-aligned.

**Toolbar:** contextual (left): benchmark selector (dropdown, default S&P 500), Export (chart image + underlying data as CSV). Persistent (right): standard.

**Widgets:** summary row (Return %, vs. Benchmark delta, Best/Worst period — three compact stat blocks), the performance line chart with benchmark overlay, date-range preset control (1M/3M/1Y/YTD/All/Custom).

**Tables:** none primary; an optional "View as table" toggle beneath the chart reveals the underlying period-by-period return data in a minimal Data Table for users who want exact figures rather than reading them off the chart.

**Context menus:** right-click within the chart area: "Export chart as image," "View as table," "Copy value at cursor" (when right-clicking near a specific data point).

**Keyboard shortcuts:** `Ctrl+4` opens Performance; number-key presets (`1`=1M, `3`=3M, `Y`=YTD, `A`=All) apply while the chart has focus; arrow keys scrub the cursor along the chart when focused, announcing the value at each point (accessibility, see below).

**Mouse interactions:** hover reveals a crosshair + tooltip (date, portfolio return, benchmark return) per Design System 1.10; click-drag on the chart selects a custom range and updates the date-range control to match.

**Double-click behavior:** double-click the chart resets zoom/range to the currently selected preset (undoes a click-drag custom selection).

**Right-click behavior:** see Context menus.

**Drag & drop:** click-drag range selection only, as above; no other drag interactions.

**Empty states:** insufficient history (fewer than 2 priced data points) — chart area replaced by an explicit message: "Performance requires at least one priced holding over more than one day," never a blank/broken chart render (architecture §15's explicit reasoning against ambiguous emptiness).

**Loading states:** chart recomputation for a large date range (e.g., "All," multi-decade) shows a determinate progress state only if genuinely slow; otherwise near-instant from cached daily computed values — this screen should not need a spinner in normal operation.

**Error states:** if the benchmark's external price data failed to load, the portfolio line still renders with a Caption note ("Benchmark data unavailable, showing portfolio only") rather than blocking the whole chart.

**Confirmation dialogs:** none.

**Toast notifications:** "Chart exported" after a successful image/CSV export.

**Search/filter behavior:** not applicable beyond the benchmark selector, which is a dropdown, not a search field.

**Sorting:** not applicable (chronological chart, not a sortable list); the optional table view sorts by date descending by default, user-resortable.

**Multi-selection behavior:** not applicable.

**Navigation flow:** entered via sidebar (`Ctrl+4`) or Dashboard's Allocation-adjacent context; this screen is largely terminal (no further drill-down beyond the optional table view) by design — performance is a summary metric, not a navigation hub.

**Accessibility:** the chart exposes a keyboard-navigable data-point mode (arrow keys move a focus indicator between data points, each announced with date + value) so the chart's information is not mouse-hover-only; the "View as table" toggle exists partly *for* accessibility, giving a fully standard table-based alternative to the visual chart.

**Developer implementation notes:** the benchmark overlay must share the exact same date-range and normalization basis as the portfolio line (both indexed to the same start point) — a benchmark comparison with mismatched bases would be a correctness bug, not a display nuance, so this should be validated in the data layer, not assumed correct because the chart "looks right."

---

### 2.6 Analytics → Allocation

**Purpose:** answer whether the portfolio's shape still matches intent — asset class, sector, or geography breakdown.

**Layout:** single chart area (donut or bar — color/visual-type decision deferred per prior scope notes) with a breakdown-type tab control directly above it.

**Toolbar:** contextual (left): breakdown-type tabs (Asset Class / Sector / Geography), Export. Persistent (right): standard.

**Widgets:** the allocation chart, a small legend/list beside or below it showing each segment's label, $ value, and %, sorted largest-to-smallest.

**Tables:** the legend list doubles as a minimal table (Segment, Value, %) — no separate Data Table component needed for a screen with this few rows per breakdown.

**Context menus:** right-click a chart segment or legend row: "View holdings in this segment" (navigates to Holdings, pre-filtered), "Export."

**Keyboard shortcuts:** `Ctrl+4` then Allocation tab (or direct deep-link); `←`/`→` cycles the breakdown-type tabs while the screen has focus.

**Mouse interactions:** click a chart segment or legend row filters/navigates to Holdings for that segment (matches architecture's stated click-through behavior); hover highlights the corresponding segment and legend row simultaneously (linked hover, standard chart-legend pairing).

**Double-click behavior:** same as click — no distinct double-click behavior on this screen, since single-click already navigates and there's no "select without navigating" state worth preserving here.

**Right-click behavior:** see Context menus.

**Drag & drop:** none.

**Empty states:** a breakdown type with no applicable data (e.g., Geography when no holdings have geography metadata) shows "No geography data available for current holdings" rather than an empty chart, and the tab itself shows a subtle disabled/muted state if it would always be empty for this portfolio.

**Loading states:** instant from cached holdings data; no meaningful loading state expected.

**Error states:** not applicable beyond the general empty-state handling above — allocation is computed entirely from local holdings, no external dependency to fail.

**Confirmation dialogs:** none.

**Toast notifications:** "Chart exported" on export, matching Performance's pattern.

**Search/filter behavior:** none local; the breakdown-type tabs serve the equivalent role of a filter here.

**Sorting:** legend list is sorted by value descending, fixed (not user-resortable — the visual chart's segment order should match the legend's order 1:1, and re-sorting one without the other would break that pairing).

**Multi-selection behavior:** not applicable.

**Navigation flow:** entered via sidebar or Dashboard's allocation snapshot card; exits to Holdings (filtered) on segment click.

**Accessibility:** each chart segment is individually focusable and announces "{segment}, {value}, {percent} of portfolio" — the legend list provides the same information in standard list form as a non-visual fallback, mirroring Performance's table-view accessibility pattern.

**Developer implementation notes:** the three breakdown types should share one chart-rendering component parameterized by grouping dimension, not three separate chart implementations — this is the kind of screen where under-abstracting leads to three slightly-diverging copies of the same logic over time.

---

### 2.7 Dividends → Overview

**Purpose:** the dividend-investor's dashboard — "how much income am I generating," the most-checked screen in this section.

**Layout:** Card grid, structurally identical pattern to the main Dashboard (1.3): full-width Monthly Income chart card on top, a two-stat row (This Year / Last Year, Yield / Yield on Cost) beneath, then By Company / By Sector cards side by side.

**Toolbar:** contextual (left): Export. Persistent (right): standard.

**Widgets:** Monthly Income bar chart (12mo trailing), Annual comparison stat block, Yield + Yield on Cost paired stat block, By Company top-5 list, By Sector breakdown list.

**Tables:** By Company and By Sector render as compact lists (name, $ amount, small bar or %), not full Data Tables — consistent with their role as glanceable summaries that link out to the full History screen for detail.

**Context menus:** right-click a By Company row: "View full history for {company}" (navigates to History, pre-filtered).

**Keyboard shortcuts:** `Ctrl+3` opens Dividends → Overview.

**Mouse interactions:** click any bar in the Monthly Income chart to jump to History filtered to that month; click a By Company/By Sector row to filter History accordingly; hover on chart bars shows exact $ and count-of-payments tooltip.

**Double-click behavior:** not distinct from single-click on this screen (same reasoning as Allocation, 2.6).

**Right-click behavior:** see Context menus.

**Drag & drop:** none.

**Empty states:** no dividend-paying holdings yet — the whole screen collapses to a single centered message: "No dividend income yet — dividends will appear here automatically once you hold an income-paying security," no false-zero charts rendered.

**Loading states:** instant, computed from local transaction/holdings data.

**Error states:** not applicable — fully local computation, no external dependency.

**Confirmation dialogs:** none.

**Toast notifications:** "Chart exported" on export, consistent with Analytics screens.

**Search/filter behavior:** none local to this screen; it is a fixed summary, with drill-down handled by navigating to History.

**Sorting:** By Company/By Sector lists sorted by $ amount descending, fixed.

**Multi-selection behavior:** not applicable.

**Navigation flow:** entered via sidebar (`Ctrl+3`) or Dashboard's This Week panel; exits to History (filtered by month/company/sector) on any click-through.

**Accessibility:** Yield and Yield on Cost stat block is announced as a paired comparison ("Yield 2.1 percent, Yield on Cost 3.4 percent") rather than two disconnected numbers, since their relationship is the point (per the prior architecture note on this pairing).

**Developer implementation notes:** Monthly Income figures must be computed on payment date, not ex-date or declaration date, and this convention should be documented at the data layer so History and Overview never disagree about which month a given payment belongs to.

---

### 2.8 Dividends → Calendar

**Purpose:** literal date-oriented view of upcoming (and past) dividend payments — the one dividend screen that earns a non-list interaction pattern.

**Layout:** standard month-grid calendar, current month by default; a list-view toggle (top-right of the toolbar) renders the same data as a scannable chronological list for users who prefer it.

**Toolbar:** contextual (left): list/calendar view toggle, month navigation (◀ Month ▶), "Today" jump button. Persistent (right): standard.

**Widgets:** the calendar grid itself (or list, depending on toggle); each day cell shows up to 3 payment entries with a "+N more" overflow.

**Tables:** the list-view alternative is a simple two-column list (Date, Payment details), not a full Data Table — filtering/sorting chrome would be excessive for what's fundamentally a chronological schedule.

**Context menus:** right-click a payment entry (in either view): "View security," "View full dividend history for this company."

**Keyboard shortcuts:** `←`/`→` moves between months (or scrolls the list view); `T` jumps to today; `Ctrl+3` then Calendar tab to enter this screen.

**Mouse interactions:** click a day cell with entries expands a small popover listing all payments that day (avoids needing to navigate away just to see an overflowed day); click an individual payment entry navigates to its Security Detail.

**Double-click behavior:** not distinct from single-click for payment entries; double-click on an empty day cell has no action (no "add event" concept here — dividends are derived data, not user-created calendar entries).

**Right-click behavior:** see Context menus.

**Drag & drop:** none.

**Empty states:** a month with no scheduled/received payments shows a plainly empty calendar grid with a small centered Caption ("No dividends this month") rather than any error-like treatment — an empty month is a completely normal, expected state for this screen, not a fallback to explain away.

**Loading states:** instant, local computation; month navigation has no perceptible loading delay.

**Error states:** not applicable — fully local.

**Confirmation dialogs:** none.

**Toast notifications:** none originate from this screen.

**Search/filter behavior:** none — a calendar is browsed, not searched; finding a specific past payment is what History (2.9) is for.

**Sorting:** not applicable (chronological by nature).

**Multi-selection behavior:** not applicable.

**Navigation flow:** entered via sidebar (`Ctrl+3` → Calendar tab) or Dashboard's This Week panel ("View full calendar" link); exits to Security Detail on payment click.

**Accessibility:** calendar grid uses standard grid/date-picker ARIA patterns; each day cell announces its date and payment count ("July 23rd, 2 dividend payments") on focus, with arrow-key navigation between days matching standard calendar-widget conventions.

**Developer implementation notes:** "upcoming" entries (not yet paid) and "received" entries (already paid) should be visually distinguishable within the same day cell (e.g., via the Pending status indicator, 1.9) so a user glancing at the current month can immediately tell what's already happened vs. what's still expected.

---

### 2.9 Dividends → History

**Purpose:** the detailed, filterable, provable record behind Overview's summary numbers — every dividend ever received.

**Layout:** full-width Data Table below a filter bar, same structural pattern as Holdings/Transactions. When filtered to a single company, a small growth sparkline card renders above the table.

**Toolbar:** contextual (left): filter-by company/sector dropdowns are part of the filter bar rather than the toolbar itself; toolbar carries density toggle and Export. Persistent (right): standard.

**Widgets:** filter bar (company, sector, date range, type: cash/reinvested), optional per-company growth sparkline card, the History table.

**Tables:** columns — Date, Company, Amount, Type (Cash / Reinvested), Yield at Payment. Default sort: Date descending.

**Context menus:** right-click a row:
```
Open Security
Go to Transaction        (jumps to the underlying Transactions row)
─────────────
Filter to this Company
Filter to this Sector
```
(No Edit/Delete here — dividend records are derived from Transactions, so corrections happen there per the "one log, multiple views" principle; this menu reflects that by omission rather than offering an action that would need to write back to a different entity.)

**Keyboard shortcuts:** `Ctrl+3` then History tab; `Ctrl+F` focuses in-grid filter; arrow keys + `Enter` navigate/open rows, matching Holdings/Transactions conventions.

**Mouse interactions:** single-click selects; column header click sorts; clicking the company name within a row filters the whole table to that company and reveals the sparkline card (a lighter-weight interaction than fully navigating away).

**Double-click behavior:** double-click a row opens the underlying Transaction in its Edit panel (consistent with Transactions' double-click convention, since a dividend history row *is* a transaction) rather than opening Security Detail — this is the one grid in the app where double-click intentionally diverges from Holdings' "open Security" convention, because for a dividend record the more useful default action is inspecting/correcting the underlying entry.

**Right-click behavior:** see Context menus.

**Drag & drop:** column reorder only, per the standard Data Table rules.

**Empty states:** no dividend history at all — same messaging pattern as Overview's empty state; filtered-to-empty (e.g., a company filter with no matches) uses the standard "no matches, clear filter" pattern shared across all grid screens.

**Loading states:** instant, local data.

**Error states:** not applicable — fully local computation.

**Confirmation dialogs:** none originate here (corrections happen via Transactions).

**Toast notifications:** "Filtered to {company}" is intentionally *not* a toast — filter changes are reflected directly in the visible filter bar state, and a toast for every filter click would be noise; only Export produces a toast ("Exported {n} records").

**Search/filter behavior:** in-grid filter combines company/sector dropdowns with free-text and date range, AND logic, matching Holdings/Transactions patterns for consistency.

**Sorting:** any column, single-column sort, defaults to Date descending.

**Multi-selection behavior:** `Shift`/`Ctrl`+click for Export Selected only; no bulk actions beyond export, since this screen doesn't support direct edits.

**Navigation flow:** entered via sidebar, Overview (chart bar / company row click-through), or Calendar (payment entry's "view full history" menu item); exits to Security Detail or the underlying Transaction's Edit panel.

**Accessibility:** identical grid ARIA pattern to Holdings/Transactions (1.4-governed); the per-company sparkline card, when shown, includes a text summary ("Dividend per share grew from $0.82 to $1.04 over 3 years") as a non-visual equivalent to the trend line.

**Developer implementation notes:** "Reinvested" type rows must link to their corresponding Buy transaction (the reinvestment purchase) so "Go to Transaction" resolves unambiguously — this is a data-relationship requirement flowing directly from the UX decision to treat DRIP as a transaction type rather than a separate model, flagged here so it's implemented as a proper reference rather than inferred by matching date/amount at query time.

---

### 2.10 Import

**Purpose:** bring statement data in with confidence nothing is mis-imported or silently dropped — a two-step flow (Modal selection → tab-based Review), not a single screen, per the finalized architecture.

**Layout — Step 1 (Modal, per Dialog Rules 1.5):** file picker control, account selector dropdown (with "+ New Account" inline option), Continue (Primary) / Cancel (Secondary).

**Layout — Step 2 (Review tab):** three grouped sections stacked vertically — "Needs Review" (top, expanded by default), "New" (collapsible, expanded by default), "Matched" (collapsible, collapsed by default since these need no action) — each a mini Data Table.

**Toolbar (Review tab):** contextual (left): "Confirm Import" (Primary Button, disabled until all Needs Review rows are resolved), "Cancel Import" (Secondary/Destructive-adjacent — discards the staged batch entirely). Persistent (right): standard.

**Widgets:** the three grouped staging tables; a running count summary ("48 matched · 5 new · 3 need review") pinned above them.

**Tables:** each group shares one column set — Date, Type, Security, Amount, Account, Status/Suggested Match — with "Needs Review" rows additionally showing an inline resolution control (a dropdown to confirm/correct the suggested security match, or mark as a duplicate to skip).

**Context menus:** right-click a "Needs Review" row: "Accept suggested match," "Mark as duplicate (skip)," "Edit before import…" (opens a lightweight inline editor for that staged row only, not the full Transaction panel, since it isn't a real transaction yet).

**Keyboard shortcuts:** `Ctrl+I` opens Import (Step 1 modal) from anywhere; within Review, `Enter` accepts the focused row's suggested match; `Ctrl+Enter` confirms the whole batch once eligible; `Esc` on the Review tab prompts "Discard this import?" rather than silently closing (data-loss-prevention, consistent with Constitution: never silently discard user data).

**Mouse interactions:** click a group header to expand/collapse it; click a Needs Review row's resolution dropdown to resolve inline without leaving the table.

**Double-click behavior:** double-click a Matched or New row (no action needed) shows a read-only preview of what will be created; double-click a Needs Review row opens the "Edit before import" inline editor directly (shortcut to the context-menu action).

**Right-click behavior:** see Context menus.

**Drag & drop:** the Step 1 file picker accepts drag-and-drop of a statement file directly onto the modal, in addition to the standard file-browser button — this is the one meaningful drag target in the app, since it mirrors how users already handle files in the OS.

**Empty states:** not applicable in the traditional sense — if a selected file produces zero parseable rows, the Review tab shows a direct message ("No transactions could be read from this file") with an option to try a different file, rather than opening an empty Review screen.

**Loading states:** file parsing (Step 1 → Step 2 transition) shows a brief determinate or indeterminate progress indicator scoped to the transition itself, not a full-app loading state; large files use a determinate progress bar if parse time is expected to exceed ~1s.

**Error states:** an unparseable/corrupted file is a Tier 3 (blocking) error per architecture §16 — shown as a Modal explaining the file couldn't be read, with a "Copy diagnostic details" option, and critically: the original file is untouched and nothing is staged, so retrying costs nothing.

**Confirmation dialogs:** "Cancel Import" (mid-review) — Modal, "Discard {n} staged rows? Nothing has been saved yet." — Destructive-styled Confirm, Secondary Cancel; "Confirm Import" itself does not require a second confirmation dialog, since the Review tab's entire purpose *is* the confirmation step (a second modal on top of it would be redundant friction the architecture specifically avoids per §12's reasoning).

**Toast notifications:** "Imported 53 transactions" (with a "View in Transactions" action) on successful confirm; this is the definitive success signal for the whole flow.

**Search/filter behavior:** a lightweight in-grid search within the Review tables (matches security/account) for statements large enough to warrant it; not present in Step 1.

**Sorting:** Review tables sort by Status-group first (fixed structural grouping, not a user sort choice) then Date descending within each group.

**Multi-selection behavior:** multi-select within "Needs Review" enables "Accept All Suggested" as a bulk action — the one true bulk-resolve shortcut in this flow, since resolving rows one-by-one on a large statement would otherwise be tedious.

**Navigation flow:** entered via `Ctrl+I`, sidebar Import item, Dashboard's This Week panel (if an import is left pending), or Accounts' "Import Statement…" context menu item (pre-fills the account selector); exits to Transactions (via toast link) or back to whatever screen was active before Import was invoked, on cancel.

**Accessibility:** the three-group Review structure uses proper heading levels (H2 per group) and each group's expand/collapse state is announced; the inline resolution dropdown is a standard combobox, keyboard-operable without leaving row focus.

**Developer implementation notes:** staged rows must exist only in an in-memory/transient state until "Confirm Import" — nothing should be written to the persistent store during Review, so that closing the app or canceling mid-review is guaranteed to leave zero partial writes, which is the concrete mechanism behind the "never silently discard/corrupt data" principle for this specific flow.

---

### 2.11 Settings

**Purpose:** the small set of things configured once and rarely revisited — deliberately the least visually elaborate screen in the app.

**Layout:** tabbed panel (tabs: General, Accounts & Connections, Data & Backup, Shortcuts, About) within a single screen — no sidebar-within-sidebar, no nested navigation.

**Toolbar:** none — Settings has no contextual toolbar actions; each tab's actions live inline within its content (e.g., "Add Account" button within the Accounts & Connections tab itself).

**Widgets by tab:**
- **General:** base currency dropdown, date format dropdown, default landing screen dropdown (Dashboard / Last-open tab), table density default (Default/Compact), zebra-striping toggle.
- **Accounts & Connections:** the account CRUD list (add/rename/archive/delete — the management surface behind Portfolio → Accounts' lighter view).
- **Data & Backup:** local database file location (read-only display + "Reveal in Finder/Explorer"), "Back Up Now" button, "Restore from Backup…" button, last-backup timestamp.
- **Shortcuts:** a searchable list of every keyboard shortcut in the app with an inline "Reassign" control per row.
- **About:** version number, license info, "Check for Updates" button.

**Tables:** Accounts & Connections and Shortcuts both render as simple lists/tables but without the full Data Table chrome (no column resize/reorder — these are short, fixed-structure lists).

**Context menus:** right-click an account row in Accounts & Connections: "Rename," "Archive," "Delete Account…" (Destructive, the one place full account deletion lives, per 2.4's reasoning).

**Keyboard shortcuts:** none dedicated to reach this screen (reachable via Command Palette or menu bar only, consistent with the finalized architecture's stance that infrequent screens don't need memorized shortcuts); within the Shortcuts tab, clicking "Reassign" then pressing any key combination captures it live.

**Mouse interactions:** standard form controls throughout; clicking a tab switches content with a brief fade (1.14's structural-transition timing).

**Double-click behavior:** not applicable — no grid-style rows with a distinct double-click action on this screen.

**Right-click behavior:** see Context menus (Accounts & Connections only).

**Drag & drop:** none.

**Empty states:** not applicable — every tab has fixed, always-present content (even zero accounts still shows the Accounts & Connections management UI with an "Add Account" prompt, not a blank tab).

**Loading states:** instant; the one exception is "Back Up Now," which shows a determinate progress state for the backup operation itself.

**Error states:** a failed backup shows an inline error directly in the Data & Backup tab (not a toast, since this is important enough to persist until acknowledged) with a retry action and a "Copy diagnostic details" option, matching the Tier 3 error pattern used for Import failures.

**Confirmation dialogs:** Delete Account — Modal, requires typing the account name to confirm (the one place in the app that uses type-to-confirm, reserved for this specifically because it's the single most irreversible action available: deleting an account deletes its full transaction history); Restore from Backup — Modal warning that current data will be replaced, Destructive-styled confirm.

**Toast notifications:** "Settings saved" is intentionally *not* shown for every field change (settings auto-save on change, per standard desktop-app convention, and a toast per keystroke/dropdown-change would be noisy); "Backup complete," "Shortcut updated," and "Account deleted" do produce toasts since those are discrete, meaningful events.

**Search/filter behavior:** the Shortcuts tab has a free-text search across action names, since it's the one Settings tab with enough rows to benefit from it.

**Sorting:** Shortcuts list grouped by category (Navigation, Editing, Grid) rather than alphabetically, for learnability; not user-resortable.

**Multi-selection behavior:** not applicable anywhere in Settings.

**Navigation flow:** entered via sidebar, Command Palette, or menu bar (Edit/App → Preferences convention); this screen is terminal — it has no further drill-down, by design.

**Accessibility:** tabs use standard ARIA tablist/tabpanel roles with arrow-key navigation between tabs; the Shortcuts reassignment control clearly announces "Press any key combination" when active so it's discoverable via screen reader, not just visually implied by a focused empty field.

**Developer implementation notes:** Settings should read/write directly to a single application-preferences store separate from portfolio data, so that restoring a data backup (Data & Backup tab) never inadvertently resets the user's General/Shortcuts preferences, and vice versa — these two stores must remain independent at the persistence layer even though they're presented in one screen.

---

## APPENDIX — Cross-Screen Conventions Reference

A few interaction rules are deliberately identical across every grid screen (Holdings, Transactions, History, and the Review tables in Import) — listed once here rather than re-derived per screen, so an inconsistency during implementation is easy to spot against a single source of truth:

| Convention | Rule |
|---|---|
| Single-click on a data row | Selects only; never navigates |
| Double-click on a data row | Opens the row's primary detail (Security Detail, or Transaction Edit where the row *is* a transaction) — see each screen's Double-click section for which applies |
| `Ctrl+F` | Focuses that screen's in-grid filter |
| `Shift`/`Ctrl`+click | Multi-select, surfaces the bulk-action strip |
| Column header click | Sorts (toggles ascending/descending); single-column sort only, app-wide |
| Empty due to no data vs. empty due to filter | Always visually and textually distinguished (§15 architecture principle, enforced at the component level here) |
| Destructive actions | Always Modal-confirmed, always state exactly what's being affected, never a bare "Are you sure?" |
| Toasts | Reserved for discrete completed actions the user should know succeeded; never used for passive state changes (filtering, sorting, tab switching) |

This appendix should be treated as a lint rule during implementation review: any new grid screen or dialog that deviates from it should be a deliberate, documented exception — not a default drift.
