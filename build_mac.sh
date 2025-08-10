#!/bin/bash
# Build script for Mac .app bundle
# Run this on a Mac computer

echo "========================================"
echo "Building Simple PDF Splitter for Mac"
echo "========================================"

# Install PyInstaller if needed
pip3 install pyinstaller

# Convert icon if needed (requires imagemagick)
# brew install imagemagick
# convert static/images/app_icon.ico static/images/app_icon.icns

# Create the .app bundle
pyinstaller --onefile \
    --windowed \
    --name "Simple PDF Splitter" \
    --icon="static/images/app_icon.icns" \
    --add-data "templates:templates" \
    --add-data "static:static" \
    --add-data "src:src" \
    --add-data ".env.example:." \
    --hidden-import flask \
    --hidden-import werkzeug \
    --hidden-import fitz \
    --hidden-import PyMuPDF \
    --hidden-import flask_wtf \
    --hidden-import flask_limiter \
    --hidden-import flask_talisman \
    --hidden-import markdown \
    --hidden-import dotenv \
    --osx-bundle-identifier "com.wallst-code.simple-pdf-splitter" \
    main.py

echo ""
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "App location: dist/Simple PDF Splitter.app"
echo ""
echo "To distribute:"
echo "1. Zip the .app file"
echo "2. Upload to GitHub Releases"
echo "3. Users download and double-click"
echo ""
echo "Note: Users will need to right-click and select 'Open'"
echo "the first time to bypass Gatekeeper."