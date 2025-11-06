# 🧬 Emerald Ash Borer Enzyme Discovery System

> **A comprehensive bioinformatics platform for discovering wood-digesting enzymes in *Agrilus planipennis* and related Buprestidae beetles**

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-61dafb.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Overview

This software system mines NCBI databases to identify, annotate, and analyze genetic sequences encoding lignocellulolytic enzymes in the Emerald Ash Borer (*Agrilus planipennis*). The platform automatically:

- **Searches** NCBI for enzyme-related sequences across multiple databases (Protein, Nucleotide, SRA)
- **Retrieves** and parses GenBank records with full metadata
- **Annotates** enzyme types using keyword matching and EC numbers
- **Validates** gut-specific expression patterns
- **Filters** candidates using BLAST homology (optional)
- **Builds** a ranked "Digestive Matrix" of high-confidence enzyme candidates
- **Visualizes** results through an interactive web dashboard

## 🧩 Architecture

```
Enzyme-Engine/
├── backend/              # Python bioinformatics pipeline
│   ├── modules/          # Core analysis modules
│   │   ├── search_ncbi.py
│   │   ├── retrieve_sequences.py
│   │   ├── annotation.py
│   │   ├── blast_filter.py
│   │   ├── expression_validate.py
│   │   ├── storage.py
│   │   ├── matrix_builder.py
│   │   └── visualization.py
│   ├── data/             # SQLite database and cached results
│   ├── config.py         # Configuration and constants
│   ├── main.py           # CLI interface
│   └── requirements.txt
└── frontend/             # React web interface
    ├── src/
    │   ├── components/
    │   │   └── EABEnzymeExplorer.jsx
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    └── index.html
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** (for frontend)
- **Git**

### Backend Installation

```bash
# Clone repository
git clone <your-repo-url>
cd Enzyme-Engine/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure NCBI credentials (required)
export NCBI_EMAIL="your.email@example.com"
export NCBI_API_KEY="your_api_key"  # Optional but recommended
```

### Frontend Installation

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 📖 Usage

### Command Line Interface

#### Basic Search

Search for all enzymes in *Agrilus planipennis*:

```bash
cd backend
python main.py --organism "Agrilus planipennis" --max-results 200
```

#### Enzyme-Specific Search

Search for cellulases only:

```bash
python main.py --enzyme cellulase --database protein --max-results 100
```

#### Advanced Options

```bash
python main.py \
  --organism "Agrilus planipennis" \
  --enzyme laccase \
  --database protein \
  --max-results 150 \
  --min-confidence 0.7 \
  --no-skip-blast  # Enable BLAST (slow!)
```

#### View Database Statistics

```bash
python main.py --stats-only
```

### Available Enzyme Types

- `cellulase` - Cellulose degradation (EC 3.2.1.4, GH5/6/7/9/12/45/48)
- `laccase` - Lignin oxidation (EC 1.10.3.2, AA1)
- `peroxidase` - Lignin degradation (EC 1.11.1.7, AA2)
- `oxidase` - Oxidative degradation (EC 1.3.3.4, AA3/4)
- `xylanase` - Hemicellulose breakdown (EC 3.2.1.8, GH10/11)
- `beta-glucosidase` - Cellulose hydrolysis (EC 3.2.1.21, GH1/3)
- `mannanase` - Hemicellulose breakdown (EC 3.2.1.78, GH26)

## 📊 Output Files

After running the pipeline, results are saved to `backend/data/results/`:

| File | Description |
|------|-------------|
| `digestive_matrix.csv` | Ranked enzyme table (CSV) |
| `digestive_matrix.json` | Ranked enzyme table (JSON) |
| `discovery_report.txt` | Comprehensive text report |
| `enzyme_distribution.png` | Bar chart of enzyme types |
| `organism_distribution.png` | Pie chart of species |
| `confidence_histogram.png` | Confidence score distribution |
| `gh_family_distribution.png` | GH/AA family analysis |
| `tissue_stage_heatmap.png` | Tissue × stage matrix |
| `summary_dashboard.png` | Combined overview |

## 🔬 Scientific Background

### Target Enzymes

The EAB digests wood through a suite of lignocellulolytic enzymes:

**Cellulose Degradation:**
- Endoglucanases (GH5, GH9, GH45, GH48)
- Exoglucanases (GH6, GH7)
- β-glucosidases (GH1, GH3)

**Lignin Degradation:**
- Laccases (AA1)
- Peroxidases (AA2)
- Oxidases (AA3, AA4)

**Hemicellulose Degradation:**
- Xylanases (GH10, GH11)
- Mannanases (GH26)

### Related Species

The system searches across Buprestidae:
- *Agrilus planipennis* (Emerald Ash Borer)
- *Agrilus anxius* (Bronze Birch Borer)
- *Agrilus biguttatus* (Oak Splendour Beetle)
- *Chrysobothris femorata* (Flatheaded Appletree Borer)
- *Melanophila acuminata* (Fire-chaser Beetle)

## 🧪 Pipeline Details

### Step-by-Step Process

1. **NCBI Search** - Queries protein, nucleotide, and SRA databases
2. **Sequence Retrieval** - Downloads GenBank records with full annotations
3. **Enzyme Annotation** - Classifies enzymes using keyword/EC matching
4. **Expression Validation** - Confirms gut tissue expression
5. **BLAST Filtering** (optional) - Homology-based validation
6. **Confidence Scoring** - Multi-factor ranking algorithm
7. **Matrix Building** - Generates ranked enzyme table
8. **Visualization** - Creates charts and reports

### Confidence Scoring

Sequences are scored (0.0–1.0) based on:

| Factor | Weight |
|--------|--------|
| BLAST Identity | 30% |
| BLAST Coverage | 20% |
| EC Number Match | 15% |
| GH Family Match | 15% |
| Keyword Match | 10% |
| Gut Tissue Expression | 10% |

## 🎨 Web Interface

The React frontend provides:

- **Interactive table** with sorting and filtering
- **Search** by enzyme, organism, or accession
- **Filter** by tissue type and organism
- **Visualizations**: enzyme distribution, organism pie chart, GH families
- **Detail view** for individual sequences
- **CSV export** functionality

### Starting the Frontend

```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000` to explore results.

## ⚙️ Configuration

Edit `backend/config.py` to customize:

- Target organisms and enzyme keywords
- NCBI search parameters
- BLAST thresholds (E-value, identity, coverage)
- Confidence scoring weights
- Output directories

## 🔒 NCBI API Compliance

This tool follows NCBI's usage policies:

- **Rate limit**: 3 requests/second (with API key: 10/sec)
- **Email required**: Set `NCBI_EMAIL` environment variable
- **API key recommended**: Set `NCBI_API_KEY` for higher limits
- **Automatic delays** between requests

[Get NCBI API Key](https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/)

## 📦 Database Schema

SQLite database (`backend/data/eab_enzymes.db`) contains:

**Tables:**
- `organisms` - Taxonomy and species info
- `sequences` - Enzyme sequences with annotations
- `bioprojects` - NCBI BioProject metadata
- `sra_runs` - RNA-Seq experiment data
- `keywords` - Enzyme-related keywords
- `blast_results` - Homology search results

## 🐛 Troubleshooting

### Common Issues

**"No sequences found"**
- Check NCBI_EMAIL is set
- Try broader search terms
- Increase --max-results

**"Rate limit exceeded"**
- Get NCBI API key
- Reduce query frequency

**BLAST is very slow**
- Use `--skip-blast` flag (default)
- Process fewer sequences
- Consider local BLAST+ installation

### Performance Tips

- Use cached results: default behavior
- Skip BLAST for faster runs
- Start with `--max-results 50` for testing
- Use `--enzyme` flag to narrow searches

## 📚 Citation

If you use this software in your research, please cite:

```
EAB Enzyme Discovery System (2024)
https://github.com/your-username/Enzyme-Engine
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional enzyme families (e.g., cutinases, esterases)
- Integration with CAZy database
- RNA-Seq expression quantification
- Protein structure prediction
- Phylogenetic analysis

## 📄 License

MIT License

## 🔗 Resources

- [NCBI E-utilities Documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [BioPython Tutorial](https://biopython.org/wiki/Documentation)
- [CAZy Database](http://www.cazy.org/)
- [EAB Information (USDA)](https://www.aphis.usda.gov/aphis/resources/pests-diseases/emerald-ash-borer)

## 🎓 Scientific Context

The Emerald Ash Borer (EAB) represents a critical invasive species threatening ash tree populations. Understanding its wood-digesting enzyme repertoire has implications for:

- **Biocontrol strategies**
- **Industrial enzyme discovery** for biomass conversion
- **Evolutionary biology** of wood-boring insects
- **Comparative genomics** of Coleoptera

This platform accelerates enzyme discovery by automating data mining and annotation workflows that would otherwise require weeks of manual curation.

---

**Built with ❤️ for bioinformatics research**
