#!/bin/bash
# Create DMG installer for Mac
# Run this AFTER building the .app with build_mac.sh

echo "Creating DMG installer..."

# Create a temporary directory for DMG contents
mkdir -p dmg_temp
cp -r "dist/Simple PDF Splitter.app" dmg_temp/
ln -s /Applications dmg_temp/Applications

# Create DMG
hdiutil create -volname "Simple PDF Splitter" \
    -srcfolder dmg_temp \
    -ov -format UDZO \
    "Simple PDF Splitter v1.0.0.dmg"

# Clean up
rm -rf dmg_temp

echo "DMG created: Simple PDF Splitter v1.0.0.dmg"
echo ""
echo "Users can:"
echo "1. Download the DMG"
echo "2. Double-click to mount"
echo "3. Drag app to Applications"
echo "4. Run from Applications folder"