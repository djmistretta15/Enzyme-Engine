"""
Configuration file for EAB Enzyme Discovery System
"""
import os
from typing import List, Dict

# NCBI Configuration
NCBI_EMAIL = os.getenv("NCBI_EMAIL", "your.email@example.com")
NCBI_API_KEY = os.getenv("NCBI_API_KEY", None)  # Optional, increases rate limit
NCBI_TOOL = "EAB_Enzyme_Discovery"
NCBI_RATE_LIMIT = 0.34  # Seconds between requests (3 per second max)

# Target Organisms
PRIMARY_ORGANISM = "Agrilus planipennis"
BUPRESTIDAE_FAMILY = "Buprestidae"
RELATED_SPECIES = [
    "Agrilus anxius",
    "Agrilus biguttatus",
    "Chrysobothris femorata",
    "Melanophila acuminata"
]

# Target Enzymes and Keywords
ENZYME_KEYWORDS = {
    "cellulase": {
        "ec_numbers": ["3.2.1.4"],
        "gh_families": ["GH5", "GH6", "GH7", "GH9", "GH12", "GH45", "GH48"],
        "keywords": ["cellulase", "endoglucanase", "cellobiohydrolase"]
    },
    "laccase": {
        "ec_numbers": ["1.10.3.2"],
        "gh_families": ["AA1"],
        "keywords": ["laccase", "phenol oxidase", "benzenediol oxidase"]
    },
    "peroxidase": {
        "ec_numbers": ["1.11.1.7"],
        "gh_families": ["AA2"],
        "keywords": ["peroxidase", "lignin peroxidase", "manganese peroxidase"]
    },
    "oxidase": {
        "ec_numbers": ["1.3.3.4", "1.14.13.1"],
        "gh_families": ["AA3", "AA4"],
        "keywords": ["oxidase", "glucose oxidase", "aryl-alcohol oxidase"]
    },
    "xylanase": {
        "ec_numbers": ["3.2.1.8"],
        "gh_families": ["GH10", "GH11"],
        "keywords": ["xylanase", "endo-1,4-beta-xylanase"]
    },
    "beta-glucosidase": {
        "ec_numbers": ["3.2.1.21"],
        "gh_families": ["GH1", "GH3"],
        "keywords": ["beta-glucosidase", "cellobiase"]
    },
    "mannanase": {
        "ec_numbers": ["3.2.1.78"],
        "gh_families": ["GH26"],
        "keywords": ["mannanase", "mannan endo-1,4-beta-mannosidase"]
    }
}

# Tissue Keywords
GUT_TISSUES = ["gut", "midgut", "foregut", "hindgut", "digestive", "alimentary", "intestine"]
DEVELOPMENTAL_STAGES = ["larva", "larval", "adult", "pupa", "pupal"]

# NCBI Databases
DATABASES = ["nucleotide", "protein", "sra", "bioproject", "biosample"]

# BLAST Configuration
BLAST_EVALUE_THRESHOLD = 1e-20
BLAST_IDENTITY_THRESHOLD = 50.0
BLAST_COVERAGE_THRESHOLD = 70.0

# Database Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "eab_enzymes.db")
CACHE_DIR = os.path.join(os.path.dirname(__file__), "data", "cache")

# Search Query Templates
QUERY_TEMPLATES = {
    "gut_transcriptome": '"{organism}"[Organism] AND ({tissues}) AND ({stages}) AND (transcriptome OR RNA-Seq)',
    "enzyme_specific": '"{organism}"[Organism] AND ({enzyme_keywords})',
    "family_wide": '"{family}"[Organism] AND ({tissues}) AND ({enzyme_keywords})'
}

# Confidence Scoring Weights
CONFIDENCE_WEIGHTS = {
    "blast_identity": 0.3,
    "blast_coverage": 0.2,
    "ec_match": 0.15,
    "gh_family_match": 0.15,
    "keyword_match": 0.1,
    "gut_tissue": 0.1
}

# Output Configuration
MAX_RESULTS_PER_QUERY = 500
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "data", "results")
EXPORT_FORMATS = ["csv", "json", "fasta", "excel"]

# Visualization Settings
CHART_COLORS = {
    "primary": "#284C3B",
    "secondary": "#C79A4B",
    "accent": "#C2C1BA",
    "background": "#F5F5F5",
    "charcoal": "#1F1F1F"
}

# Create necessary directories
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
