# 🚀 Installation & Setup Guide

Complete instructions for setting up the EAB Enzyme Discovery System.

## 📋 Prerequisites

### Required Software

- **Python 3.11+** - [Download here](https://www.python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/) (for frontend)
- **Git** - [Download here](https://git-scm.com/)

### Optional but Recommended

- **NCBI API Key** - [Get one here](https://www.ncbi.nlm.nih.gov/account/) (increases rate limit from 3 to 10 requests/sec)

## 🎯 Quick Setup (Recommended)

### Linux/Mac

```bash
# Clone repository
git clone <your-repo-url>
cd Enzyme-Engine

# Setup backend
cd backend
chmod +x setup.sh
./setup.sh

# Setup frontend (in new terminal)
cd ../frontend
chmod +x setup.sh
./setup.sh
```

### Windows

```batch
# Clone repository
git clone <your-repo-url>
cd Enzyme-Engine

# Setup backend
cd backend
setup.bat

# Setup frontend (in new terminal/tab)
cd ..\frontend
setup.bat
```

## 🐍 Backend Setup (Detailed)

### Step 1: Navigate to Backend

```bash
cd backend
```

### Step 2: Create Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```batch
python -m venv venv
venv\Scripts\activate.bat
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- **biopython** - NCBI data access and sequence parsing
- **pandas** - Data manipulation
- **matplotlib** - Visualizations
- **requests** - HTTP requests
- **tqdm** - Progress bars
- Plus optional packages (streamlit, excel export, testing tools)

### Step 4: Configure NCBI Credentials

**REQUIRED:** Set your email (NCBI requires this)

**Linux/Mac:**
```bash
export NCBI_EMAIL="your.email@example.com"
```

**Windows:**
```batch
set NCBI_EMAIL=your.email@example.com
```

**OPTIONAL:** Set API key for higher rate limits

**Linux/Mac:**
```bash
export NCBI_API_KEY="your_api_key_here"
```

**Windows:**
```batch
set NCBI_API_KEY=your_api_key_here
```

### Step 5: Test Installation

```bash
# Run with test dataset
python main.py --organism "Agrilus planipennis" --max-results 10

# Or use universal launcher
python discover.py eab --max-results 10
```

## 🎨 Frontend Setup (Detailed)

### Step 1: Navigate to Frontend

```bash
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

This will install:
- **React** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Data visualizations
- **Lucide React** - Icons

### Step 3: Start Development Server

```bash
npm run dev
```

The frontend will be available at: **http://localhost:3000**

### Step 4: Build for Production (Optional)

```bash
npm run build
npm run preview
```

## 📦 Dependencies Reference

### Backend (Python)

| Package | Version | Purpose |
|---------|---------|---------|
| biopython | ≥1.81 | NCBI data access, GenBank parsing |
| pandas | ≥2.0.0 | Data manipulation and analysis |
| numpy | ≥1.24.0 | Numerical operations |
| matplotlib | ≥3.7.0 | Chart generation |
| seaborn | ≥0.12.0 | Statistical visualizations |
| requests | ≥2.31.0 | HTTP requests to NCBI |
| tqdm | ≥4.65.0 | Progress bars |
| streamlit | ≥1.28.0 | Optional: Web interface |
| openpyxl | ≥3.1.0 | Optional: Excel export |
| xlsxwriter | ≥3.1.0 | Optional: Excel formatting |

### Frontend (Node.js)

| Package | Version | Purpose |
|---------|---------|---------|
| react | ^18.2.0 | UI framework |
| react-dom | ^18.2.0 | React DOM rendering |
| recharts | ^2.10.0 | Charts and graphs |
| lucide-react | ^0.294.0 | Icon library |
| vite | ^5.0.8 | Build tool and dev server |
| tailwindcss | ^3.3.6 | CSS framework |

## 🔧 Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named 'Bio'"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.bat  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**"NCBI email not set"**
```bash
# Set the environment variable
export NCBI_EMAIL="your.email@example.com"  # Linux/Mac
set NCBI_EMAIL=your.email@example.com       # Windows
```

**"Rate limit exceeded"**
```bash
# Get NCBI API key to increase rate limit
# Visit: https://www.ncbi.nlm.nih.gov/account/
export NCBI_API_KEY="your_key"
```

**"Python version too old"**
```bash
# Check version
python3 --version

# Install Python 3.11+ from python.org
# Or use pyenv:
pyenv install 3.11
pyenv local 3.11
```

### Frontend Issues

**"npm: command not found"**
```bash
# Install Node.js from nodejs.org
# Then verify:
node --version
npm --version
```

**"Port 3000 already in use"**
```bash
# Kill process on port 3000
# Linux/Mac:
lsof -ti:3000 | xargs kill -9

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or change port in vite.config.js
```

**"Module not found" errors**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json  # Linux/Mac
rmdir /s node_modules & del package-lock.json  # Windows

npm install
```

## 🧪 Verify Installation

### Backend Test

```bash
cd backend
source venv/bin/activate  # Linux/Mac only
python -c "import Bio; import pandas; import matplotlib; print('✓ All imports successful')"
```

### Frontend Test

```bash
cd frontend
npm run dev
# Visit http://localhost:3000
# You should see the Enzyme Explorer interface
```

## 📝 Environment Variables

Create a `.env` file in the backend directory (optional):

```bash
# backend/.env
NCBI_EMAIL=your.email@example.com
NCBI_API_KEY=your_api_key_here
```

Then load it before running:

**Linux/Mac:**
```bash
source .env
```

**Windows:**
```batch
# Use a .bat file to set variables
```

## 🔐 NCBI API Setup

### Why You Need an API Key

- **Without key:** 3 requests/second
- **With key:** 10 requests/second
- Prevents IP blocking
- Faster enzyme discovery

### How to Get One

1. Visit: https://www.ncbi.nlm.nih.gov/account/
2. Sign up or log in
3. Go to "Settings" → "API Key Management"
4. Create new key
5. Copy and set as environment variable

## 📚 Next Steps

After successful setup:

1. **Run First Discovery**
   ```bash
   cd backend
   python discover.py eab --max-results 50
   ```

2. **View Results**
   - Check `backend/data/results/` for outputs
   - Open `digestive_matrix.csv` in Excel
   - Review `discovery_report.txt`

3. **Launch Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Explore Documentation**
   - `README.md` - Main documentation
   - `ORGANISM_GUIDE.md` - Target different organisms
   - `backend/config.py` - Configuration options

## 🐳 Docker Setup (Advanced)

Coming soon! Docker support for containerized deployment.

## 🤝 Getting Help

If you encounter issues:

1. Check this setup guide
2. Review error messages carefully
3. Ensure all prerequisites are installed
4. Verify environment variables are set
5. Check Python/Node.js versions

## ✅ Installation Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] Git installed
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] NCBI_EMAIL environment variable set
- [ ] NCBI_API_KEY set (optional but recommended)
- [ ] Frontend dependencies installed
- [ ] Backend test successful
- [ ] Frontend runs on localhost:3000
- [ ] First enzyme discovery completed

---

**Ready to discover enzymes?** 🧬

```bash
python discover.py --list  # See all organism profiles
python discover.py eab --max-results 100  # Start discovering!
```
