# 📦 System Requirements & Dependencies

Complete reference for all software requirements and dependencies.

## 🖥️ System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+) |
| **Python** | 3.11 or higher |
| **Node.js** | 18.0 or higher |
| **RAM** | 4 GB minimum, 8 GB recommended |
| **Disk Space** | 2 GB for software + data storage |
| **Internet** | Required for NCBI API access |

### Recommended Setup

| Component | Recommendation |
|-----------|----------------|
| **Python** | 3.11 or 3.12 |
| **Node.js** | 20 LTS |
| **RAM** | 16 GB for large datasets |
| **CPU** | Multi-core for parallel processing |
| **SSD** | For faster database operations |

## 🐍 Python Dependencies (Backend)

### Core Dependencies

```txt
biopython>=1.81          # NCBI data access and sequence parsing
pandas>=2.0.0            # Data manipulation and analysis
numpy>=1.24.0            # Numerical operations
matplotlib>=3.7.0        # Visualization and chart generation
seaborn>=0.12.0          # Statistical visualizations
requests>=2.31.0         # HTTP requests to NCBI APIs
tqdm>=4.65.0             # Progress bars for long operations
```

### Optional Dependencies

```txt
streamlit>=1.28.0        # Web interface (alternative to React frontend)
openpyxl>=3.1.0          # Excel file export (.xlsx)
xlsxwriter>=3.1.0        # Excel formatting
```

### Development Dependencies

```txt
pytest>=7.4.0            # Unit testing
black>=23.7.0            # Code formatting
flake8>=6.1.0            # Linting
```

### Installation

```bash
cd backend
pip install -r requirements.txt
```

## 🎨 Node.js Dependencies (Frontend)

### Production Dependencies

```json
{
  "react": "^18.2.0",              // UI framework
  "react-dom": "^18.2.0",          // DOM rendering
  "recharts": "^2.10.0",           // Charts and visualizations
  "lucide-react": "^0.294.0"       // Icon library
}
```

### Development Dependencies

```json
{
  "@vitejs/plugin-react": "^4.2.1",     // Vite React plugin
  "vite": "^5.0.8",                     // Build tool
  "tailwindcss": "^3.3.6",              // CSS framework
  "postcss": "^8.4.32",                 // CSS processing
  "autoprefixer": "^10.4.16",           // CSS prefixing
  "eslint": "^8.55.0",                  // JavaScript linting
  "eslint-plugin-react": "^7.33.2",     // React linting
  "eslint-plugin-react-hooks": "^4.6.0" // React hooks linting
}
```

### Installation

```bash
cd frontend
npm install
```

## 🔧 External Requirements

### NCBI Account (Required)

- **Email address** - Required by NCBI for API access
- **API Key** - Optional but highly recommended
  - Without key: 3 requests/second
  - With key: 10 requests/second
- Get API key: https://www.ncbi.nlm.nih.gov/account/

### Optional Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| **BLAST+** | Local BLAST searches | https://blast.ncbi.nlm.nih.gov/doc/blast-help/downloadblastdata.html |
| **Docker** | Containerized deployment | https://www.docker.com/get-started |
| **VS Code** | Recommended IDE | https://code.visualstudio.com/ |

## 📊 Dependency Details

### Why Each Python Package?

**biopython**
- Parse GenBank and FASTA files
- Access NCBI Entrez API
- Handle biological sequences

**pandas**
- Tabular data manipulation
- Export to CSV, Excel, JSON
- Statistical analysis

**matplotlib**
- Generate PNG charts
- Enzyme distribution plots
- Confidence histograms

**requests**
- HTTP requests to NCBI
- API communication
- Data retrieval

### Why Each Node Package?

**react + react-dom**
- Modern UI framework
- Component-based architecture
- Fast rendering

**recharts**
- Data visualizations
- Bar charts, pie charts
- Interactive tooltips

**tailwindcss**
- Utility-first CSS
- Responsive design
- Fast styling

**vite**
- Fast development server
- Hot module replacement
- Optimized production builds

## 🔒 Security Considerations

### Environment Variables

Never commit these to Git:
- `NCBI_EMAIL`
- `NCBI_API_KEY`
- Any personal credentials

### Best Practices

1. Use `.env` files for local development
2. Set environment variables in production
3. Keep API keys private
4. Don't share your NCBI API key

## 🌐 Network Requirements

### NCBI API Access

- **Endpoints**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`
- **Ports**: HTTPS (443)
- **Rate Limits**:
  - 3 requests/second (no API key)
  - 10 requests/second (with API key)

### Firewall Configuration

Allow outbound HTTPS to:
- `*.ncbi.nlm.nih.gov`
- `*.nih.gov`

## 🖥️ Platform-Specific Notes

### Windows

- Use PowerShell or CMD
- Virtual environment: `venv\Scripts\activate.bat`
- Path separator: `\`

### macOS

- Use Terminal or iTerm2
- May need Xcode Command Line Tools
- Virtual environment: `source venv/bin/activate`

### Linux

- Use any terminal
- May need `python3-venv` package
- Virtual environment: `source venv/bin/activate`

## 📥 Installation Commands Summary

### Quick Install (All Platforms)

**Linux/Mac:**
```bash
./setup-all.sh
```

**Windows:**
```batch
setup-all.bat
```

### Manual Install

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate.bat on Windows
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

## ✅ Verification

### Check Python Packages

```bash
pip list | grep -E "biopython|pandas|matplotlib|requests"
```

### Check Node Packages

```bash
npm list --depth=0
```

### Test Imports

```bash
python -c "import Bio; import pandas; import matplotlib; print('✓ Success')"
```

## 🔄 Updating Dependencies

### Python

```bash
pip install --upgrade -r requirements.txt
```

### Node.js

```bash
npm update
```

## 📋 Dependency License Information

### Python Packages

| Package | License |
|---------|---------|
| biopython | Biopython License |
| pandas | BSD 3-Clause |
| numpy | BSD 3-Clause |
| matplotlib | PSF-based |
| requests | Apache 2.0 |

### Node Packages

| Package | License |
|---------|---------|
| react | MIT |
| vite | MIT |
| tailwindcss | MIT |
| recharts | MIT |

All dependencies use permissive open-source licenses compatible with research and commercial use.

## 🆘 Troubleshooting

### "pip: command not found"

```bash
python3 -m pip install --upgrade pip
```

### "npm: command not found"

Install Node.js from https://nodejs.org/

### Package conflicts

```bash
# Python
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Node.js
rm -rf node_modules package-lock.json
npm install
```

## 📞 Support

For dependency issues:
1. Check this file
2. Review `SETUP.md`
3. Verify Python/Node versions
4. Try clean reinstall

---

**All requirements in one place!** 📦
