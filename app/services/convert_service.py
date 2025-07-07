import tempfile
import os
import logging
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline
from docling.datamodel.base_models import InputFormat
from docling.datamodel import vlm_model_specs
from docling.datamodel.pipeline_options import VlmPipelineOptions
from app.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = {"json", "md", "html"}

def get_vlm_model_spec(model_name: str):
    try:
        return getattr(vlm_model_specs, model_name)
    except AttributeError:
        raise ValueError(f"Model '{model_name}' is not supported.")

def convert_document(file_path: str, output_format: str, model_name: str) -> str:
    logger.info(f"Converting document: {file_path}, format: {output_format}, model: {model_name}")
    if output_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Format '{output_format}' not supported. Choose from {SUPPORTED_FORMATS}")

    vlm_spec = get_vlm_model_spec(model_name)
    pipeline_options = VlmPipelineOptions()
    pipeline_options.vlm_options = vlm_spec

    # converter = DocumentConverter(
    #     format_options={
    #         InputFormat.PDF: PdfFormatOption(
    #             pipeline_cls=VlmPipeline,
    #             pipeline_options=pipeline_options,
    #         ),
    #     }
    # )

    converter= DocumentConverter()

    try:
        result = converter.convert(file_path)
    except Exception as e:
        logger.error(f"Docling conversion failed: {e}")
        raise

    suffix = f".{output_format}"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        if output_format == "json":
            tmp.write(result.document.model_dump_json(indent=2).encode("utf-8"))
        elif output_format == "md":
            tmp.write(result.document.export_to_markdown().encode("utf-8"))
        elif output_format == "html":
            tmp.write(result.document.export_to_html().encode("utf-8"))
        tmp_path = tmp.name
    logger.info(f"Document converted and saved to: {tmp_path}")
    return tmp_path
