# Docling integration service
from docling.document_converter import DocumentConverter
import os
import tempfile
import zipfile
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_tables_to_csv(pdf_path: str) -> str:
    """
    Extract tables from a PDF file using Docling and return path to zipped CSVs
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        str: Path to the ZIP file containing CSV tables
    """
    logger.info(f"Processing PDF: {pdf_path}")
    
    try:
        # Initialize Docling converter
        converter = DocumentConverter()
        
        # Convert the PDF
        result = converter.convert(pdf_path)
        
        # Get the document
        doc = result.document
        
        # Check if we have tables
        if not hasattr(doc, 'tables') or not doc.tables:
            logger.warning("No tables found in the document")
            # Create a temporary file to return
            zip_path = tempfile.mktemp(suffix=".zip")
            with zipfile.ZipFile(zip_path, 'w') as empty_zip:
                # Add a placeholder file to indicate no tables were found
                empty_zip.writestr('no_tables_found.txt', 'No tables were found in the document.')
            return zip_path
        
        # Create a temporary directory to store CSVs
        temp_dir = tempfile.mkdtemp()
        
        # Extract tables to CSV
        table_count = 0
        for idx, table in enumerate(doc.tables):
            try:
                # Convert table to dataframe
                table_df = table.export_to_dataframe()
                
                # Save as CSV
                csv_path = os.path.join(temp_dir, f"table_{idx+1}.csv")
                table_df.to_csv(csv_path, index=False)
                table_count += 1
                logger.info(f"Extracted table {idx+1} to {csv_path}")
            except Exception as e:
                logger.error(f"Error processing table {idx+1}: {str(e)}")
        
        logger.info(f"Extracted {table_count} tables from the document")
        
        # Create a zip file with all CSVs
        zip_path = tempfile.mktemp(suffix=".zip")
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                if os.path.isfile(file_path):
                    zip_file.write(file_path, file_name)
        
        logger.info(f"Created ZIP file at {zip_path}")
        
        return zip_path
        
    except Exception as e:
        logger.error(f"Error extracting tables: {str(e)}")
        raise
