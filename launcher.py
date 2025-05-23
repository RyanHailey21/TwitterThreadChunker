"""
Launcher script for Twitter Thread Chunker with Virtual Environment Support
Automatically activates venv, starts Streamlit and opens browser
"""

import subprocess
import webbrowser
import time
import sys
import os
from pathlib import Path

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    app_path = script_dir / "app.py"
    venv_path = script_dir / "venv"
    
    # Check if app.py exists
    if not app_path.exists():
        print("❌ Error: app.py not found in the same directory as launcher.py")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Check if virtual environment exists
    if not venv_path.exists():
        print("❌ Error: Virtual environment not found!")
        print("🔧 Please run setup.bat first to create the virtual environment.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("🧵 Starting Twitter Thread Chunker...")
    print("🔄 Using virtual environment...")
    print("📱 Your app will open in your browser shortly...")
    
    # Determine the Python executable in the venv
    if os.name == 'nt':  # Windows
        python_exe = venv_path / "Scripts" / "python.exe"
    else:  # macOS/Linux
        python_exe = venv_path / "bin" / "python"
    
    # Start Streamlit in the background
    try:
        # Change to the script directory
        os.chdir(script_dir)
        
        # Start streamlit using the venv Python
        process = subprocess.Popen(
            [str(python_exe), "-m", "streamlit", "run", "app.py", "--server.headless=true"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        # Wait a moment for Streamlit to start
        time.sleep(3)
        
        # Open browser
        webbrowser.open("http://localhost:8501")
        
        print("✅ App is running!")
        print("🌐 Opening in your default browser...")
        print("🔒 Using isolated virtual environment")
        print("❌ Close this window to stop the app")
        
        # Keep the process alive
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            process.terminate()
            
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        print("💡 Try running setup.bat first if you haven't already.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
