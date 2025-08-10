"""
Setup script to create a portable Simple PDF Splitter distribution.
Downloads embedded Python and creates a complete portable package.
"""

import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

PYTHON_EMBEDDED_URL = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip"
PYTHON_EMBEDDED_SIZE = "~15MB"

def download_file(url, destination):
    """Download a file with progress indicator."""
    print(f"Downloading: {url}")
    print(f"Size: {PYTHON_EMBEDDED_SIZE}")
    
    def download_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(downloaded * 100 / total_size, 100)
        print(f"Progress: {percent:.1f}%", end='\r')
    
    urllib.request.urlretrieve(url, destination, download_progress)
    print("\nDownload complete!")

def setup_portable_python():
    """Set up embedded Python for portable distribution."""
    base_dir = Path(__file__).parent
    portable_dir = base_dir / "portable_dist"
    python_dir = portable_dir / "python_embedded"
    
    print("\n" + "="*50)
    print("Creating Portable Simple PDF Splitter")
    print("="*50)
    
    # Create distribution directory
    print("\n1. Creating distribution directory...")
    portable_dir.mkdir(exist_ok=True)
    python_dir.mkdir(exist_ok=True)
    
    # Download embedded Python
    print("\n2. Downloading embedded Python...")
    python_zip = portable_dir / "python_embedded.zip"
    
    if not python_zip.exists():
        download_file(PYTHON_EMBEDDED_URL, python_zip)
    else:
        print("Python already downloaded, skipping...")
    
    # Extract Python
    print("\n3. Extracting Python...")
    with zipfile.ZipFile(python_zip, 'r') as zip_ref:
        zip_ref.extractall(python_dir)
    
    # Copy application files
    print("\n4. Copying application files...")
    app_dir = portable_dir / "app"
    
    # Directories to copy
    dirs_to_copy = ["src", "static", "templates", "logs", "temp_uploads"]
    for dir_name in dirs_to_copy:
        src = base_dir / dir_name
        dst = app_dir / dir_name
        if src.exists():
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"   Copied: {dir_name}/")
    
    # Files to copy
    files_to_copy = [
        "main.py",
        "requirements.txt",
        "README.md",
        "create_shortcuts.py",
        ".env"  # Include .env for configuration
    ]
    for file_name in files_to_copy:
        src = base_dir / file_name
        dst = app_dir / file_name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"   Copied: {file_name}")
    
    # Create launcher batch file
    print("\n5. Creating launcher...")
    launcher_content = """@echo off
title Simple PDF Splitter
cd /d "%~dp0"

echo ========================================
echo Simple PDF Splitter - Portable Edition
echo ========================================
echo.
echo Starting application...
echo The browser will open to http://localhost:5000
echo.

REM Use embedded Python
set PYTHON_EXE=python_embedded\\python.exe

REM Install dependencies if needed
if not exist "python_embedded\\.deps_installed" (
    echo First run detected. Installing dependencies...
    "%PYTHON_EXE%" -m pip install --no-warn-script-location -r app\\requirements.txt
    echo. > "python_embedded\\.deps_installed"
)

REM Run the application
cd app
"..\\%PYTHON_EXE%" main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application failed to start
    pause
)
"""
    
    launcher_file = portable_dir / "Run Simple PDF Splitter.bat"
    with open(launcher_file, 'w') as f:
        f.write(launcher_content)
    
    print(f"   Created: {launcher_file.name}")
    
    # Create setup instructions
    print("\n6. Creating instructions...")
    instructions = """Simple PDF Splitter - Portable Edition
=====================================

QUICK START:
1. Double-click "Run Simple PDF Splitter.bat"
2. Your browser will open to http://localhost:5000
3. Start splitting PDFs!

FEATURES:
- No installation required
- No Python installation needed
- Completely portable
- All processing happens locally

FIRST RUN:
On first run, the app will install required packages.
This only happens once and takes about 30 seconds.

CREATING SHORTCUTS:
After first run, you can run:
  python app\\create_shortcuts.py
To create desktop shortcuts.

TROUBLESHOOTING:
- Make sure Windows Defender isn't blocking the app
- Ensure port 5000 isn't in use by another application
- Try running as Administrator if you have permission issues

=====================================
"""
    
    readme_file = portable_dir / "README_PORTABLE.txt"
    with open(readme_file, 'w') as f:
        f.write(instructions)
    
    print(f"   Created: {readme_file.name}")
    
    # Final summary
    print("\n" + "="*50)
    print("Portable package created successfully!")
    print("="*50)
    print(f"\nLocation: {portable_dir}")
    print(f"Total size: ~50MB (including Python)")
    print("\nTo distribute:")
    print("1. Zip the 'portable_dist' folder")
    print("2. Users extract and run 'Run Simple PDF Splitter.bat'")
    print("3. No Python installation required!")
    
    return portable_dir

def main():
    """Main setup function."""
    if sys.platform != 'win32':
        print("[ERROR] This script currently only supports Windows")
        return
    
    try:
        portable_dir = setup_portable_python()
        print("\n[SUCCESS] Portable distribution ready!")
    except Exception as e:
        print(f"\n[ERROR] Setup failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())