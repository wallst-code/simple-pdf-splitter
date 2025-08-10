@echo off
:: Simple PDF Splitter - User-Friendly Launcher
:: This provides a clean experience without terminal windows

title Simple PDF Splitter
color 1F
mode con: cols=60 lines=15

echo.
echo    =========================================
echo            SIMPLE PDF SPLITTER
echo    =========================================
echo.
echo           Starting application...
echo.
echo       Your browser will open shortly
echo         at http://localhost:5000
echo.
echo    =========================================
echo.

:: Hide the window after 3 seconds
timeout /t 3 /nobreak >nul

:: Minimize this window
if not "%1"=="min" (
    start /min cmd /c %0 min %*
    exit /b
)

:: Set Python path
set PYTHON_EXE=python_embedded\python.exe
cd /d "%~dp0"

:: Install dependencies silently if needed
if not exist "python_embedded\.deps_installed" (
    "%PYTHON_EXE%" -m pip install --no-warn-script-location -r app\requirements.txt >nul 2>&1
    echo. > "python_embedded\.deps_installed"
)

:: Run the application
cd app
"..\%PYTHON_EXE%" main.py