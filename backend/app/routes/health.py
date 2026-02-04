from fastapi import APIRouter
from app.models.schemas import HealthCheckResponse
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now(),
        message="MediCare AI Backend is running!"
    )
