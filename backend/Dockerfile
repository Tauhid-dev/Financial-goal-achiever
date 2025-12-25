# ---- Base image ----
FROM python:3.11-slim

# ---- Create non-root user ----
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
WORKDIR /app

# ---- Install dependencies (placeholder) ----
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy application code ----
COPY backend/app /app

# ---- Switch to non-root user ----
USER appuser

# ---- Placeholder command (no server start) ----
# CMD ["python"]
