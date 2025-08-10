"""
Build standalone EXE for Simple PDF Splitter
Creates a single executable file with everything bundled.
"""

import os
import sys
import shutil
from pathlib import Path

def build_exe():
    """Build the executable using PyInstaller."""
    
    print("\n" + "="*50)
    print("Building Simple PDF Splitter EXE")
    print("="*50)
    
    # Install PyInstaller if needed
    print("\n1. Checking PyInstaller...")
    try:
        import PyInstaller
        print("   PyInstaller found")
    except ImportError:
        print("   Installing PyInstaller...")
        os.system("pip install pyinstaller")
    
    # Create spec file for better control
    print("\n2. Creating build specification...")
    
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('src', 'src'),
        ('.env.example', '.'),
    ],
    hiddenimports=[
        'flask',
        'werkzeug',
        'fitz',
        'PyMuPDF',
        'flask_wtf',
        'flask_limiter',
        'flask_talisman',
        'markdown',
        'dotenv',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Simple PDF Splitter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='static/images/app_icon.ico',
)
"""
    
    with open('pdf_splitter.spec', 'w') as f:
        f.write(spec_content)
    
    print("   Created pdf_splitter.spec")
    
    # Build the EXE
    print("\n3. Building executable...")
    print("   This may take a few minutes...")
    
    result = os.system("pyinstaller pdf_splitter.spec --clean --noconfirm")
    
    if result == 0:
        print("\n" + "="*50)
        print("BUILD SUCCESSFUL!")
        print("="*50)
        print("\nExecutable location:")
        print("  dist/Simple PDF Splitter.exe")
        print("\nFile size: ~50-80 MB")
        print("\nUsers can now:")
        print("1. Download the EXE")
        print("2. Double-click to run")
        print("3. No installation needed!")
    else:
        print("\n[ERROR] Build failed")
        return False
    
    return True

def create_mac_app():
    """Create Mac .app bundle."""
    print("\n" + "="*50)
    print("Creating Mac App")
    print("="*50)
    
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('src', 'src'),
        ('.env.example', '.'),
    ],
    hiddenimports=[
        'flask',
        'werkzeug',
        'fitz',
        'PyMuPDF',
        'flask_wtf',
        'flask_limiter',
        'flask_talisman',
        'markdown',
        'dotenv',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Simple PDF Splitter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='Simple PDF Splitter.app',
    icon='static/images/app_icon.icns',  # Need to convert ico to icns
    bundle_identifier='com.wallst-code.simple-pdf-splitter',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'LSMinimumSystemVersion': '10.14.0',
    },
)
"""
    
    with open('pdf_splitter_mac.spec', 'w') as f:
        f.write(spec_content)
    
    print("To build for Mac, run on a Mac:")
    print("  pyinstaller pdf_splitter_mac.spec --clean")

if __name__ == "__main__":
    if sys.platform == "win32":
        build_exe()
        print("\nTo distribute:")
        print("1. Upload 'Simple PDF Splitter.exe' to GitHub Releases")
        print("2. Users download and double-click")
        print("3. That's it!")
    elif sys.platform == "darwin":
        create_mac_app()
    else:
        print("Linux: Use PyInstaller directly")
        print("  pyinstaller main.py --onefile --windowed --name 'Simple PDF Splitter'")