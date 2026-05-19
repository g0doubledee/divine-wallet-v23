"""API router - all endpoints."""

from fastapi import APIRouter

v1_financial_router = APIRouter(prefix="/v1", tags=["financial"])

@v1_financial_router.get("/health")
async def health():
    return {"status": "healthy", "version": "23.0"}