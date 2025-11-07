#!/bin/bash
# Enzyme Discovery System - Frontend Setup Script

set -e  # Exit on error

echo "========================================"
echo "EAB ENZYME DISCOVERY - FRONTEND SETUP"
echo "========================================"
echo ""

# Check Node.js version
echo "Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    echo "Please install Node.js 18+ from: https://nodejs.org/"
    exit 1
fi

node_version=$(node --version)
echo "Found Node.js $node_version"

# Check npm
echo "Checking npm..."
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed"
    exit 1
fi

npm_version=$(npm --version)
echo "Found npm $npm_version"

# Install dependencies
echo ""
echo "Installing Node.js dependencies..."
npm install

echo ""
echo "========================================"
echo "✓ FRONTEND SETUP COMPLETE!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Start the development server:"
echo "     npm run dev"
echo ""
echo "  2. Open your browser to:"
echo "     http://localhost:3000"
echo ""
echo "  3. Build for production:"
echo "     npm run build"
echo ""
echo "Note: Make sure the backend is running and has"
echo "generated results before using the frontend!"
echo ""
