@echo off
REM Enzyme Discovery System - Backend Setup Script (Windows)

echo ========================================
echo EAB ENZYME DISCOVERY - BACKEND SETUP
echo ========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo BACKEND SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo   1. Set your NCBI email (required):
echo      set NCBI_EMAIL=your.email@example.com
echo.
echo   2. (Optional) Set NCBI API key for higher rate limits:
echo      set NCBI_API_KEY=your_api_key
echo      Get one at: https://www.ncbi.nlm.nih.gov/account/
echo.
echo   3. Activate the virtual environment:
echo      venv\Scripts\activate.bat
echo.
echo   4. Run your first discovery:
echo      python main.py --organism "Agrilus planipennis" --max-results 50
echo.
echo   5. Or use the universal launcher:
echo      python discover.py eab --max-results 50
echo.

pause
