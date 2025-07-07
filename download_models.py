#!/usr/bin/env python
"""
Script to download Docling models upfront.
"""

import logging
import os
import sys

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
from app.core.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def download_models():
    """Download Docling models upfront."""
    try:
        from docling.datamodel import vlm_model_specs
        from docling.pipeline.vlm_pipeline import VlmPipeline
        from docling.datamodel.pipeline_options import VlmPipelineOptions

        logger.info("Starting Docling model download")
        # Specify which model you want to download
        model_name = "SMOLDOCLING_TRANSFORMERS"
        
        # Get model specification
        model_spec = getattr(vlm_model_specs, model_name)
        
        # Initialize pipeline options with the model spec
        pipeline_options = VlmPipelineOptions()
        pipeline_options.vlm_options = model_spec
        
        # Create the pipeline - this will trigger the model download
        logger.info(f"Downloading model: {model_name}")
        pipeline = VlmPipeline(pipeline_options=pipeline_options)
        
        logger.info(f"Successfully downloaded model: {model_name}")
        
        # Print the cache directory location
        import os
        from huggingface_hub import HfFolder
        cache_dir = os.getenv("HF_HOME", os.path.join(os.path.expanduser("~"), ".cache", "huggingface"))
        logger.info(f"Models are cached at: {cache_dir}/models")
        
        return True
    except Exception as e:
        logger.error(f"Error downloading models: {e}")
        return False

if __name__ == "__main__":
    success = download_models()
    sys.exit(0 if success else 1)
