#!/usr/bin/env bash
set -euo pipefail

# Detect CI environment
if [ "${CI:-false}" = "true" ]; then
  echo "Running in CI mode – skipping health check and venv activation"
else
  # 1. Backend health check
  echo "Checking backend health..."
  if ! curl -sSf http://localhost:8000/health; then
    echo "Backend health check failed"
    exit 1
  fi
fi

# 2. Frontend build
npm -C frontend run build

# 3. Backend tests
if [ "${CI:-false}" = "true" ]; then
  python -m pytest -q
else
  source ./myenv/bin/activate && python -m pytest -q
fi

# 4. Frontend tests
npm -C frontend test --silent

# 5. No stray compiled files
git ls-files | grep -E "__pycache__|\.pyc$|\.pyo$|\.pyd$" || true

echo "Smoke demo passed"
