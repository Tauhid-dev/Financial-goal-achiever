# Architecture Overview

## Backend Stack
- Python 3.11
- FastAPI (API contracts only)
- Docker & docker-compose (not executed)
- Domain-driven modular structure

## Module Overview
- ingest → PDF parsing & OCR stub
- normalize → transaction cleanup & categorization
- budget → family profiles & monthly analysis
- goals → savings goals & simulations
- privacy → redaction, sanitization & guardrails
- api → FastAPI schemas & route contracts
- core → runtime & config safety

## Architectural Principles
- Modules must be independent
- No side effects
- No execution during build
- Business logic never lives in API routes
- Everything must be extensible