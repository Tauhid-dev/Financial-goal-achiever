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

## One‑command demo
```bash
docker compose -f docker-compose.demo.yml up --build
```
The backend will be reachable at `http://localhost:8000` and the frontend at `http://localhost:5173`.

To stop and clean up:
```bash
docker compose -f docker-compose.demo.yml down -v
