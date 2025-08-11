@echo off
echo Building Simple PDF Splitter GUI...
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM Build with PyInstaller
echo Building with PyInstaller...
pyinstaller SimplePDFSplitter.spec --noconfirm

REM Check if build succeeded
if exist "dist\SimplePDFSplitter\SimplePDFSplitter.exe" (
    echo.
    echo Build successful!
    echo Executable located at: dist\SimplePDFSplitter\SimplePDFSplitter.exe
    echo.
    echo To create installer, run Inno Setup Compiler with installer_setup.iss
) else (
    echo.
    echo Build failed! Check error messages above.
    exit /b 1
)

pause