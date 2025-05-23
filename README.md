# Twitter Thread Chunker

Transform your long thoughts into perfectly sized Twitter threads!

## 🚀 Quick Setup (Recommended)

1. **Install Python** (if not already installed)
   - Download from https://python.org
   - Make sure to check "Add Python to PATH" during installation

2. **Run Setup** (One-time only)
   - Double-click `setup.bat` in this folder
   - This will create a virtual environment and install dependencies

3. **Launch the App**
   - Double-click `run_twitter_chunker.bat`
   - Your app will open in your browser automatically!

## 📁 What's in This Folder

- **`setup.bat`** - One-time setup (creates venv & installs dependencies)
- **`run_twitter_chunker.bat`** - Double-click to launch app
- **`app.py`** - Main Streamlit interface
- **`twitter_chunker.py`** - Core chunking logic
- **`launcher.py`** - Launch script with venv support
- **`requirements.txt`** - Python dependencies
- **`venv/`** - Virtual environment (created by setup.bat)

## 🖥️ Creating Desktop Shortcut

1. Right-click on your desktop → "New" → "Shortcut"
2. Browse to this folder and select `run_twitter_chunker.bat`
3. Name it "Twitter Thread Chunker"
4. (Optional) Right-click shortcut → "Properties" → "Change Icon" to customize
5. (Optional) Right-click shortcut → "Pin to taskbar"

## 🔧 Manual Setup (Alternative)

If you prefer command line:
```cmd
# Navigate to the app folder
cd C:\Users\ryanh\Documents\TwitterThreadChunker

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python launcher.py
```

## 📱 How to Use

1. Launch the app (browser will open automatically)
2. Either type/paste your text or upload a .txt file
3. See your text automatically chunked into tweets
4. Copy individual tweets or the entire thread
5. Paste into Twitter or your scheduling tool

## ✨ Features

- ✅ Automatically splits at word boundaries
- ✅ Adds thread indicators (1/5, 2/5, etc.)
- ✅ Shows character counts and warnings
- ✅ Individual and bulk copy options
- ✅ File upload support
- ✅ Clean, easy-to-use interface
- ✅ Isolated virtual environment (no conflicts!)

## 🛠️ Troubleshooting

- **App won't start**: Run `setup.bat` first if you haven't already
- **"Virtual environment not found"**: Run `setup.bat` to create it
- **Python not found**: Make sure Python is installed and in your PATH
- **Browser doesn't open**: Manually go to http://localhost:8501
- **Want to update**: Re-run `setup.bat` to update dependencies

## 🔄 Updating the App

To update dependencies:
1. Run `setup.bat` again, or
2. Manually: activate venv → `pip install --upgrade -r requirements.txt`

## 🎯 Why Virtual Environment?

✅ **Clean**: Dependencies isolated from other Python projects  
✅ **Safe**: No conflicts with system Python packages  
✅ **Portable**: Easy to delete/recreate if needed  
✅ **Best Practice**: Professional Python development standard  

Enjoy chunking your thoughts! 🧵
