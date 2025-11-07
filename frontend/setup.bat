@echo off
REM Enzyme Discovery System - Frontend Setup Script (Windows)

echo ========================================
echo EAB ENZYME DISCOVERY - FRONTEND SETUP
echo ========================================
echo.

REM Check Node.js
echo Checking Node.js version...
node --version
if %errorlevel% neq 0 (
    echo Error: Node.js is not installed
    echo Please install Node.js 18+ from: https://nodejs.org/
    exit /b 1
)

REM Check npm
echo Checking npm...
npm --version
if %errorlevel% neq 0 (
    echo Error: npm is not installed
    exit /b 1
)

REM Install dependencies
echo.
echo Installing Node.js dependencies...
npm install

echo.
echo ========================================
echo FRONTEND SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo   1. Start the development server:
echo      npm run dev
echo.
echo   2. Open your browser to:
echo      http://localhost:3000
echo.
echo   3. Build for production:
echo      npm run build
echo.
echo Note: Make sure the backend is running and has
echo generated results before using the frontend!
echo.

pause
