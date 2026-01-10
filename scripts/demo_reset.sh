#!/usr/bin/env bash
set -euo pipefail

echo "Tearing down demo containers and volumes..."
docker compose -f docker-compose.demo.yml down -v

# Remove any stray containers by name (defensive)
docker rm -f fga_demo_backend fga_demo_frontend fga_demo_db 2>/dev/null || true

echo "Demo environment reset complete."
echo "You can start a fresh demo with:"
echo "  docker compose -f docker-compose.demo.yml up --build"
