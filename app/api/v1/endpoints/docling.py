from fastapi import APIRouter
from docling.datamodel import vlm_model_specs
import logging
from app.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/docling",
    tags=["Docling"],
    responses={404: {"description": "Not found"}},
)

@router.get("/models", summary="List available Docling models")
def list_models():
    """
    Returns a list of available Docling models that can be used for document parsing.
    """
    models = []
    for name in dir(vlm_model_specs):
        models.append(name)
    return {"models": models}
