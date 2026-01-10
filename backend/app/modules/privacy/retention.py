# Simple retention policy – documentation only, no enforcement logic.
RETENTION_POLICY = {
    "raw_pdf": "memory_only",               # never persisted
    "extracted_text": "ephemeral",          # kept only during processing
    "normalized_transactions": "persistable",
    "aggregates": "persistable",
}
