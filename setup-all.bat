@echo off
REM Complete Setup Script for EAB Enzyme Discovery System (Windows)

echo ========================================================================
echo   ENZYME DISCOVERY SYSTEM - COMPLETE SETUP
echo ========================================================================
echo.
echo This script will install both backend (Python) and frontend (Node.js)
echo.

REM Check if we're in the right directory
if not exist README.md (
    echo Error: Please run this script from the Enzyme-Engine root directory
    exit /b 1
)

REM Backend setup
echo.
echo =========================================
echo STEP 1: Setting up Backend (Python)
echo =========================================
echo.

cd backend

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    echo Please install Python 3.11+ from: https://www.python.org/downloads/
    exit /b 1
)

python --version

REM Create virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate and install
echo Installing Python dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt

echo.
echo Backend setup complete!

cd ..

REM Frontend setup
echo.
echo =========================================
echo STEP 2: Setting up Frontend (Node.js)
echo =========================================
echo.

cd frontend

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Node.js is not installed
    echo Please install Node.js 18+ from: https://nodejs.org/
    exit /b 1
)

node --version

REM Install dependencies
echo Installing Node.js dependencies...
call npm install

echo.
echo Frontend setup complete!

cd ..

REM Final instructions
echo.
echo ========================================================================
echo   INSTALLATION COMPLETE!
echo ========================================================================
echo.
echo IMPORTANT: Configure NCBI credentials before running:
echo.
echo    set NCBI_EMAIL=your.email@example.com
echo    set NCBI_API_KEY=your_api_key  # Optional but recommended
echo.
echo    Get API key at: https://www.ncbi.nlm.nih.gov/account/
echo.
echo ========================================================================
echo QUICK START
echo ========================================================================
echo.
echo Backend (Command Prompt 1):
echo   cd backend
echo   venv\Scripts\activate.bat
echo   set NCBI_EMAIL=your.email@example.com
echo   python discover.py eab --max-results 50
echo.
echo Frontend (Command Prompt 2):
echo   cd frontend
echo   npm run dev
echo   Open: http://localhost:3000
echo.
echo ========================================================================
echo Documentation:
echo   - README.md           - Main documentation
echo   - SETUP.md            - Detailed setup guide
echo   - ORGANISM_GUIDE.md   - Target different organisms
echo ========================================================================
echo.

pause
