"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.errors import register_exception_handlers
from app.core.rate_limit import RateLimitMiddleware
from app.database.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
    init_db()
    yield


app = FastAPI(
    title="AI Health Monitor API",
    description=(
        "REST API to receive, validate and store health data from the mobile app. "
        "Provides patient registration, vitals ingestion and anomaly analysis."
    ),
    version="1.1.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "patients", "description": "Patient registration and identity."},
        {"name": "heart-rate", "description": "Heart rate ingestion endpoint."},
        {"name": "steps", "description": "Steps ingestion endpoint."},
        {"name": "analysis", "description": "Health anomaly analysis endpoint."},
    ],
)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.parsed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    RateLimitMiddleware,
    limit=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)

app.include_router(api_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check for deployment and load balancers."""
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    """Root redirect to docs."""
    return {"message": "AI Health Monitor API", "docs": "/docs"}
