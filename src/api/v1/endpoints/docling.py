from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import tempfile
import os
from services.docling_service import extract_tables_to_csv

router = APIRouter()

@router.post("/extract-tables-csv/")
def extract_tables_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name
    try:
        csv_zip_path = extract_tables_to_csv(tmp_path)
        return FileResponse(csv_zip_path, filename="tables.zip", media_type="application/zip")
    finally:
        os.remove(tmp_path)
