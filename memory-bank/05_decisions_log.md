## API Routing Consolidation
Decision: API routes currently consolidated into shared route files.
Reason: Faster iteration during early scaffolding.
Follow-up: May refactor to per-domain routers later if needed.

## Partial DB Models
Decision: Only MonthlySummary model added initially.
Reason: Focus was on core financial logic before persistence.
Follow-up: Remaining domain models to be added next.

## Memory Bank Correction
Decision: Memory Bank updated to reflect actual repo state.
Reason: Restore single-source-of-truth discipline before further development.