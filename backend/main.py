#!/usr/bin/env python3
"""
EAB Enzyme Discovery System - Main CLI
Comprehensive pipeline for discovering wood-digesting enzymes in Emerald Ash Borer
"""
import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from modules.search_ncbi import create_searcher
from modules.retrieve_sequences import create_retriever
from modules.annotation import create_annotator
from modules.blast_filter import create_blast_filter
from modules.expression_validate import create_expression_validator
from modules.storage import create_database_manager
from modules.matrix_builder import create_matrix_builder
from modules.visualization import create_visualizer
from config import PRIMARY_ORGANISM, RESULTS_DIR

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EABEnzymeDiscovery:
    """Main pipeline controller"""

    def __init__(
        self,
        use_cache: bool = True,
        use_blast: bool = False,
        min_confidence: float = 0.5
    ):
        self.searcher = create_searcher()
        self.retriever = create_retriever(use_cache=use_cache)
        self.annotator = create_annotator()
        self.blast_filter = create_blast_filter() if use_blast else None
        self.validator = create_expression_validator()
        self.db = create_database_manager()
        self.matrix_builder = create_matrix_builder()
        self.visualizer = create_visualizer()
        self.min_confidence = min_confidence

    def run_pipeline(
        self,
        organism: str = PRIMARY_ORGANISM,
        enzyme_type: Optional[str] = None,
        database: str = "protein",
        max_results: int = 100,
        skip_blast: bool = True
    ):
        """
        Run complete enzyme discovery pipeline

        Args:
            organism: Target organism name
            enzyme_type: Specific enzyme type or None for all
            database: NCBI database to search
            max_results: Maximum number of sequences to process
            skip_blast: Skip BLAST analysis (faster)
        """
        logger.info("=" * 80)
        logger.info("EAB ENZYME DISCOVERY PIPELINE")
        logger.info("=" * 80)

        # Step 1: Search NCBI
        logger.info("\n[STEP 1] Searching NCBI databases...")
        search_results = self.searcher.search_all_organisms(
            database=database,
            enzyme_type=enzyme_type,
            include_related=True
        )

        # Collect all IDs
        all_ids = []
        for result in search_results:
            all_ids.extend(result["id_list"][:max_results])

        logger.info(f"Found {len(all_ids)} sequences to process")

        if not all_ids:
            logger.warning("No sequences found. Exiting.")
            return

        # Step 2: Retrieve sequences
        logger.info("\n[STEP 2] Retrieving sequences from NCBI...")
        sequences = self.retriever.retrieve_batch(
            database=database,
            id_list=all_ids[:max_results]
        )

        logger.info(f"Retrieved {len(sequences)} sequences")

        if not sequences:
            logger.warning("No sequences retrieved. Exiting.")
            return

        # Step 3: Annotate enzymes
        logger.info("\n[STEP 3] Annotating enzyme types...")
        annotated_sequences = self.annotator.annotate_batch(sequences)

        # Step 4: Validate expression
        logger.info("\n[STEP 4] Validating tissue expression...")
        validated_sequences = self.validator.validate_batch(annotated_sequences)

        # Step 5: BLAST filtering (optional)
        if not skip_blast and self.blast_filter:
            logger.info("\n[STEP 5] Running BLAST homology analysis...")
            logger.info("WARNING: This step is very slow. Consider skipping with --skip-blast")
            validated_sequences = self.blast_filter.annotate_with_blast(validated_sequences)

        # Step 6: Filter by confidence
        logger.info(f"\n[STEP 6] Filtering by confidence (min: {self.min_confidence})...")
        high_confidence = self.annotator.filter_by_confidence(
            validated_sequences,
            min_confidence=self.min_confidence
        )

        # Step 7: Store in database
        logger.info("\n[STEP 7] Storing results in database...")
        self.db.insert_batch(high_confidence)

        # Step 8: Build digestive matrix
        logger.info("\n[STEP 8] Building digestive enzyme matrix...")
        matrix = self.matrix_builder.build_matrix(
            high_confidence,
            min_confidence=self.min_confidence
        )

        logger.info(f"Matrix contains {len(matrix)} enzymes")

        # Step 9: Generate outputs
        logger.info("\n[STEP 9] Generating outputs...")

        output_dir = Path(RESULTS_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Export matrix
        matrix_file = output_dir / "digestive_matrix.csv"
        self.matrix_builder.export_matrix(matrix, matrix_file, format="csv")

        matrix_json = output_dir / "digestive_matrix.json"
        self.matrix_builder.export_matrix(matrix, matrix_json, format="json")

        # Generate report
        report_file = output_dir / "discovery_report.txt"
        self.matrix_builder.generate_report(matrix, report_file)

        # Generate visualizations
        logger.info("\n[STEP 10] Creating visualizations...")
        self.visualizer.generate_all_plots(matrix)

        # Final summary
        logger.info("\n" + "=" * 80)
        logger.info("PIPELINE COMPLETE!")
        logger.info("=" * 80)

        summary = self.matrix_builder.generate_summary(matrix)
        logger.info(f"\nTotal enzymes identified: {summary['total_enzymes']}")
        logger.info(f"High confidence (≥0.8): {summary['high_confidence_count']}")
        logger.info(f"Gut-expressed: {summary['gut_expressed_count']}")
        logger.info(f"Average confidence: {summary['avg_confidence']:.2f}")

        logger.info(f"\nResults saved to: {output_dir}")
        logger.info(f"  - Digestive matrix: {matrix_file}")
        logger.info(f"  - Detailed report: {report_file}")
        logger.info(f"  - Visualizations: {output_dir}")

        return matrix


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="EAB Enzyme Discovery System - Mine NCBI for wood-digesting enzymes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for all enzymes in Agrilus planipennis
  python main.py --organism "Agrilus planipennis" --max-results 200

  # Search for specific enzyme type
  python main.py --enzyme cellulase --database protein --max-results 100

  # Include BLAST analysis (slow!)
  python main.py --organism "Agrilus planipennis" --no-skip-blast

  # Custom confidence threshold
  python main.py --min-confidence 0.7 --max-results 150
        """
    )

    parser.add_argument(
        "--organism",
        default=PRIMARY_ORGANISM,
        help="Target organism name (default: Agrilus planipennis)"
    )

    parser.add_argument(
        "--enzyme",
        choices=["cellulase", "laccase", "peroxidase", "oxidase", "xylanase", "beta-glucosidase", "mannanase"],
        help="Specific enzyme type to search for (default: all)"
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

    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="Only show database statistics, don't run pipeline"
    )

    args = parser.parse_args()

    # Show database stats if requested
    if args.stats_only:
        db = create_database_manager()
        stats = db.get_statistics()

        print("\n" + "=" * 60)
        print("DATABASE STATISTICS")
        print("=" * 60)
        print(f"Total sequences: {stats['total_sequences']}")
        print(f"Total organisms: {stats['total_organisms']}")
        print(f"Average confidence: {stats['avg_confidence']:.2f}")

        print("\nEnzyme types:")
        for enzyme, count in sorted(stats['enzyme_types'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {enzyme}: {count}")

        print("\nTop organisms:")
        for org, count in list(stats['top_organisms'].items())[:10]:
            print(f"  {org}: {count}")

        return

    # Run pipeline
    try:
        pipeline = EABEnzymeDiscovery(
            use_cache=not args.no_cache,
            use_blast=args.no_skip_blast,
            min_confidence=args.min_confidence
        )

        pipeline.run_pipeline(
            organism=args.organism,
            enzyme_type=args.enzyme,
            database=args.database,
            max_results=args.max_results,
            skip_blast=not args.no_skip_blast
        )

    except KeyboardInterrupt:
        logger.info("\nPipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
