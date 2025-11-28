@echo off
echo Starting JTalk Web Interface...
echo ================================

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install flask flask-cors transformers torch numpy

REM Start the web interface
echo Starting JTalk Web Interface...
python run_web_interface.py

pause
