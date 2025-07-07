import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from app.services.convert_service import convert_document

def main():
    print("Docling CLI - Document Conversion Tool")
    print("This tool converts PDF documents to various formats using Docling models.")
    parser = argparse.ArgumentParser(description="Convert a document using Docling and a specified VLM model.")
    parser.add_argument("file_path", help="Path to the PDF file to convert")
    parser.add_argument("output_format", choices=["json", "md", "html"], help="Desired output format")
    parser.add_argument("model_name", help="Docling model name (e.g., SMOLDOCLING_TRANSFORMERS)")

    args = parser.parse_args()

    try:
        output_file = convert_document(args.file_path, args.output_format, args.model_name)
        print(f"Conversion successful! Output saved to: {output_file}")
    except Exception as e:
        print(f"Conversion failed: {e}")

if __name__ == "__main__":
    main()