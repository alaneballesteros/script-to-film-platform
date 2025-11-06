"""Main application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from script_to_film import __version__
from script_to_film.api.routes import router
from script_to_film.config.settings import settings

app = FastAPI(
    title="Script to Film Platform",
    description="AI-powered platform for converting scripts to short films",
    version=__version__,
    debug=settings.debug,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["api"])


@app.on_event("startup")
async def startup_event() -> None:
    """Run on application startup."""
    print(f"Starting Script to Film Platform v{__version__}")
    print(f"Environment: {settings.api_env}")
    print(f"Debug mode: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Run on application shutdown."""
    print("Shutting down Script to Film Platform")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "script_to_film.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
