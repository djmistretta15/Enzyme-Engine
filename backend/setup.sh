#!/bin/bash
# Enzyme Discovery System - Backend Setup Script

set -e  # Exit on error

echo "========================================"
echo "EAB ENZYME DISCOVERY - BACKEND SETUP"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Python 3.11+ is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "✓ BACKEND SETUP COMPLETE!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Set your NCBI email (required):"
echo "     export NCBI_EMAIL='your.email@example.com'"
echo ""
echo "  2. (Optional) Set NCBI API key for higher rate limits:"
echo "     export NCBI_API_KEY='your_api_key'"
echo "     Get one at: https://www.ncbi.nlm.nih.gov/account/"
echo ""
echo "  3. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  4. Run your first discovery:"
echo "     python main.py --organism 'Agrilus planipennis' --max-results 50"
echo ""
echo "  5. Or use the universal launcher:"
echo "     python discover.py eab --max-results 50"
echo ""
