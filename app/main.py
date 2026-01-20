"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.services.detector import get_detector, close_detector


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup: Instantiate detector so failures surface early
    get_detector()
    yield
    # Shutdown: Clean up detector resources
    close_detector()


app = FastAPI(
    title="Face Detection Service",
    description="A REST API for detecting human faces in images using MediaPipe",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api", tags=["face-detection"])


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}
