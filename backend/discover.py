#!/usr/bin/env python3
"""
Universal Enzyme Discovery Launcher
Easily switch between different organism targets
"""
import argparse
import sys
from pathlib import Path

# Organism profiles
ORGANISM_PROFILES = {
    "eab": {
        "name": "Emerald Ash Borer",
        "organism": "Agrilus planipennis",
        "description": "Wood-boring beetle devastating ash trees",
        "config": "organism_configs.eab_config"
    },
    "termite": {
        "name": "Termites",
        "organism": "Reticulitermes flavipes",
        "description": "Subterranean termites with symbiotic gut flora",
        "config": "organism_configs.termite_config"
    },
    "bark-beetle": {
        "name": "Bark Beetles",
        "organism": "Dendroctonus ponderosae",
        "description": "Mountain Pine Beetle with fungal symbionts",
        "config": "organism_configs.bark_beetle_config"
    },
    "fungus": {
        "name": "Wood-Rot Fungi",
        "organism": "Phanerochaete chrysosporium",
        "description": "White-rot fungus - nature's lignin destroyer",
        "config": "organism_configs.fungal_config"
    },
    "custom": {
        "name": "Custom Organism",
        "organism": None,  # User provides
        "description": "Any organism in NCBI databases",
        "config": None
    }
}


def print_available_profiles():
    """Display available organism profiles"""
    print("\n" + "=" * 70)
    print("AVAILABLE ORGANISM PROFILES")
    print("=" * 70 + "\n")

    for key, profile in ORGANISM_PROFILES.items():
        if key != "custom":
            print(f"  {key:15} - {profile['name']}")
            print(f"  {'':15}   {profile['organism']}")
            print(f"  {'':15}   {profile['description']}")
            print()

    print(f"  {'custom':15} - Any organism (specify with --organism)")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Universal Enzyme Discovery System - Target any organism",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Discover enzymes in Emerald Ash Borer
  python discover.py eab --max-results 200

  # Discover termite gut enzymes
  python discover.py termite --enzyme cellulase --max-results 150

  # Discover bark beetle detox enzymes
  python discover.py bark-beetle --max-results 100

  # Discover fungal ligninases
  python discover.py fungus --enzyme laccase --max-results 200

  # Custom organism
  python discover.py custom --organism "Teredo navalis" --max-results 100

  # List all available profiles
  python discover.py --list
        """
    )

    parser.add_argument(
        "profile",
        nargs="?",
        choices=list(ORGANISM_PROFILES.keys()),
        help="Organism profile to use"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available organism profiles"
    )

    parser.add_argument(
        "--organism",
        help="Custom organism name (for 'custom' profile)"
    )

    parser.add_argument(
        "--enzyme",
        choices=["cellulase", "laccase", "peroxidase", "oxidase", "xylanase", "beta-glucosidase", "mannanase"],
        help="Specific enzyme type to search for"
    )

    parser.add_argument(
        "--database",
        choices=["protein", "nucleotide", "sra"],
        default="protein",
        help="NCBI database to search (default: protein)"
    )

    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Maximum number of sequences to process (default: 100)"
    )

    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.5,
        help="Minimum confidence threshold (default: 0.5)"
    )

    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable sequence caching"
    )

    parser.add_argument(
        "--no-skip-blast",
        action="store_true",
        help="Enable BLAST analysis (WARNING: very slow!)"
    )

    args = parser.parse_args()

    # List profiles if requested
    if args.list:
        print_available_profiles()
        return

    # Check if profile was provided
    if not args.profile:
        print("Error: Please specify an organism profile")
        print_available_profiles()
        sys.exit(1)

    # Get profile
    profile = ORGANISM_PROFILES[args.profile]

    # Determine organism name
    if args.profile == "custom":
        if not args.organism:
            print("Error: --organism required for custom profile")
            print("Example: python discover.py custom --organism 'Teredo navalis'")
            sys.exit(1)
        organism_name = args.organism
    else:
        organism_name = profile["organism"]

    # Display banner
    print("\n" + "=" * 70)
    print(f"ENZYME DISCOVERY: {profile['name'].upper()}")
    print("=" * 70)
    print(f"Target: {organism_name}")
    print(f"Database: {args.database}")
    print(f"Max Results: {args.max_results}")
    if args.enzyme:
        print(f"Enzyme Filter: {args.enzyme}")
    print("=" * 70 + "\n")

    # Import and run main pipeline
    from main import EABEnzymeDiscovery

    try:
        pipeline = EABEnzymeDiscovery(
            use_cache=not args.no_cache,
            use_blast=args.no_skip_blast,
            min_confidence=args.min_confidence
        )

        pipeline.run_pipeline(
            organism=organism_name,
            enzyme_type=args.enzyme,
            database=args.database,
            max_results=args.max_results,
            skip_blast=not args.no_skip_blast
        )

        print("\n" + "=" * 70)
        print("DISCOVERY COMPLETE!")
        print("=" * 70)
        print(f"\nResults for {organism_name} saved to backend/data/results/")
        print("\nNext steps:")
        print("  1. Review digestive_matrix.csv for top enzyme candidates")
        print("  2. Read discovery_report.txt for detailed analysis")
        print("  3. Check visualizations in backend/data/results/")
        print("  4. Launch frontend (cd ../frontend && npm run dev)")

    except KeyboardInterrupt:
        print("\n\nDiscovery interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
