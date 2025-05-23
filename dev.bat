@echo off
echo 🔧 Development Mode - Twitter Thread Chunker

REM Check if venv exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo 🔧 Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Start development server with auto-reload
echo 🚀 Starting development server...
echo 📝 Code changes will auto-reload
echo 🌐 App will open at http://localhost:8501
echo ❌ Press Ctrl+C to stop

streamlit run app.py

pause