# First Demo – Financial Goal Achiever

## Running on OCI (demo‑only)

See the [OCI demo runbook](deploy/OCI_DEMO.md) and the bootstrap script
`scripts/oci_demo_bootstrap.sh` for step‑by‑step instructions.

## Prerequisites
- **Python 3.13+** (or 3.11+)
- **Node 18+** and **npm**
- **PostgreSQL** (or Docker Compose which will start a local instance)

## Backend setup
1. Create and activate a virtual environment  
   ```bash
   python -m venv myenv
   source ./myenv/bin/activate
   ```
2. Install Python dependencies  
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Copy the example env file and edit if needed  
   ```bash
   cp backend/.env.example backend/.env
   # edit backend/.env – at minimum set DATABASE_URL and JWT_SECRET
   ```
4. Run the API (development mode)  
   ```bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Frontend setup
1. Install Node dependencies  
   ```bash
   cd frontend
   npm install
   ```
2. Copy the example env file and edit if needed  
   ```bash
   cp .env.example .env
   # set VITE_API_BASE_URL to the backend URL, e.g. http://localhost:8000
   ```
3. Run the dev server  
   ```bash
   npm run dev   # serves at http://localhost:5173
   ```

## One‑command demo
```bash
docker compose -f docker-compose.demo.yml up --build
```
The backend will be reachable at `http://localhost:8000` and the frontend at `http://localhost:5173`.

To stop and clean up:
```bash
docker compose -f docker-compose.demo.yml down -v
```

## Demo reset
If you need a fresh demo environment (e.g., to clear the database), run:
```bash
./scripts/demo_reset.sh
```

## Full end‑to‑end smoke test
After the containers are up, you can verify the complete flow with the provided smoke script:
```bash
./scripts/smoke_demo.sh
```
The script will:
- Build the frontend
- Run backend and frontend tests
- Register a demo user, log in, and obtain a JWT
- Fetch the default family (scope)
- Create, list, and delete a demo goal
- Retrieve documents, summary, transactions, and insights
- Report **E2E smoke demo passed** on success

## Expected URLs
- Backend API health: `http://localhost:8000/health`
- Frontend UI: `http://localhost:5173`

You can now start the demo, run the smoke test, and reset when needed.
