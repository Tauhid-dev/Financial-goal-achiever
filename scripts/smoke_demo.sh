#!/usr/bin/env bash
set -euo pipefail

# 1. Backend health check
echo "Checking backend health..."
if ! curl -sSf http://localhost:8000/health; then
  echo "Backend health check failed"
  exit 1
fi

# 2. Frontend build
npm -C frontend run build

# 3. Backend tests
source ./myenv/bin/activate && python -m pytest -q

# 4. Frontend tests
npm -C frontend test --silent

# 5. No stray compiled files
git ls-files | grep -E "__pycache__|\.pyc$|\.pyo$|\.pyd$" || true

echo "Smoke demo passed"
