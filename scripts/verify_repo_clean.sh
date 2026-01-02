#!/usr/bin/env bash
set -e

# -------------------------------------------------
# Repository Cleanliness Verification Script
# -------------------------------------------------

# 1. Ensure no uncommitted changes
echo "Checking git status..."
if [[ -n $(git status --porcelain) ]]; then
  echo "Repository has uncommitted changes:"
  git status --porcelain
  exit 1
else
  echo "No uncommitted changes."
fi

# 2. Ensure no ignored files are tracked
echo "Checking for tracked ignored files..."
if git ls-files | grep -E "__pycache__|\.pyc$|\.pyo$|\.pyd$|\.env$|\.venv/|venv/|env/; then
  echo "Found tracked files that should be ignored."
  exit 1
else
  echo "No tracked ignored files."
fi

# 3. Quick compile sanity for backend
echo "Compiling backend Python files..."
python -m compileall backend/app -q

# 4. Run tests if pytest is available
if command -v pytest >/dev/null 2>&1; then
  echo "Running test suite..."
  pytest -q
else
  echo "pytest not installed – skipping tests."
fi

echo "Repository verification completed successfully."
