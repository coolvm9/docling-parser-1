from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import FileResponse
import os
import tempfile
from app.services.convert_service import convert_document, SUPPORTED_FORMATS
from app.models.convert_request import ConvertRequest
import logging
from app.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/convert",
    tags=["Convert"],
    responses={404: {"description": "Not found"}},
)

def convert_request_as_form(
    output_format: str = Form(..., description="Output format: json, md, or html"),
    model_name: str = Form(..., description="Docling model name (e.g., SMOLDOCLING_TRANSFORMERS)"),
) -> ConvertRequest:
    return ConvertRequest(output_format=output_format, model_name=model_name)

@router.post(
    "/",
    summary="Convert document to a specified format using a selected Docling model",
    description="Upload a PDF, specify output format (json, md, html), and model name. Returns the converted file.",
)
def convert_api(
    file: UploadFile = File(..., description="PDF file to convert"),
    req: ConvertRequest = Depends(convert_request_as_form),
):
    logger.info(f"Received file: {file.filename}, format: {req.output_format}, model: {req.model_name}")
    if not file.filename.lower().endswith(".pdf"):
        logger.warning("File is not a PDF.")
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    if req.output_format not in SUPPORTED_FORMATS:
        logger.warning(f"Unsupported format: {req.output_format}")
        raise HTTPException(status_code=400, detail=f"Format '{req.output_format}' not supported. Choose from {SUPPORTED_FORMATS}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name
    try:
        out_path = convert_document(tmp_path, req.output_format, req.model_name)
        filename = os.path.basename(file.filename).rsplit(".", 1)[0] + f".{req.output_format}"
        logger.info(f"Returning converted file: {filename}")
        return FileResponse(out_path, filename=filename)
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(tmp_path)
        logger.info(f"Temporary file removed: {tmp_path}")
