#!/usr/bin/env bash
set -e

# -------------------------------------------------
# OCI Bootstrap Script
# Installs Docker + Docker Compose plugin (Ubuntu)
# Clones or updates the repository
# Prepares .env file
# Builds and starts containers
# -------------------------------------------------

# 1. Install Docker prerequisites
echo "Updating package index..."
sudo apt-get update -y

echo "Installing required packages..."
sudo apt-get install -y ca-certificates curl gnupg

# 2. Add Docker’s official GPG key
echo "Adding Docker GPG key..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 3. Set up the stable repository
echo "Setting up Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. Install Docker Engine and Compose plugin
echo "Installing Docker Engine and Compose plugin..."
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verify installation
docker --version
docker compose version

# 5. Clone or update repository
REPO_URL="https://github.com/Tauhid-dev/Financial-goal-achiever.git"
TARGET_DIR="${PWD}/Financial-goal-achiever"

if [ -d "$TARGET_DIR/.git" ]; then
  echo "Repository already exists. Pulling latest changes..."
  cd "$TARGET_DIR"
  git pull
else
  echo "Cloning repository..."
  git clone "$REPO_URL" "$TARGET_DIR"
  cd "$TARGET_DIR"
fi

# 6. Ensure .env exists
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    echo "Creating .env from .env.example."
    cp .env.example .env
    echo "Please edit the following required environment variables as needed:"
    echo "DATABASE_URL=postgresql+asyncpg://..."
    echo "JWT_SECRET=change-me"
    echo "ENV=production"
    echo "LOG_LEVEL=INFO"
    echo "ACCESS_TOKEN_EXPIRE_MINUTES=60"
  else
    echo "No .env or .env.example found. Creating empty .env. Please edit manually."
    touch .env
  fi
else
  echo ".env already present."
fi

# Prompt user to edit .env if needed
read -p "Edit .env now? (y/n) " edit_choice
if [[ "$edit_choice" == "y" || "$edit_choice" == "Y" ]]; then
  ${EDITOR:-nano} .env
fi

# 7. Build and start containers
echo "Building Docker images..."
docker compose build

echo "Starting containers in detached mode..."
docker compose up -d

# 8. Health check
echo "Running health check..."
curl -s http://localhost:8000/health || echo "Health check failed."

echo "OCI bootstrap completed."
