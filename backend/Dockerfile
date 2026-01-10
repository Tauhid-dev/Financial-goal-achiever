FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Install python dependencies (cache‑friendly)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the backend source code
COPY . /app

# Ensure the app package is importable
ENV PYTHONPATH=/app

USER appuser

EXPOSE 8000

CMD ["python","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
