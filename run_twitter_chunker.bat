@echo off
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo 🔧 Please run setup.bat first to create the virtual environment.
    pause
    exit /b 1
)

REM Run the launcher (which will handle venv activation)
python launcher.py
pause