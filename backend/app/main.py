from fastapi import FastAPI
from .api import router as api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Family Finance Intelligence API",
        version="0.1.0",
        description="Privacy‑first backend for family financial analysis",
    )
    app.include_router(api_router)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app

app = create_app()
