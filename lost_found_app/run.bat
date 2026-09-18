@echo off
REM Quick start script for Lost & Found App

cd /d "%~dp0"

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run the app
python app.py
