@echo off
echo ============================================
echo  Cat YouTube Automation - Windows Setup
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)
echo [OK] Python found

REM Install Python packages
echo.
echo Installing Python packages...
pip install -r requirements.txt
echo [OK] Python packages installed

REM Check FFmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] FFmpeg not found!
    echo Please install FFmpeg:
    echo   1. Go to https://ffmpeg.org/download.html
    echo   2. Download Windows build
    echo   3. Extract and add to PATH
    echo   OR use: winget install ffmpeg
    echo.
    pause
)
echo [OK] FFmpeg found

echo.
echo ============================================
echo  Setup complete! Next steps:
echo  1. Edit config.py with your API keys
echo  2. Run: python main.py --scripts-only
echo     (test script generation first)
echo  3. Run: python main.py --skip-upload
echo     (test full video generation)
echo  4. Run: python main.py
echo     (full pipeline with YouTube upload)
echo ============================================
pause
