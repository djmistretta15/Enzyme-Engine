"""
Configuration for Bark Beetle Enzyme Discovery
Target: Dendroctonus ponderosae (Mountain Pine Beetle) and relatives
"""

# Target Organisms
PRIMARY_ORGANISM = "Dendroctonus ponderosae"
ORGANISM_FAMILY = "Curculionidae"
RELATED_SPECIES = [
    "Dendroctonus ponderosae",
    "Dendroctonus frontalis",  # Southern Pine Beetle
    "Ips typographus",  # European Spruce Bark Beetle
    "Dendroctonus rufipennis",  # Spruce Beetle
    "Scolytus ventralis"  # Fir Engraver
]

SPECIES_COMMON_NAMES = {
    "Dendroctonus ponderosae": "Mountain Pine Beetle",
    "Dendroctonus frontalis": "Southern Pine Beetle",
    "Ips typographus": "European Spruce Bark Beetle",
}

# Bark beetle-specific tissues
GUT_TISSUES = [
    "gut", "midgut", "foregut", "hindgut",
    "digestive", "mycangium", "mycangia"  # Fungal storage organs
]

DEVELOPMENTAL_STAGES = [
    "larva", "larval", "adult", "pupa", "pupal",
    "gallery", "brood"
]

# Bark beetle-specific keywords (they use fungal symbionts!)
BEETLE_KEYWORDS = [
    "mycangium", "mycangial", "fungal symbiont",
    "Grosmannia", "Ophiostoma",  # Common fungal symbionts
    "monoterpene", "terpene", "resin",  # Tree defenses
    "phloem", "cambium"
]

# Additional enzyme types relevant to bark beetles
ADDITIONAL_ENZYMES = {
    "terpene_synthase": {
        "keywords": ["terpene synthase", "monoterpene", "sesquiterpene"],
        "ec_numbers": ["4.2.3.-"]
    },
    "cytochrome_p450": {
        "keywords": ["cytochrome P450", "CYP", "detoxification"],
        "ec_numbers": ["1.14.13.-", "1.14.14.-"]
    }
}

PROJECT_NAME = "Bark_Beetle_Enzyme_Discovery"
RESULTS_PREFIX = "bark_beetle"
