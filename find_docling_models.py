#!/usr/bin/env python3
"""
Script to find where Docling stores its downloaded models
"""
import os
import sys
import importlib
import inspect
from pathlib import Path

# Import docling
try:
    import docling
    try:
        version = docling.__version__
    except AttributeError:
        version = "Unknown (no __version__ attribute)"
    print(f"Docling version: {version}")
    print(f"Docling package location: {docling.__file__}")
except ImportError:
    print("Docling is not installed")
    sys.exit(1)

# Try to directly load package info
try:
    import importlib.metadata
    try:
        version_info = importlib.metadata.metadata('docling')
        print(f"Package metadata version: {version_info['Version']}")
    except (importlib.metadata.PackageNotFoundError, KeyError):
        print("Package metadata not found")
except ImportError:
    print("importlib.metadata not available")

# List of potential cache directories
cache_dirs = [
    os.path.expanduser("~/.cache/docling"),
    os.path.expanduser("~/.config/docling"),
    os.path.expanduser("~/Library/Application Support/docling"),
    os.path.expanduser("~/Library/Caches/docling"),
    os.path.join(os.path.dirname(docling.__file__), "models"),
    os.path.join(os.path.dirname(docling.__file__), "artifacts"),
    os.path.join(os.path.dirname(docling.__file__), "data"),
]

# Check if directories exist
print("\nChecking potential cache directories:")
for d in cache_dirs:
    if os.path.exists(d):
        print(f"Found: {d}")
        # List some files in this directory
        try:
            files = os.listdir(d)
            if files:
                print(f"  Contains {len(files)} files/directories")
                for f in files[:5]:  # Show only first 5
                    full_path = os.path.join(d, f)
                    if os.path.isdir(full_path):
                        print(f"  - {f}/ (directory)")
                    else:
                        size = os.path.getsize(full_path) / (1024*1024)
                        print(f"  - {f} ({size:.2f} MB)")
                if len(files) > 5:
                    print(f"  - ... and {len(files)-5} more")
            else:
                print("  (empty directory)")
        except Exception as e:
            print(f"  Error listing directory: {e}")
    else:
        print(f"Not found: {d}")

# Try to execute a basic docling command
print("\nTrying to run a basic docling conversion to see if it downloads models:")
try:
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.txt') as f:
        f.write(b"Hello world")
        f.flush()
        
        print(f"Created temp file: {f.name}")
        
        # Try to access docling CLI functions
        print("Checking if docling has CLI functionality:")
        cli_found = False
        for name in dir(docling):
            if name.lower().startswith('cli') or name.lower().endswith('cli'):
                print(f"Found potential CLI module: {name}")
                cli_found = True
        
        if not cli_found:
            print("No CLI module found directly in docling")
except Exception as e:
    print(f"Error testing docling: {e}")

# Look for modules that might contain paths to model files
print("\nChecking for modules that might contain model paths:")
for name in dir(docling):
    if ("model" in name.lower() or "download" in name.lower() or 
        "path" in name.lower() or "cache" in name.lower() or 
        "config" in name.lower() or "artifact" in name.lower()):
        print(f"Found module: docling.{name}")
        try:
            module = getattr(docling, name)
            if inspect.ismodule(module):
                print(f"  Is a module")
                for subname in dir(module):
                    if ("path" in subname.lower() or "dir" in subname.lower() or 
                        "cache" in subname.lower() or "file" in subname.lower() or
                        "download" in subname.lower()):
                        print(f"  - Found attribute: {subname}")
        except Exception as e:
            print(f"  Error inspecting module: {e}")

# Look for large files in the docling package directory
print("\nLooking for large files in docling package directory:")
docling_dir = os.path.dirname(docling.__file__)
large_files = []

for root, dirs, files in os.walk(docling_dir):
    for file in files:
        if file.endswith(('.bin', '.pt', '.pth', '.onnx', '.model', '.data', '.pb')):
            path = os.path.join(root, file)
            try:
                size = os.path.getsize(path) / (1024*1024)  # Size in MB
                if size > 1:  # Only show files larger than 1MB
                    large_files.append((path, size))
            except Exception:
                pass

# Sort by size (largest first)
large_files.sort(key=lambda x: x[1], reverse=True)

# Print the largest files
if large_files:
    for path, size in large_files[:10]:
        rel_path = os.path.relpath(path, docling_dir)
        print(f"  {rel_path} ({size:.2f} MB)")
else:
    print("  No large model files found")
