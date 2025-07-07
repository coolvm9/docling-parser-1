from fastapi import APIRouter
from app.api.v1.endpoints import docling, health, convert

api_router = APIRouter()
api_router.include_router(docling.router)
api_router.include_router(health.router)
api_router.include_router(convert.router)
