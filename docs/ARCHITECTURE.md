# Architecture

## Purpose

This document defines the technical architecture of Portfolio Tracker. It serves as the primary reference for software design decisions, ensuring that every component follows a consistent structure, clear responsibilities, and maintainable engineering practices.

The architecture prioritizes correctness, modularity, extensibility, and long-term maintainability over short-term implementation convenience.

## Architectural Goals

The architecture is designed to:

- Separate business logic from the user interface.
- Keep components loosely coupled and highly cohesive.
- Support offline-first operation.
- Ensure calculations are deterministic and reproducible.
- Allow new features to be added with minimal impact on existing code.
- Enable plugin-based extensibility.
- Maintain excellent performance with large portfolios.
- Keep the codebase easy to test and maintain.

## High-Level Overview

Portfolio Tracker follows a layered architecture.

User interactions are handled by the presentation layer, which communicates with application services responsible for business logic. Services coordinate imports, analytics, reporting, plugins, and database operations without depending on the user interface.

Persistent data is stored in SQLite through SQLAlchemy, ensuring that every calculation is reproducible from imported brokerage statements.

## Layered Architecture

Portfolio Tracker follows a four-layer architecture designed to separate concerns and maximize maintainability.

### 1. Presentation Layer
Responsible for the desktop user interface built with PySide6. This layer displays information, receives user input, and delegates work to the Application Layer. It must not contain business logic.

### 2. Application Layer
Coordinates application workflows such as importing statements, refreshing portfolio data, generating reports, and executing analytics. It orchestrates operations but contains minimal business rules.

### 3. Domain Layer
The core of the application. It contains portfolio models, investment calculations, analytics algorithms, validation rules, benchmark comparisons, and all business logic. This layer must remain independent of the UI.

### 4. Infrastructure Layer
Provides technical services such as SQLite persistence, SQLAlchemy repositories, file parsing, configuration management, logging, plugin loading, and external integrations.

Dependencies flow downward only.

Presentation
    ↓
Application
    ↓
Domain
    ↓
Infrastructure

Lower layers must never depend on higher layers.

## Module Responsibilities

Presentation
- Windows
- Dialogs
- Widgets
- View models
- User interaction

Application
- Import orchestration
- Report generation
- Workflow coordination
- Command handling

Domain
- Portfolio calculations
- Asset models
- Transactions
- Analytics
- Benchmark engine
- Cash-flow engine
- Validation

Infrastructure
- Database
- File system
- Logging
- Configuration
- Plugin loader
- Import parsers

Each module should have a single, clearly defined responsibility.

## Folder Structure

To be defined.

## Dependency Rules

The architecture follows these mandatory dependency rules:

- The Presentation Layer may depend on the Application Layer only.
- The Application Layer may depend on the Domain and Infrastructure Layers.
- The Domain Layer must not depend on the Presentation Layer.
- Infrastructure may implement interfaces defined by higher layers but must not introduce business rules.
- Circular dependencies are prohibited.
- Business logic must never exist inside UI classes.
- Database models must not contain business calculations.
- Every layer should communicate through well-defined interfaces whenever practical.

## Data Flow

Portfolio Tracker follows a predictable, unidirectional flow of data.

1. The user performs an action in the Presentation Layer.
2. The Presentation Layer delegates the request to an Application Service.
3. The Application Service validates the request and coordinates the required workflow.
4. The Domain Layer performs calculations and business logic.
5. The Infrastructure Layer persists or retrieves data when required.
6. Results flow back through the Application Layer to the Presentation Layer for display.

This predictable flow simplifies debugging, testing, and maintenance.

## Import Pipeline

The import pipeline converts brokerage statements into validated portfolio data.

Pipeline stages:

1. File Selection
2. File Validation
3. Broker Detection
4. Statement Parsing
5. Data Normalization
6. Validation
7. Duplicate Detection
8. Transaction Mapping
9. Database Persistence
10. Portfolio Recalculation
11. Analytics Refresh
12. UI Refresh

Each stage has a single responsibility and produces deterministic output before passing control to the next stage.

Pipeline stages should be independently testable.

## Analytics Pipeline

Analytics are generated after portfolio data has been validated and stored.

Pipeline stages:

1. Load portfolio state.
2. Calculate holdings.
3. Calculate cash flows.
4. Calculate performance metrics (TWR, XIRR, CAGR).
5. Calculate benchmark comparison.
6. Calculate allocation statistics.
7. Generate charts and summaries.
8. Return analytics results to the Presentation Layer.

Analytics should never modify portfolio data.

All calculations must be deterministic and reproducible from stored transactions.

## Plugin Architecture

Portfolio Tracker provides a modular plugin architecture that enables new functionality to be added without modifying the core application.

Plugins may contribute:

- Brokerage statement importers.
- Analytics modules.
- Custom reports.
- Dashboard widgets.
- Benchmark providers.
- AI capabilities.
- Data exporters.

Every plugin must implement a well-defined interface and be loaded through the Plugin Manager.

Plugins operate within clearly defined boundaries and must not directly modify the application's internal state. All interactions with the core system occur through public APIs.

## AI Assistant Architecture

The AI Assistant is implemented as an independent application service rather than being tightly coupled to the user interface.

Its responsibilities include:

- Explaining portfolio analytics.
- Answering questions about holdings and performance.
- Summarizing portfolio changes.
- Assisting with application workflows.
- Explaining calculations and metrics.

The AI Assistant must consume data exposed by the Application Layer and Domain Layer. It must never access the database directly or bypass business rules.

## Configuration Management

Application configuration is centralized through a dedicated Configuration Service.

Configuration includes:

- Application preferences.
- Theme settings.
- Import settings.
- Plugin configuration.
- Logging configuration.
- Database configuration.
- AI Assistant settings.

Configuration should be validated during application startup and exposed through a strongly typed configuration interface rather than scattered throughout the codebase.

## Logging Strategy

Portfolio Tracker uses structured logging to provide clear diagnostics while avoiding unnecessary verbosity.

Logging levels:

- DEBUG – Detailed diagnostic information for development.
- INFO – Normal application events.
- WARNING – Recoverable issues.
- ERROR – Operation failures.
- CRITICAL – Severe failures that may prevent normal operation.

Business logic should log meaningful events without exposing sensitive user data.

## Error Handling Philosophy

Errors should be handled as close to their source as practical while providing meaningful feedback to the user.

Principles:

- Never silently ignore errors.
- Display user-friendly error messages.
- Log detailed technical information for debugging.
- Recover gracefully whenever possible.
- Prevent partial or inconsistent database updates using transactions.

## Performance Considerations

The architecture is designed to remain responsive for large investment portfolios.

Performance principles:

- Lazy-load data where appropriate.
- Avoid unnecessary database queries.
- Cache expensive calculations when safe.
- Perform long-running tasks asynchronously.
- Keep the UI responsive during imports and analytics.
- Optimize for portfolios containing tens of thousands of transactions.

## Security Model

Portfolio Tracker is designed as an offline-first desktop application where user data remains under the user's control.

Security principles:

- All portfolio data is stored locally by default.
- No financial data is transmitted externally unless the user explicitly enables an integration.
- Secrets such as API keys must never be hardcoded and should be stored securely.
- Input from imported files must always be validated before processing.
- Database operations must use parameterized queries through SQLAlchemy.
- Sensitive information should never appear in logs.
- The application should fail securely when encountering invalid or unexpected input.

## Scalability Strategy

The architecture is designed to support future growth without major redesign.

Scalability principles:

- Maintain clear separation between presentation, application, domain, and infrastructure layers.
- Design services to remain modular and independently testable.
- Support additional importers, analytics modules, and plugins without modifying the core application.
- Minimize coupling between components.
- Optimize database access to support very large transaction histories.
- Ensure future cloud synchronization can be introduced without impacting offline functionality.

## Testing Strategy

Testing is an essential part of development and should accompany every major feature.

Testing includes:

- Unit tests for business logic.
- Integration tests for database operations.
- Import validation tests using sample brokerage statements.
- Analytics verification using known reference portfolios.
- UI testing for critical workflows.
- Regression testing before releases.

Automated tests should be preferred wherever practical.

## Deployment Architecture

Portfolio Tracker is distributed as a standalone desktop application.

Deployment principles:

- The application should run entirely on the user's local machine.
- Package releases using PyInstaller for Windows, with future support for macOS and Linux.
- Bundle all required dependencies within the installer where practical.
- Store user data separately from application binaries to simplify upgrades.
- Support automatic migration of the database schema between compatible versions.
- Configuration and user data must persist across application updates.
- Ensure installation and updates are simple for non-technical users.

## Future Architectural Evolution

The architecture is intentionally designed to support future enhancements without requiring major redesign.

Potential future capabilities include:

- Optional cloud synchronization while preserving offline-first behavior.
- Mobile companion applications.
- Additional brokerage integrations.
- Advanced analytics and reporting modules.
- Multi-user support.
- Portfolio sharing and collaboration.
- Enhanced AI capabilities.
- Expanded plugin ecosystem.

Future enhancements should build upon the existing layered architecture and maintain backward compatibility whenever practical.
