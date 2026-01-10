from fastapi import FastAPI

def create_app() -> FastAPI:
    """
    FastAPI application factory.
    - Sets title, version, description.
    - Does NOT mount routers or start the server.
    """
    app = FastAPI(
        title="Financial Goal Achiever API",
        version="0.1.0",
        description="API contracts for PDF ingestion, budgeting, and savings‑goal projections.",
    )
    # Routers will be included by the consumer of this factory.
    return app
