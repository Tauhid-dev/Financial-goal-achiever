from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router as api_router
from .core.config import Config

def create_app() -> FastAPI:
    app = FastAPI(
        title="Family Finance Intelligence API",
        version="0.1.0",
        description="Privacy‑first backend for family financial analysis",
    )
    app.include_router(api_router)

    # Include auth router
    # CORS configuration – origins from env var
    origins = [o.strip() for o in Config.CORS_ORIGINS.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    from ..app.auth.routes import router as auth_router
    app.include_router(auth_router)
    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app

app = create_app()
