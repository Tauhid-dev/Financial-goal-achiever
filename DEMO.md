# First Demo – Financial Goal Achiever

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

## One‑command demo flow
Open **two terminals**:

**Terminal 1 – Backend**
```bash
source ./myenv/bin/activate
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 – Frontend**
```bash
cd frontend
npm run dev
```

Now run the end‑to‑end smoke script (it will exercise the full API):
```bash
./scripts/smoke_demo.sh
```

### Expected demo steps performed by the script
1. Health‑check the backend.
2. Build the frontend (ensures the build succeeds).
3. Run backend unit tests.
4. Run frontend unit tests.
5. Register a random demo user.
6. Log in and obtain a JWT.
7. Fetch the default family (scope) for the user.
8. Create a demo goal.
9. List goals (the newly created one should appear).
10. Retrieve insights for the family.
11. Print **“E2E smoke demo passed”** on success.

## Troubleshooting
- **CORS errors** – ensure `CORS_ORIGINS` in `backend/.env` includes the frontend URL (`http://localhost:5173` by default).  
- **Missing JWT_SECRET** – set a strong secret in `backend/.env`.  
- **Database not reachable** – verify `DATABASE_URL` points to a running PostgreSQL instance or use the Docker Compose file (`docker compose up -d`).  
- **Port conflicts** – make sure ports 8000 (backend) and 5173 (frontend) are free.  

Happy demoing!
