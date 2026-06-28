from fastapi import APIRouter

from app.config.settings import settings

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
async def health_check():
    """
    Health check endpoint.

    Used by:
    - Developers
    - Docker
    - Kubernetes
    - Monitoring tools
    """

    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }