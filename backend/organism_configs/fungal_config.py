"""
Configuration for Fungal Enzyme Discovery
Target: Wood-rotting fungi (white-rot and brown-rot)
"""

# Target Organisms
PRIMARY_ORGANISM = "Phanerochaete chrysosporium"
ORGANISM_FAMILY = "Polyporaceae"
RELATED_SPECIES = [
    "Phanerochaete chrysosporium",  # White-rot
    "Trametes versicolor",  # Turkey tail (white-rot)
    "Pleurotus ostreatus",  # Oyster mushroom
    "Postia placenta",  # Brown-rot
    "Gloeophyllum trabeum",  # Brown-rot
    "Ceriporiopsis subvermispora"  # White-rot
]

SPECIES_COMMON_NAMES = {
    "Phanerochaete chrysosporium": "White-Rot Fungus",
    "Trametes versicolor": "Turkey Tail Mushroom",
    "Pleurotus ostreatus": "Oyster Mushroom",
    "Postia placenta": "Brown Cubical Rot Fungus",
}

# Fungal growth conditions (instead of tissues)
GROWTH_CONDITIONS = [
    "lignocellulose", "cellulose", "wood",
    "secreted", "extracellular", "culture",
    "mycelium", "fruiting body"
]

# Growth phases
DEVELOPMENTAL_STAGES = [
    "exponential", "stationary", "decay",
    "vegetative", "reproductive",
    "ligninolytic", "cellulolytic"
]

# Fungal-specific enzyme families (they're the masters!)
FUNGAL_SPECIFIC_ENZYMES = {
    "lignin_peroxidase": {
        "keywords": ["lignin peroxidase", "LiP"],
        "ec_numbers": ["1.11.1.14"],
        "gh_families": ["AA2"]
    },
    "manganese_peroxidase": {
        "keywords": ["manganese peroxidase", "MnP"],
        "ec_numbers": ["1.11.1.13"],
        "gh_families": ["AA2"]
    },
    "versatile_peroxidase": {
        "keywords": ["versatile peroxidase", "VP"],
        "ec_numbers": ["1.11.1.16"],
        "gh_families": ["AA2"]
    },
    "glyoxal_oxidase": {
        "keywords": ["glyoxal oxidase", "GLOX"],
        "ec_numbers": ["1.2.3.5"],
        "gh_families": ["AA5"]
    },
    "cellobiose_dehydrogenase": {
        "keywords": ["cellobiose dehydrogenase", "CDH"],
        "ec_numbers": ["1.1.99.18"],
        "gh_families": ["AA3"]
    }
}

# Fungi don't have "gut tissues" - use growth conditions instead
# Override the tissue validation for fungi
SKIP_TISSUE_VALIDATION = True
USE_GROWTH_CONDITIONS = True

PROJECT_NAME = "Fungal_Enzyme_Discovery"
RESULTS_PREFIX = "fungal"

# Special notes for fungi
ORGANISM_NOTES = """
White-rot fungi are the most efficient lignin degraders on Earth.
They produce extensive suites of oxidative enzymes including:
- Lignin peroxidases (LiP)
- Manganese peroxidases (MnP)
- Versatile peroxidases (VP)
- Laccases

Brown-rot fungi use Fenton chemistry for wood degradation.
"""
