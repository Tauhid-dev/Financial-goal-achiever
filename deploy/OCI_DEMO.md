# OCI Demo Runbook

## Prerequisites
- OCI VM with the following ports open:
  - **22** (SSH)
  - **5173** (frontend)
  - **8000** (backend API)
- Docker Engine and Docker Compose installed.
- Git installed.

## Setup Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/Tauhid-dev/Financial-goal-achiever.git
   cd Financial-goal-achiever
   ```

2. **Create a demo environment file**
   ```bash
   cat > .env.demo <<EOF
   # Replace <OCI_PUBLIC_IP> with the public IP of your OCI VM
   JWT_SECRET=change-me
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   CORS_ORIGINS=http://<OCI_PUBLIC_IP>:5173
   VITE_API_BASE_URL=http://<OCI_PUBLIC_IP>:8000
   EOF
   ```

3. **Start the demo stack**
   ```bash
   docker compose -f docker-compose.demo.yml --env-file .env.demo up --build -d
   ```

4. **Verify health**
   ```bash
   curl http://localhost:8000/health
   ./scripts/smoke_demo.sh
   ```

5. **Stop & clean up**
   ```bash
   docker compose -f docker-compose.demo.yml down
   ./scripts/demo_reset.sh   # if you want to reset the DB
   ```

## Troubleshooting
- **CORS errors** – ensure `CORS_ORIGINS` matches the OCI public IP.
- **Frontend cannot reach API** – adjust `VITE_API_BASE_URL` accordingly.
- **Containers keep restarting** – view logs:
  ```bash
  docker compose -f docker-compose.demo.yml logs -f backend db frontend
  ```

## Demo URLs
- **Frontend:** `http://<OCI_PUBLIC_IP>:5173`
- **Backend docs:** `http://<OCI_PUBLIC_IP>:8000/docs`
