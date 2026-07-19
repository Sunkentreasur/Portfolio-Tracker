# Contributor Reference Material

This directory preserves architecture and UX material contributed during planning.
It is reference material for future implementation work; it does not replace the
repository's primary design documents in `docs/`.

## Precedence

1. Current implementation and the repository-owned documents in `docs/` are the
   source of truth.
2. `UI_UX.md` is the detailed interaction and design-system specification for
   the personal-edition UI. Use it when implementing user-facing screens.
3. `UX_ARCHITECTURE_V2_PERSONAL.md` records the current personal-edition
   information architecture and the rationale for its intentionally small scope.
4. The remaining files are valuable design input, historical context, or reviews.
   Adopt their recommendations only when they fit the current repository design
   and the active implementation milestone.

## Files

| File | Purpose | Status |
| --- | --- | --- |
| `UI_UX.md` | Detailed screen behavior, interaction patterns, accessibility, and design tokens. | Current UX implementation reference. |
| `UX_ARCHITECTURE_V2_PERSONAL.md` | Personal-edition navigation and screen rationale. | Current UX architecture reference. |
| `UX_ARCHITECTURE_V1.md` | Earlier, broader UX architecture. | Historical; superseded in scope by v2. |
| `DATABASE_IMPORT_ANALYTICS_BENCHMARK_NOTES.md` | Database, import, analytics, and benchmark-engine recommendations. | Technical reference; validate each financial rule with tests before adoption. |
| `FINANCIAL_SYSTEMS_BLUEPRINT.md` | Analytics priorities and financial-calculation considerations. | Technical reference for roadmap and validation. |
| `ARCHITECTURE_REVIEW.md` | External architectural review and suggested mitigations. | Review input; not an accepted change list. |

## Integration Notes

- The detailed UI specification and v2 UX architecture intentionally reduce the
  earlier v1 scope: no dedicated tax, watchlist, report-builder, or notification
  modules are planned for the personal edition.
- The database and analytics references reinforce immutable transactions,
  import-batch traceability, precise decimal arithmetic, background analytics,
  and a review-before-commit import workflow. These align with the project goals.
- The architecture review recommends strict dependency inversion and a command
  boundary for plugins. These are potentially significant changes from the
  repository's current layered architecture, so they require an explicit design
  decision before implementation rather than being adopted implicitly.

