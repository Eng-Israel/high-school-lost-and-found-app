@echo off
REM Lost & Found App Installation Script for Windows
REM This script sets up the application automatically on any computer

setlocal enabledelayedexpansion

echo.
echo ========================================
echo  Lost & Found System Installer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please download and install Python from:
    echo   https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Get the current directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Create virtual environment
echo [*] Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
if errorlevel 1 (
    echo WARNING: Could not upgrade pip, continuing anyway...
) else (
    echo [OK] pip upgraded
)
echo.

REM Install requirements
echo [*] Installing dependencies...
echo    This may take 1-2 minutes...
echo.

if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo.
        echo Please check your internet connection and try again
        pause
        exit /b 1
    )
    echo [OK] All dependencies installed successfully
) else (
    echo ERROR: requirements.txt not found
    pause
    exit /b 1
)
echo.

REM Initialize database
echo [*] Initializing database...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('[OK] Database initialized')"
if errorlevel 1 (
    echo WARNING: Database initialization had an issue, but app may still work
)
echo.

echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo The Lost & Found System is ready to run.
echo.
echo To start the application:
echo   1. Run: python app.py
echo   2. Open browser to: http://127.0.0.1:5000
echo.
echo You can also use run.bat to start the app
echo.

REM Ask if user wants to run the app now
set /p RUNAPP="Do you want to start the application now? (y/n): "
if /i "%RUNAPP%"=="y" (
    echo.
    echo Starting application...
    echo.
    python app.py
) else (
    echo.
    echo To start later, run: python app.py
    echo.
    pause
)
