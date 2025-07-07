from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="Docling Parser API",
    description="API for extracting structured data from documents using IBM Docling",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(api_router, prefix="/api/v1")
