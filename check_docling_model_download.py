#!/usr/bin/env python3
"""
Script to check how Docling downloads its models
"""
import os
import sys
import tempfile
import time
import docling
from pathlib import Path

def try_find_method(module, name_pattern):
    """Search for method in module that match the pattern"""
    for name in dir(module):
        if name_pattern in name.lower():
            return name
    return None

# Print some basic information
print(f"Docling module location: {docling.__file__}")

# Check for important modules
models_module = getattr(docling, 'models', None)
if models_module:
    print(f"Found docling.models module: {models_module.__file__}")
    
    # Check if there's a download method
    download_method = try_find_method(models_module, 'download')
    if download_method:
        print(f"Found potential download method: {download_method}")
    
    # Check for default paths or directories
    path_method = try_find_method(models_module, 'path')
    if path_method:
        print(f"Found potential path method: {path_method}")

# Try to find more information from docling.cli module
if hasattr(docling, 'cli'):
    print("\nExamining CLI module:")
    cli = docling.cli
    for name in dir(cli):
        if 'download' in name.lower() or 'model' in name.lower() or 'path' in name.lower():
            print(f"Found CLI attribute: {name}")

# Try to run docling with verbose output to see where it looks for models
print("\nTrying to run docling with a small test file to see download behavior:")
try:
    # Create a small test PDF
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    pdf_path = os.path.join(tempfile.gettempdir(), "docling_test.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, "Test PDF for Docling")
    c.save()
    
    print(f"Created test PDF: {pdf_path}")
    
    # Run docling with verbose flag
    print("Running docling on test PDF with verbose flag:")
    import subprocess
    
    cmd = ["docling", pdf_path, "--verbose", "-v"]
    print(f"Running command: {' '.join(cmd)}")
    
    # Print a message about watching for model downloads
    print("Watching for model download messages in output...")
    
    # Run the command
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Monitor stdout and stderr for mentions of downloads or paths
    while True:
        stdout_line = process.stdout.readline()
        stderr_line = process.stderr.readline()
        
        if not stdout_line and not stderr_line and process.poll() is not None:
            break
            
        if stdout_line:
            line = stdout_line.strip()
            if any(x in line.lower() for x in ["download", "model", "cache", "artifact", "path"]):
                print(f"STDOUT: {line}")
                
        if stderr_line:
            line = stderr_line.strip()
            if any(x in line.lower() for x in ["download", "model", "cache", "artifact", "path"]):
                print(f"STDERR: {line}")
    
    # Wait for process to complete
    process.wait()
    
    print(f"Docling process exited with code: {process.returncode}")
    
except Exception as e:
    print(f"Error running docling test: {e}")

print("\nChecking user directories for downloaded models:")
home = Path.home()
locations = [
    home / ".docling",
    home / ".cache" / "docling",
    home / ".local" / "share" / "docling",
    home / "Library" / "Application Support" / "docling",
    home / "Library" / "Caches" / "docling"
]

for loc in locations:
    if loc.exists():
        print(f"Found directory: {loc}")
        # List contents
        files = list(loc.glob("**/*"))
        if files:
            print(f"  Contains {len(files)} files/directories")
            for f in files[:5]:  # Show only first 5
                if f.is_dir():
                    print(f"  - {f.name}/ (directory)")
                else:
                    size = os.path.getsize(f) / (1024*1024)
                    print(f"  - {f.name} ({size:.2f} MB)")
            if len(files) > 5:
                print(f"  - ... and {len(files)-5} more")
