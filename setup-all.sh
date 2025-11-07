#!/bin/bash
# Complete Setup Script for EAB Enzyme Discovery System

set -e  # Exit on error

echo "========================================================================"
echo "  ENZYME DISCOVERY SYSTEM - COMPLETE SETUP"
echo "========================================================================"
echo ""
echo "This script will install both backend (Python) and frontend (Node.js)"
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "Error: Please run this script from the Enzyme-Engine root directory"
    exit 1
fi

# Backend setup
echo ""
echo "========================================="
echo "STEP 1: Setting up Backend (Python)"
echo "========================================="
echo ""

cd backend

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.11+ from: https://www.python.org/downloads/"
    exit 1
fi

echo "Found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate and install
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt

echo ""
echo "✓ Backend setup complete!"

cd ..

# Frontend setup
echo ""
echo "========================================="
echo "STEP 2: Setting up Frontend (Node.js)"
echo "========================================="
echo ""

cd frontend

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    echo "Please install Node.js 18+ from: https://nodejs.org/"
    exit 1
fi

echo "Found: $(node --version)"

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

echo ""
echo "✓ Frontend setup complete!"

cd ..

# Final instructions
echo ""
echo "========================================================================"
echo "  ✓ INSTALLATION COMPLETE!"
echo "========================================================================"
echo ""
echo "📝 IMPORTANT: Configure NCBI credentials before running:"
echo ""
echo "   export NCBI_EMAIL='your.email@example.com'"
echo "   export NCBI_API_KEY='your_api_key'  # Optional but recommended"
echo ""
echo "   Get API key at: https://www.ncbi.nlm.nih.gov/account/"
echo ""
echo "========================================================================"
echo "🚀 QUICK START"
echo "========================================================================"
echo ""
echo "Backend (Terminal 1):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  export NCBI_EMAIL='your.email@example.com'"
echo "  python discover.py eab --max-results 50"
echo ""
echo "Frontend (Terminal 2):"
echo "  cd frontend"
echo "  npm run dev"
echo "  Open: http://localhost:3000"
echo ""
echo "========================================================================"
echo "📚 Documentation:"
echo "  - README.md           - Main documentation"
echo "  - SETUP.md            - Detailed setup guide"
echo "  - ORGANISM_GUIDE.md   - Target different organisms"
echo "========================================================================"
echo ""
