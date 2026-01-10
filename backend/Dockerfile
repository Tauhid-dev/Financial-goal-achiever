# Added comment for final commit
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Install dependencies (build context is repository root)
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Alembic configuration
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic

# Application code
COPY backend/app /app/backend/app

# Ensure the container can import the backend package
ENV PYTHONPATH=/app

USER appuser
EXPOSE 8000

CMD ["python","-m","uvicorn","backend.app.main:app","--host","0.0.0.0","--port","8000"]
