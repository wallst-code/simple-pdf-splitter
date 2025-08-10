@echo off
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
set PYTHON_EXE=python_embedded\python.exe

REM Install dependencies if needed
if not exist "python_embedded\.deps_installed" (
    echo First run detected. Installing dependencies...
    "%PYTHON_EXE%" -m pip install --no-warn-script-location -r app\requirements.txt
    echo. > "python_embedded\.deps_installed"
)

REM Run the application
cd app
"..\%PYTHON_EXE%" main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application failed to start
    pause
)
