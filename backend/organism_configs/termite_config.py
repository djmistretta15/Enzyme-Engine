"""
Configuration for Termite Enzyme Discovery
Target: Reticulitermes flavipes and related wood-eating termites
"""

# Target Organisms
PRIMARY_ORGANISM = "Reticulitermes flavipes"
ORGANISM_FAMILY = "Rhinotermitidae"
RELATED_SPECIES = [
    "Reticulitermes flavipes",
    "Reticulitermes hesperus",
    "Coptotermes formosanus",
    "Heterotermes aureus",
    "Prorhinotermes simplex"
]

# Common names for reference
SPECIES_COMMON_NAMES = {
    "Reticulitermes flavipes": "Eastern Subterranean Termite",
    "Coptotermes formosanus": "Formosan Termite",
}

# Termite-specific tissue keywords
GUT_TISSUES = [
    "gut", "midgut", "foregut", "hindgut",
    "digestive", "paunch", "colon",
    "alimentary", "intestine"
]

# Developmental stages
DEVELOPMENTAL_STAGES = [
    "worker", "soldier", "reproductive",
    "larva", "larval", "adult", "nymph"
]

# Additional termite-specific keywords
TERMITE_KEYWORDS = [
    "symbiont", "symbiotic", "protozoa", "flagellate",
    "cellulose degradation", "lignocellulose", "wood digestion"
]

# Search query templates
QUERY_TEMPLATES = {
    "gut_metagenome": '"{organism}"[Organism] AND (gut OR hindgut) AND (metagenome OR microbiome)',
    "symbiont_enzymes": '"{organism}"[Organism] AND (symbiont OR protozoa) AND ({enzyme_keywords})',
    "worker_specific": '"{organism}"[Organism] AND worker AND ({tissues}) AND (transcriptome OR RNA-Seq)',
}

# Output naming
PROJECT_NAME = "Termite_Enzyme_Discovery"
RESULTS_PREFIX = "termite"
