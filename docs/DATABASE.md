# Database Design

## Goals

The database architecture is designed to support the core requirements of Portfolio Tracker while maintaining data integrity, performance, and long-term maintainability.

- **Offline-first** – All portfolio data must be stored locally and accessible without an internet connection.
- **Reliability** – The database must handle large transaction histories without corruption or data loss.
- **Data integrity** – Financial data must be accurate, consistent, and validated at the database level.
- **Auditability** – Every change to portfolio data must be traceable through immutable transaction history.
- **Performance** – Queries must remain responsive even with tens of thousands of transactions.
- **Extensibility** – The schema must support future features without major redesign.

## Database Technology

Portfolio Tracker uses SQLite as the primary database technology, accessed through SQLAlchemy ORM with Alembic for schema migrations.

- **SQLite** – Embedded, serverless database ideal for desktop applications. Provides ACID compliance, zero configuration, and excellent performance for read-heavy workloads.
- **SQLAlchemy ORM** – Python ORM that provides a high-level abstraction over database operations while allowing raw SQL when needed. Ensures type safety and reduces boilerplate.
- **Alembic migrations** – Database migration tool that tracks schema changes and enables safe upgrades between versions.
- **Foreign key enforcement** – Referential integrity is enforced at the database level to prevent orphaned records.
- **Transaction support** – All database operations are wrapped in transactions to ensure atomicity and enable rollback on failure.

## Design Principles

The database schema follows established database design principles while being tailored to the specific requirements of investment portfolio management.

- **Normalized schema where appropriate** – The database is normalized to eliminate redundancy while balancing query performance. Denormalization is used only where justified by performance requirements.
- **Immutable transaction history** – Once recorded, transactions are never modified. Corrections are made through reversal transactions, preserving complete audit trails.
- **No duplicated financial data** – Financial values are stored in their most atomic form and calculated on demand. This ensures consistency and eliminates synchronization issues.
- **Referential integrity** – All relationships are enforced through foreign keys to prevent orphaned records and maintain data consistency.
- **Soft deletion only where justified** – Most records are never deleted. Soft deletion is used only for user-facing entities like watchlists or notes, never for financial data.
- **Deterministic calculations** – All portfolio calculations are derived from stored transactions. The database stores the source of truth, not derived values.

## Core Entities

### Portfolio

**Purpose**
Represents a complete investment portfolio, typically corresponding to a single investor or household. A portfolio may contain multiple accounts across different brokers.

**Relationships**
- Has many Accounts
- Has many Transactions (through Accounts)
- Has many Benchmarks
- Has many Watchlists
- Has many Settings

**Important Design Considerations**
- Portfolios are the top-level organizational unit for reporting and analytics.
- A single user may have multiple portfolios (e.g., personal, retirement, business).
- Portfolio-level settings control default behavior for analytics and reporting.

### Account

**Purpose**
Represents a single brokerage or investment account. Accounts are the primary container for transactions and positions.

**Relationships**
- Belongs to a Portfolio
- Has many Transactions
- Has many Positions
- Has many Cash Balances
- Belongs to a Broker (optional)

**Important Design Considerations**
- Accounts are uniquely identified by account number and broker.
- Account type (taxable, IRA, 401k, etc.) is stored for tax reporting.
- Currency is stored at the account level to support multi-currency portfolios in the future.

### Asset

**Purpose**
Represents a tradeable security or investment vehicle. Assets include stocks, ETFs, mutual funds, bonds, options, and other investment types.

**Relationships**
- Has many Transactions
- Has many Positions
- Has many Price History entries
- Belongs to an Asset Class
- Has many Tags

**Important Design Considerations**
- Assets are uniquely identified by ticker symbol and exchange.
- Asset type (common stock, ETF, mutual fund, etc.) is stored for classification and analytics.
- Asset metadata (name, sector, industry) is cached to reduce external API dependencies.

### Transaction

**Purpose**
Records every buy, sell, dividend, corporate action, and other portfolio activity. Transactions are the source of truth for all portfolio calculations.

**Relationships**
- Belongs to an Account
- Belongs to an Asset
- Belongs to a Transaction Type
- May reference a Corporate Action

**Important Design Considerations**
- Transactions are immutable. Corrections are made through reversal transactions.
- Transaction types include buy, sell, dividend, interest, deposit, withdrawal, transfer, corporate action, and fee.
- Quantity and price are stored with high precision to avoid rounding errors.
- Settlement date is stored separately from trade date for accurate cash flow tracking.

### Position

**Purpose**
Represents current holdings of an asset within an account. Positions are calculated from transactions and can be reconstructed at any point in time.

**Relationships**
- Belongs to an Account
- Belongs to an Asset
- Derived from Transactions

**Important Design Considerations**
- Positions are not stored directly but calculated from transaction history.
- This ensures consistency and eliminates synchronization issues.
- Position snapshots may be cached for performance but are never the source of truth.

### Cash Balance

**Purpose**
Tracks cash holdings within an account. Cash balances are derived from deposit, withdrawal, dividend, and transaction history.

**Relationships**
- Belongs to an Account
- Derived from Transactions

**Important Design Considerations**
- Cash balances are calculated from transaction history, not stored directly.
- Multiple currencies may be supported per account in the future.
- Cash is treated as an asset class for allocation analytics.

### Dividend

**Purpose**
Records dividend and interest income received from investments. Dividends are a subset of transactions but are tracked separately for income analytics.

**Relationships**
- Belongs to a Transaction
- Belongs to an Asset
- Belongs to an Account

**Important Design Considerations**
- Dividends are immutable and derived from transaction history.
- Dividend type (qualified, ordinary, interest) is stored for tax reporting.
- Yield calculations are performed on demand, not stored.

### Corporate Action

**Purpose**
Records corporate actions that affect holdings without being standard buy/sell transactions. Includes splits, mergers, spin-offs, and symbol changes.

**Relationships**
- Belongs to an Asset
- Affects many Transactions
- Affects many Positions

**Important Design Considerations**
- Corporate actions are rare but critical for accurate historical performance.
- Splits are recorded as ratio adjustments to historical quantities.
- Mergers and spin-offs require mapping between old and new assets.
- Corporate actions must be applied in chronological order to reconstruct accurate positions.

### Benchmark

**Purpose**
Represents a market index or benchmark used for performance comparison. Benchmarks enable evaluation of portfolio performance relative to market standards.

**Relationships**
- Belongs to a Portfolio
- Has many Price History entries
- Has many Benchmark Data Points

**Important Design Considerations**
- Benchmarks may be custom (user-defined) or standard (S&P 500, etc.).
- Benchmark data is stored as time series for performance calculation.
- Multiple benchmarks may be tracked per portfolio for different comparison purposes.

### Price History

**Purpose**
Stores historical price data for assets and benchmarks. Price history enables performance calculation and charting.

**Relationships**
- Belongs to an Asset or Benchmark
- Has many Price Points

**Important Design Considerations**
- Price data includes open, high, low, close, and volume where available.
- Prices are stored at daily granularity for most assets.
- Intraday data may be supported in the future but is not required for long-term portfolio tracking.
- Price data is sourced from external APIs or imported from broker statements.

### Watchlist

**Purpose**
Allows users to track assets they are interested in but do not currently hold. Watchlists support investment research and monitoring.

**Relationships**
- Belongs to a Portfolio
- Has many Assets

**Important Design Considerations**
- Watchlists are user-facing and support soft deletion.
- Multiple watchlists may be created per portfolio (e.g., candidates, sector focus).
- Watchlist entries may include notes and target prices.

### Notes

**Purpose**
Stores user annotations and documentation attached to portfolios, accounts, assets, or transactions. Notes provide context and documentation for investment decisions.

**Relationships**
- Belongs to a Portfolio, Account, Asset, or Transaction
- Supports soft deletion

**Important Design Considerations**
- Notes are user-facing and support soft deletion.
- Notes may include timestamps for chronological tracking.
- Notes are optional and do not affect calculations.

### Tags

**Purpose**
Provides flexible categorization and labeling of assets, transactions, and other entities. Tags enable custom organization and filtering.

**Relationships**
- Has many Assets
- Has many Transactions
- Many-to-many with tagged entities

**Important Design Considerations**
- Tags are user-defined and completely flexible.
- Tags support custom analytics and reporting (e.g., sector, strategy, risk level).
- Tag relationships are many-to-many to support multiple tags per entity.

### Settings

**Purpose**
Stores application and portfolio-level configuration. Settings control application behavior, preferences, and default values.

**Relationships**
- Belongs to a Portfolio (for portfolio-level settings)
- Global settings exist at the application level

**Important Design Considerations**
- Settings are validated during application startup.
- Settings are strongly typed to prevent configuration errors.
- Default values are defined in code and overridden by user configuration.

## Database Relationships

### One-to-Many Relationships

- **Portfolio → Accounts**: A portfolio contains multiple accounts.
- **Account → Transactions**: An account has many transactions.
- **Account → Positions**: An account has many positions (calculated).
- **Account → Cash Balances**: An account has cash balances (calculated).
- **Asset → Transactions**: An asset appears in many transactions.
- **Asset → Price History**: An asset has historical price data.
- **Benchmark → Price History**: A benchmark has historical price data.
- **Portfolio → Watchlists**: A portfolio has multiple watchlists.
- **Portfolio → Benchmarks**: A portfolio tracks multiple benchmarks.
- **Portfolio → Settings**: A portfolio has configuration settings.

### Many-to-Many Relationships

- **Assets ↔ Tags**: An asset may have multiple tags; a tag may apply to multiple assets.
- **Transactions ↔ Tags**: A transaction may have multiple tags; a tag may apply to multiple transactions.
- **Watchlists ↔ Assets**: A watchlist contains multiple assets; an asset may appear in multiple watchlists.

### Derived Relationships

- **Positions** are not stored directly but derived from Transactions.
- **Cash Balances** are derived from Transactions.
- **Dividends** are a subset of Transactions with additional metadata.

## Indexing Strategy

Indexes are strategically placed to optimize query performance while minimizing write overhead. The indexing strategy focuses on the most common query patterns in portfolio analytics and reporting.

**Primary Indexes**
- All primary keys are automatically indexed by SQLite.
- Foreign key columns are indexed to accelerate join operations.

**Query Optimization Indexes**
- **Transactions**: Indexed by (account_id, date) for chronological account history queries.
- **Transactions**: Indexed by (asset_id, date) for asset-specific transaction history.
- **Price History**: Indexed by (asset_id, date) for time series queries.
- **Dividends**: Indexed by (account_id, date) for income reporting.
- **Corporate Actions**: Indexed by (asset_id, effective_date) for position reconstruction.

**Search and Filtering Indexes**
- **Assets**: Indexed by (ticker, exchange) for symbol lookup.
- **Assets**: Indexed by (asset_class_id) for classification queries.
- **Tags**: Indexed by name for tag-based filtering.

**Performance Considerations**
- Indexes are added only after measuring actual query performance.
- Composite indexes are used when multiple columns are frequently queried together.
- Write-heavy operations (bulk imports) may temporarily drop and recreate indexes.

## Transactions & Consistency

Portfolio Tracker relies on database transactions to ensure data integrity and enable safe error recovery.

### ACID Compliance

SQLite provides full ACID compliance, ensuring that all database operations are:

- **Atomic** – Transactions are all-or-nothing. Partial updates are never committed.
- **Consistent** – The database moves from one valid state to another, respecting all constraints.
- **Isolated** – Concurrent transactions do not interfere with each other.
- **Durable** – Committed transactions survive system failures.

### Rollback Strategy

All database operations are wrapped in transactions with explicit rollback on error:

- Import operations roll back completely if any stage fails.
- Analytics calculations use read-only transactions to prevent accidental modification.
- User-initiated operations roll back on validation errors.
- Database migrations use transactions to enable safe rollbacks if migration fails.

### Atomic Imports

The import pipeline treats the entire import operation as a single atomic transaction:

- All parsed transactions are validated before any database writes occur.
- Duplicate detection occurs within the transaction to prevent race conditions.
- Portfolio recalculation occurs after successful commit to ensure consistency.
- If any part of the import fails, the entire transaction is rolled back.

### Database Integrity

Referential integrity is enforced at the database level through foreign key constraints:

- Orphaned records are impossible due to foreign key enforcement.
- Cascade deletes are used only where appropriate (e.g., watchlist items).
- Financial data never uses cascade deletes to preserve audit trails.
- Check constraints validate data ranges (e.g., quantities cannot be negative).

## Performance Considerations

The database is optimized for the specific access patterns of portfolio management applications.

### Query Optimization

- **Read-heavy workload** – Portfolio analytics are read-heavy, so indexes prioritize query performance.
- **N+1 prevention** – Eager loading is used for related entities to avoid N+1 query problems.
- **Query batching** – Bulk operations use batch inserts and updates to minimize round trips.
- **Connection pooling** – SQLAlchemy connection pooling reduces connection overhead.

### Lazy Loading

- Large collections (transactions, price history) are loaded on demand.
- UI widgets load data incrementally to maintain responsiveness.
- Analytics calculations load only the data required for the specific metric.
- Pagination is used for large transaction lists in the UI.

### Batch Inserts

- Import operations use bulk insert for efficiency.
- Price history updates are batched when importing multiple assets.
- Transactions are inserted in batches during statement imports.
- Batch size is tuned to balance memory usage and performance.

### Efficient Joins

- Foreign key indexes accelerate join operations.
- Join queries are optimized to select only required columns.
- Complex analytics queries use subqueries strategically to avoid large intermediate results.
- Materialized views may be used for expensive recurring calculations.

### Large Portfolio Performance

- Historical queries are optimized using date-range indexes.
- Position calculations use incremental updates rather than full recalculation.
- Analytics results are cached where safe and invalidated on data changes.
- Long-running operations (full portfolio analytics) run asynchronously to avoid blocking the UI.

## Migration Strategy

Database schema changes are managed through Alembic migrations, ensuring safe upgrades between versions.

### Alembic Migrations

- All schema changes are tracked through Alembic migration scripts.
- Migrations are versioned and stored in the repository.
- Each migration includes both upgrade and downgrade paths.
- Migrations are tested against sample databases before release.

### Schema Versioning

- The database includes a schema version table managed by Alembic.
- Application startup checks schema version and runs pending migrations.
- Migrations run in a transaction to enable rollback on failure.
- Schema version is validated before allowing application startup.

### Backward Compatibility

- Migrations are designed to preserve existing data whenever possible.
- Data migrations are included in schema migrations when required.
- Deprecated columns are retained for at least one major version before removal.
- Breaking changes require explicit user acknowledgment before migration.

### Upgrade Process

- The application detects schema version on startup.
- Pending migrations are run automatically with user confirmation.
- Database backups are recommended before major version upgrades.
- Migration failures roll back automatically and display clear error messages.
- Migration logs are stored for troubleshooting and audit purposes.

## Future Expansion

The database schema is designed to support future features without requiring major redesign.

### Additional Broker Importers

- The transaction schema is generic enough to support any broker format.
- Broker-specific metadata is stored in flexible JSON columns where needed.
- New transaction types can be added without schema changes using enum extensions.
- Custom fields are supported through JSON columns for broker-specific data.

### New Asset Classes

- Asset types are extensible through the asset_type enum.
- Asset-specific metadata is stored in JSON columns for flexibility.
- New asset classes (crypto, derivatives, real estate) can be added without schema changes.
- Asset classification is hierarchical to support granular categorization.

### Cloud Sync

- The schema includes sync metadata columns (created_at, updated_at, sync_status).
- Conflict resolution is designed around immutable transaction history.
- Soft deletion supports sync without data loss.
- The schema is designed to merge changes from multiple sources safely.

### Multi-User Support

- Portfolio-level isolation enables multiple users per database instance.
- User authentication can be added without modifying core entities.
- Permissions can be implemented through additional user and role tables.
- Audit trails are already built-in through immutable transaction history.

### Plugin Extensions

- Tags provide a flexible extension point for custom categorization.
- JSON columns allow plugins to store custom metadata without schema changes.
- Plugin-specific tables can be added in separate migrations without affecting core schema.
- The plugin architecture is designed to extend functionality without modifying core entities.
