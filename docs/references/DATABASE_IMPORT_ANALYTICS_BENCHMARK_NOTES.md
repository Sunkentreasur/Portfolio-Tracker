# DATABASE.md

This document defines the SQLite persistence layer. The database must serve as an immutable, append-only (where possible) ledger of truth.

## Entities

* **`Account`**: Represents a brokerage or external holding entity (e.g., "Vanguard IRA").
* **`Asset`**: Represents a financial instrument (e.g., AAPL, SPY, Cash). Must contain currency and asset class metadata.
* **`Transaction`**: The immutable core of the system. Represents a single atomic movement of capital or shares (Buy, Sell, Deposit, Withdraw, Dividend, Fee).
* **`PriceHistory`**: End-of-day (EOD) pricing for assets.
* **`CorporateAction`**: Records of splits, mergers, and spin-offs necessary to adjust historical cost basis.
* **`ImportBatch`**: Tracks a specific file import event for audit and rollback purposes.

## Relationships

* **`Account` (1) to (N) `Transaction`**: Every transaction belongs to one account.
* **`Asset` (1) to (N) `Transaction`**: Every transaction (except raw cash deposits) references one asset.
* **`Asset` (1) to (N) `PriceHistory`**: An asset has many daily prices.
* **`ImportBatch` (1) to (N) `Transaction`**: A transaction originates from one import batch (or is flagged as a manual entry).

## Normalization

The schema strictly adheres to **Third Normal Form (3NF)**.
* **No derived data in core tables:** We do *not* store "Current Balance" or "Current Shares" in the `Account` or `Asset` tables. All balances are dynamically derived from the `Transaction` ledger.
* **Immutability:** Financial ledgers are append-only. To correct a mistake, the standard financial practice is to post an offsetting (reversing) transaction, though for a personal tool, a hard delete bound to a specific `ImportBatch` is permitted.

## Indexing Strategy

To support the analytics engine's need to read tens of thousands of rows rapidly, the following B-Tree indexes are required:
* `idx_txn_account_date`: On `Transaction(AccountID, Date)`. (Optimizes TWR sub-period lookups).
* `idx_txn_asset_date`: On `Transaction(AssetID, Date)`. (Optimizes holding-level CTR calculations).
* `idx_price_asset_date`: On `PriceHistory(AssetID, Date)`. (Critical for the shadow portfolio engine).
* `idx_txn_hash`: On `Transaction(UniqueHash)`. (O(1) duplicate detection during imports).

## Constraints

* **Foreign Keys:** Enforced with `ON DELETE RESTRICT`. You cannot delete an `Asset` if a `Transaction` references it.
* **Check Constraints:** `Transaction.Shares` and `Transaction.Price` must be >= 0. (Directionality is handled by a `TransactionType` enum: BUY adds shares, SELL subtracts).
* **Data Types:** SQLite does not have a native `DECIMAL` type. To prevent IEEE 754 floating-point drift, all monetary amounts and share counts MUST be stored as `INTEGER` representing micro-units (e.g., multiply by 1,000,000), or strictly parsed via Python's `decimal.Decimal` before saving to a `TEXT` column.

## Future Extensibility

* **JSONB Metadata:** Both `Transaction` and `Asset` tables will feature a `Metadata` column (using SQLite's JSON functions). This allows us to store broker-specific quirks (e.g., Robinhood margin IDs, interactive brokers execution venue) without altering the strict relational schema.

---

# IMPORT_ENGINE.md

The Import Engine guarantees that no garbage data ever enters the `Transaction` ledger. 

## Import Pipeline

1. **File Ingestion:** Read raw bytes.
2. **Broker Detection:** Scan headers/signatures to route to the correct parser.
3. **Parsing:** Convert raw CSV/PDF rows into a `RawTransaction` DTO.
4. **Normalization:** Map broker-specific terminology ("Bought", "B", "Buy to Open") into a standardized `TransactionType` enum.
5. **Validation:** Ensure all required fields exist and math balances (Shares * Price + Fees = Total).
6. **Duplicate Detection:** Compare incoming hashes against the database.
7. **Persistence:** Wrap the batch in a database transaction and commit.

## Broker Abstraction

Implement an `IBrokerParser` interface.
* `can_parse(header_row: str) -> bool`: Determines if this parser handles the file.
* `parse(stream: IO) -> List[RawTransaction]`: Yields standard objects.
Adding a new broker simply requires writing a new class that implements this interface and registering it with the Plugin Manager.

## CSV Parsing

* **Streaming:** Use Python's built-in `csv` module as a generator. Do not load a 50,000-row CSV entirely into memory.
* **Type Coercion:** All numerical parsing must instantly cast to Python's `decimal.Decimal`.

## Validation

* **Mathematical Integrity:** Assert that Shares * Price + Commission = Net Amount. If a broker's CSV rounds these numbers so they don't exactly match, flag the discrepancy and apply the remainder to a `Rounding_Adjustment` metadata field.
* **Orphan Check:** Ensure the `Asset` ticker exists in the database. If not, trigger an event to create the asset before saving the transaction.

## Duplicate Detection

* **Hashing:** Every parsed transaction generates a SHA-256 hash derived from: `BrokerID + Date + Ticker + Type + Decimal(Amount) + Decimal(Shares)`.
* **Execution:** Query the `idx_txn_hash` index. If the hash exists, silently drop the incoming row.

## Conflict Resolution

* If an incoming row matches Date, Ticker, and Type, but the amounts differ by < $0.01 (typical for floating-point broker exports), auto-resolve by keeping the existing database record and logging a warning.
* If major conflicts occur, the row is written to a `FailedImportLog` for the user to resolve manually. The rest of the batch continues.

## Undo Strategy

* When an import starts, an `ImportBatch(Timestamp, Filename)` is created.
* All transactions get stamped with this `BatchID`.
* To undo: `DELETE FROM Transactions WHERE BatchID = ?`. Cascading deletes handle the rest.

## Error Recovery

* **Unit of Work:** The entire Step 7 (Persistence) is wrapped in a `BEGIN TRANSACTION` / `COMMIT` block. If a database constraint fails on row 9,999 of 10,000, a `ROLLBACK` is issued. No partial files are ever saved.

---

# ANALYTICS.md

This engine computes all financial intelligence. It must never block the main UI thread.

## Time-Weighted Return (TWR)
* **Formula:** Product of (1 + R_i) - 1, where R_i = (Ending_Value - Beginning_Value - Cash_Flow) / Beginning_Value.
* **Inputs:** `Transaction` ledger (for CFs), `PriceHistory` (for daily valuations).
* **Dependencies:** Requires a perfectly calculated daily portfolio valuation array.
* **Refresh Strategy:** Asynchronous trigger upon database write (new imports or new daily prices).
* **Caching:** Store historical monthly TWR nodes in a materialized view. Only recalculate the current, open month dynamically.
* **Edge Cases:** Beginning Value = 0 (e.g., funding a brand new account). *Handling:* If BMV is 0, R_i for that sub-period is defined as 0, and the sub-period effectively starts at the end of the day.
* **Performance:** Highly computationally expensive to rebuild history. Caching historical nodes is critical.

## Money-Weighted Return (XIRR)
* **Formula:** The discount rate (r) that sets the Net Present Value (NPV) of all cash flows equal to zero.
* **Inputs:** Array of all Deposits (positive), Withdrawals (negative), and the Current Portfolio Value treated as a terminal Withdrawal (negative).
* **Dependencies:** None other than net cash flows and today's total value.
* **Refresh Strategy:** On-demand or asynchronous post-import.
* **Caching:** Store the last calculated XIRR rate and an MD5 hash of the cash-flow array. If the hash hasn't changed, return the cached rate.
* **Edge Cases:** Multiple sign changes in cash flows can result in multiple mathematical roots. *Handling:* Seed the Newton-Raphson algorithm with a realistic guess (e.g., 0.10) and bound the search space to [-0.99, 10.0].
* **Performance:** Fast in isolation, but solving the polynomial for 10,000 distinct cash flows can take > 100ms. Aggregate same-day cash flows into a single net daily cash flow before solving.

## Yield on Cost (YOC)
* **Formula:** Forward Annual Dividend Per Share / Adjusted Average Cost Basis Per Share
* **Inputs:** `Assets.Forward_Dividend`, `Transaction` ledger (to compute cost basis).
* **Dependencies:** `CorporateAction` table (splits fundamentally alter cost basis).
* **Refresh Strategy:** Daily (as forward dividend rates change).
* **Caching:** None required. Fast arithmetic.
* **Edge Cases:** Dividend cuts to zero, or assets acquired entirely via DRIP (resulting in zero external cost basis). *Handling:* If cost basis is 0, YOC is mathematically undefined; display as "N/A".
* **Performance:** Negligible.

---

# BENCHMARK_ENGINE.md

The Benchmark Engine calculates the "Cash-Flow Matched Shadow Portfolio." This answers: *What if I had taken every dollar I invested and blindly bought the S&P 500 instead?*

## Deposits
When the user deposits $X into their portfolio on Date_T, the Shadow Engine queries `PriceHistory` for the benchmark asset on Date_T. It calculates `Shadow_Shares_Acquired = $X / Benchmark_Closing_Price`. These shares are added to the Shadow Ledger.

## Withdrawals
When the user withdraws $Y on Date_T, the Engine sells shadow shares. `Shadow_Shares_Sold = $Y / Benchmark_Closing_Price`. If the user withdraws more cash than the shadow portfolio is worth (due to the user's outperformance), the shadow portfolio value drops to exactly 0 (it cannot go negative).

## Fractional Shares
Unlike standard brokerages, the Shadow Engine does not respect lot constraints. `Shadow_Shares` are calculated and stored using Python `decimal.Decimal` to 14 decimal places of precision.

## Dividends
The benchmark asset (e.g., SPY) pays dividends. The Engine queries the `DividendLog` for the benchmark. On the ex-dividend date, the Engine calculates: `Shadow_Div_Cash = Shadow_Shares * Dividend_Per_Share`.
* **Action:** This cash is immediately and automatically reinvested (DRIP) into more shadow shares at that day's closing price. No cash drag is permitted in the shadow portfolio.

## Stock Splits
If the benchmark undergoes a 2:1 split on Date_S, the Engine creates a systemic adjustment in the Shadow Ledger. `Shadow_Shares = Shadow_Shares * 2`. The historical cost basis of the shadow lots is halved.

## Corporate Actions
For broad market indices (SPY, VTI), spin-offs are natively handled by the ETF manager and reflected in the ETF's price/dividend. The Shadow Engine simply follows the adjusted closing price of the tracking ETF.

## Currency Conversion
If the user's base currency is EUR, but the shadow benchmark is SPY (USD), a daily FX cross-rate is required. On Date_T, a deposit of 1,000 EUR is first converted to USD using the Date_T EUR/USD spot rate *before* purchasing the shadow SPY shares. The shadow portfolio's total value is converted back to EUR daily for UI comparison.

## Benchmark Switching
If the user changes their benchmark from SPY to QQQ halfway through their timeline, the Shadow Engine does *not* mix them. 
* **Action:** The engine liquidates the entire SPY shadow portfolio on the exact day of the switch, realizing the simulated capital, and immediately buys QQQ shadow shares with 100% of the simulated proceeds.

## Historical Price Handling
Financial markets are closed on weekends and holidays. If a user transaction occurs on a Saturday (e.g., a bank transfer clears), the engine cannot buy the benchmark.
* **Rule:** The Shadow Engine strictly uses **Forward-Fill (ffill)** logic. A transaction on Saturday uses Friday's closing price.

## Accuracy Considerations
* **The Adjusted Close Problem:** We must use *raw* closing prices, not "Adjusted Close" prices from Yahoo Finance, because the engine natively simulates the reinvestment of dividends. Using "Adjusted Close" alongside native DRIP simulation would double-count dividend returns.
* **Rounding Drift:** All aggregations of the Shadow Ledger must sum using `decimal` logic. Floating-point math (`float`) will drift over 20 years of simulated daily compounding, ruining the integrity of the comparison.