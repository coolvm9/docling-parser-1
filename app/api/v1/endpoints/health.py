from fastapi import APIRouter
import logging
from app.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/health",
    tags=["Health"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", summary="Check API health")
def health_check():
    """
    Simple health check endpoint to verify the API is running correctly.
    """
    logger.info("Health check requested")
    return {"status": "ok"}
