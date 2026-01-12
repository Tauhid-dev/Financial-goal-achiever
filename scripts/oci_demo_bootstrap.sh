#!/usr/bin/env bash
set -euo pipefail

# Verify Docker and Docker Compose are available
command -v docker >/dev/null 2>&1 || { echo "Docker is not installed"; exit 1; }

# Detect Docker Compose implementation
if docker compose version >/dev/null 2>&1; then
    COMPOSE="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    COMPOSE="docker-compose"
else
    echo "Docker Compose is not installed (need either 'docker compose' plugin or 'docker-compose')."
    exit 1
fi

# Ensure .env.demo exists; if not, create a template for the user to edit
if [[ ! -f .env.demo ]]; then
  cat > .env.demo <<EOF
# Edit the <OCI_PUBLIC_IP> placeholder below
JWT_SECRET=change-me
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://<OCI_PUBLIC_IP>:5173
VITE_API_BASE_URL=http://<OCI_PUBLIC_IP>:8000
EOF
  echo ".env.demo created. Please edit the <OCI_PUBLIC_IP> placeholder before re-running this script."
  exit 0
fi

# Bring up the demo stack
$COMPOSE -f docker-compose.demo.yml --env-file .env.demo up --build -d

# Show next steps
echo "=== OCI Demo is up ==="
echo "Frontend URL: http://<OCI_PUBLIC_IP>:5173"
echo "Backend docs: http://<OCI_PUBLIC_IP>:8000/docs"
echo "To stop the demo: $COMPOSE -f docker-compose.demo.yml down"
