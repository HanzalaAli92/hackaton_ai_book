from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
import time
from ...config import settings


router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    dependencies: Dict[str, str]


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    # Check dependencies (simplified for this example)
    dependencies_status = {
        "qdrant": "unknown",  # Would check actual connection
        "neon": "unknown",    # Would check actual connection
        "openrouter": "unknown"  # Would check actual connection
    }

    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version=settings.version,
        dependencies=dependencies_status
    )


@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint to verify the service is ready to handle requests.
    """
    # In a real implementation, this would check if all dependencies are ready
    return {"status": "ready"}