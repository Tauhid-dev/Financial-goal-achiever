## Decisions Log

- API routing consolidated into a single router module early for speed; may split into per-domain routers later.
- v1 is deterministic (no LLM) for cost control and privacy.
- Build rule: do not execute code during scaffolding to keep it safe in constrained environments.
- Privacy-first defaults: redact/sanitize and avoid storing raw PDFs.
- Modular architecture for future B2B API and easy extension.
- Memory bank maintained as the single source of truth for progress/decisions.
- Auth uses JWT (HS256) with required JWT_SECRET from env; no fallback secret.
- Membership model links User ↔ Family; registration creates a default family + owner membership.
- Upload endpoint resolves user’s default family_id via membership before persisting documents/txns/summaries.
- Transaction ingestion hardening: infer direction from amount if missing; default date to 1970-01-01; cast amount to float.
- Insights are deterministic from MonthlySummary + top expense categories (no AI provider).
