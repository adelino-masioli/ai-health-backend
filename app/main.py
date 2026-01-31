"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.database.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
    init_db()
    yield


app = FastAPI(
    title="AI Health Monitor API",
    description="REST API to receive, validate and store health data from the mobile app.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
