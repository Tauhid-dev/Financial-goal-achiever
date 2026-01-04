from fastapi import FastAPI
from .routes import router
from .scopes import router as scopes_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Family Finance Intelligence API",
        version="0.1.0",
        description="Privacy‑first modular backend for family financial analysis",
    )
    app.include_router(router)
    app.include_router(scopes_router)
    return app

app = create_app()
