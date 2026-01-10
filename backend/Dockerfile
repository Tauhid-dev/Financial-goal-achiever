FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Install dependencies (build context is ./backend)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Create a package root that matches the repo layout
RUN mkdir -p /app/backend && touch /app/backend/__init__.py

# Alembic configuration
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic

# Copy the application code into /app/backend/app
COPY app /app/backend/app

# Ensure the container can import `backend...`
ENV PYTHONPATH=/app

USER appuser
EXPOSE 8000

CMD ["python","-m","uvicorn","backend.app.main:app","--host","0.0.0.0","--port","8000"]
