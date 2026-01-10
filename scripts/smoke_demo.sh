#!/usr/bin/env bash
set -euo pipefail

# -------------------------------------------------
# Smoke demo – full end‑to‑end verification
# -------------------------------------------------
# Detect CI environment – in CI we only run the static checks
if [ "${CI:-false}" = "true" ]; then
  echo "Running in CI mode – performing static checks only"
else
  echo "Running full E2E smoke demo"
fi

# -----------------------------------------------------------------
# 1. Backend health check (skip in CI)
# -----------------------------------------------------------------
if [ "${CI:-false}" != "true" ]; then
  echo "Checking backend health..."
  if ! curl -sSf http://localhost:8000/health; then
    echo "Backend health check failed"
    exit 1
  fi
fi

# -----------------------------------------------------------------
# 2. Frontend build
# -----------------------------------------------------------------
echo "Building frontend..."
npm -C frontend run build

# -----------------------------------------------------------------
# 3. Backend tests
# -----------------------------------------------------------------
if [ "${CI:-false}" = "true" ]; then
  echo "Running backend tests (CI mode)…"
  python -m pytest -q
else
  echo "Running backend tests (local)…"
  source ./myenv/bin/activate && python -m pytest -q
fi

# -----------------------------------------------------------------
# 4. Frontend tests
# -----------------------------------------------------------------
echo "Running frontend tests…"
npm -C frontend test --silent

# -----------------------------------------------------------------
# 5. No stray compiled files
# -----------------------------------------------------------------
git ls-files | grep -E "__pycache__|\.pyc$|\.pyo$|\.pyd$" || true

# -----------------------------------------------------------------
# 6. End‑to‑end API flow (skip in CI)
# -----------------------------------------------------------------
if [ "${CI:-false}" != "true" ]; then
  BASE_URL="${BASE_URL:-http://localhost:8000}"
  EMAIL="demo_$(date +%s)@example.com"
  PASSWORD="DemoPass123!"

  echo "Registering demo user $EMAIL"
  REG_RESP=$(curl -s -X POST "$BASE_URL/api/auth/register" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")
  if echo "$REG_RESP" | grep -q "\"detail\""; then
    echo "Registration failed: $REG_RESP"
    exit 1
  fi

  echo "Logging in..."
  LOGIN_RESP=$(curl -s -X POST "$BASE_URL/api/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")
  ACCESS_TOKEN=$(echo "$LOGIN_RESP" | jq -r .access_token)
  if [ -z "$ACCESS_TOKEN" ] || [ "$ACCESS_TOKEN" = "null" ]; then
    echo "Login failed: $LOGIN_RESP"
    exit 1
  fi

  AUTH_HEADER="Authorization: Bearer $ACCESS_TOKEN"

  echo "Fetching default family (scope)…"
  SCOPE_RESP=$(curl -s -H "$AUTH_HEADER" "$BASE_URL/api/me/default-family")
  FAMILY_ID=$(echo "$SCOPE_RESP" | jq -r .family_id)
  if [ -z "$FAMILY_ID" ] || [ "$FAMILY_ID" = "null" ]; then
    echo "Failed to get default family: $SCOPE_RESP"
    exit 1
  fi

  echo "Creating demo goal…"
  GOAL_PAYLOAD='{
    "name": "Demo Goal",
    "target_amount": 1000,
    "current_amount": 0,
    "monthly_contribution": 100,
    "target_date": "2030-01-01"
  }'
  CREATE_GOAL_RESP=$(curl -s -X POST "$BASE_URL/api/goals/$FAMILY_ID" \
    -H "$AUTH_HEADER" -H "Content-Type: application/json" \
    -d "$GOAL_PAYLOAD")
  GOAL_ID=$(echo "$CREATE_GOAL_RESP" | jq -r .id)
  if [ -z "$GOAL_ID" ] || [ "$GOAL_ID" = "null" ]; then
    echo "Goal creation failed: $CREATE_GOAL_RESP"
    exit 1
  fi

  echo "Listing goals…"
  LIST_GOALS_RESP=$(curl -s -H "$AUTH_HEADER" "$BASE_URL/api/goals/$FAMILY_ID")
  GOALS_COUNT=$(echo "$LIST_GOALS_RESP" | jq 'length')
  if [ "$GOALS_COUNT" -lt 1 ]; then
    echo "Goal list empty or invalid: $LIST_GOALS_RESP"
    exit 1
  fi

  echo "Fetching insights…"
  INSIGHTS_RESP=$(curl -s -H "$AUTH_HEADER" "$BASE_URL/api/insights/$FAMILY_ID")
  if [ -z "$INSIGHTS_RESP" ]; then
    echo "Insights request failed"
    exit 1
  fi
fi

echo "E2E smoke demo passed"
