"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.routes import router
from app.services.detector import get_detector, _detector

app = FastAPI(
    title="Face Detection Service",
    description="A REST API for detecting human faces in images using MediaPipe",
    version="1.0.0",
)

app.include_router(router, prefix="/api", tags=["face-detection"])


from app.services.detector import get_detector, close_detector

@app.on_event("startup")
async def startup_event():
    # Instantiate detector at startup so failures surface early
    get_detector()


@app.on_event("shutdown")
async def shutdown_event():
    # Clean up detector resources
    close_detector()


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    # instantiate detector early so model load failures are visible at startup
    get_detector()


@app.on_event("shutdown")
async def shutdown_event():
    if _detector is not None:
        _detector.close()
