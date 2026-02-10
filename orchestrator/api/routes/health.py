from fastapi import APIRouter
from orchestrator.api.models.responses import HealthResponse, MetricsResponse
from orchestrator.services.orchestrator import ChatOrchestrator

router = APIRouter(tags=["health"])

# Initialize orchestrator (singleton pattern)
orchestrator = ChatOrchestrator()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint - verifies all components are operational
    """
    components = orchestrator.health_check()
    
    # Determine overall status
    all_healthy = all(status == "healthy" for status in components.values())
    status = "healthy" if all_healthy else "degraded"
    
    return HealthResponse(
        status=status,
        version="1.0.0",
        components=components
    )


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """
    Metrics endpoint - returns performance statistics
    """
    metrics = orchestrator.get_metrics()
    return MetricsResponse(**metrics)
