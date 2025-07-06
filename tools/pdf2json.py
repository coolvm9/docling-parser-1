#!/usr/bin/env python3
"""
PDF to JSON converter using Docling

This script provides a simple wrapper around the docling CLI tool to convert PDF files to JSON format.
It handles both single files and directories of PDF files.

Usage:
    python pdf2json.py input_file.pdf [--output output_dir/]
    python pdf2json.py input_directory/ [--output output_dir/]
"""

import argparse
import os
import subprocess
import sys


def convert_pdf_to_json(input_path, output_path=None, verbose=False):
    """
    Convert PDF file(s) to JSON using docling CLI
    
    Args:
        input_path: Path to a PDF file or directory containing PDF files
        output_path: Output directory (optional)
        verbose: Enable verbose output
    
    Returns:
        True if conversion was successful, False otherwise
    """
    cmd = ["docling", input_path, "--to", "json"]
    
    if output_path:
        cmd.extend(["--output", output_path])
    
    if verbose:
        cmd.append("-v")
    
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Success! Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running docling: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Convert PDF files to JSON using docling")
    parser.add_argument("input", help="PDF file or directory containing PDF files")
    parser.add_argument("--output", help="Output directory for JSON files")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Check if input exists
    if not os.path.exists(args.input):
        print(f"Error: Input path '{args.input}' does not exist")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    if args.output and not os.path.exists(args.output):
        os.makedirs(args.output)
        print(f"Created output directory: {args.output}")
    
    success = convert_pdf_to_json(args.input, args.output, args.verbose)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
