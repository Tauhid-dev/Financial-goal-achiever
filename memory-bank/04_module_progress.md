# Module Progress

## Status
🚧 Demo-smoke CI fixed

## Completed
- Backend Dockerfile updated to copy alembic files with repository‑root build context.
- `docker-compose.demo.yml` backend service now builds from repo root and runs `python -m uvicorn app.main:app`.
- CI workflow `.github/workflows/demo-smoke.yml` preflight step added to verify build context and file visibility.
- All modifications prepared for a single commit.

## Current Focus
- Phase 2: PDF ingestion (next chunk)
