"""
Digestive Matrix Builder Module
Builds ranked enzyme matrix for wood digestion analysis
"""
from typing import List, Dict, Optional
import pandas as pd
import json
import logging
from collections import defaultdict

from ..config import ENZYME_KEYWORDS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DigestiveMatrixBuilder:
    """Build comprehensive digestive enzyme matrix"""

    def __init__(self):
        self.enzyme_types = list(ENZYME_KEYWORDS.keys())

    def build_matrix(
        self,
        sequences: List[Dict],
        min_confidence: float = 0.5
    ) -> pd.DataFrame:
        """
        Build digestive enzyme matrix from sequences

        Args:
            sequences: List of annotated sequence dictionaries
            min_confidence: Minimum confidence threshold

        Returns:
            DataFrame with enzyme matrix
        """
        # Filter by confidence
        filtered = [s for s in sequences if s.get("confidence", 0) >= min_confidence]

        logger.info(f"Building matrix from {len(filtered)} high-confidence sequences")

        matrix_data = []

        for seq in filtered:
            row = {
                "Enzyme": seq.get("enzyme_type", "unknown"),
                "EC": seq.get("ec_number_annotated", ""),
                "GH/AA Family": seq.get("gh_family", ""),
                "Gene ID": seq.get("accession", ""),
                "Gene Name": seq.get("gene_name", ""),
                "Protein": seq.get("protein_name", ""),
                "Organism": seq.get("organism", ""),
                "Tissue": seq.get("tissue_type", seq.get("tissue", "")),
                "Stage": seq.get("dev_stage_validated", seq.get("stage", "")),
                "Length": seq.get("length", 0),
                "Confidence": round(seq.get("confidence", 0.0), 3),
                "Expression": round(seq.get("expression_score", 0.0), 3),
                "BLAST Score": round(seq.get("blast_score", 0.0), 3),
                "Function": self._infer_function(seq)
            }

            matrix_data.append(row)

        # Create DataFrame
        df = pd.DataFrame(matrix_data)

        # Sort by confidence
        df = df.sort_values("Confidence", ascending=False)

        return df

    def _infer_function(self, sequence: Dict) -> str:
        """Infer enzyme function from metadata"""
        enzyme_type = sequence.get("enzyme_type", "")
        ec = sequence.get("ec_number_annotated", "")

        function_map = {
            "cellulase": "Cellulose hydrolysis",
            "laccase": "Lignin oxidation",
            "peroxidase": "Lignin degradation",
            "oxidase": "Oxidative degradation",
            "xylanase": "Hemicellulose breakdown",
            "beta-glucosidase": "Cellulose hydrolysis",
            "mannanase": "Hemicellulose breakdown"
        }

        return function_map.get(enzyme_type, "Wood polymer degradation")

    def generate_summary(self, matrix_df: pd.DataFrame) -> Dict:
        """
        Generate summary statistics from matrix

        Args:
            matrix_df: Enzyme matrix DataFrame

        Returns:
            Summary statistics dictionary
        """
        summary = {
            "total_enzymes": len(matrix_df),
            "unique_enzyme_types": matrix_df["Enzyme"].nunique(),
            "enzyme_distribution": matrix_df["Enzyme"].value_counts().to_dict(),
            "organism_distribution": matrix_df["Organism"].value_counts().to_dict(),
            "tissue_distribution": matrix_df["Tissue"].value_counts().to_dict(),
            "stage_distribution": matrix_df["Stage"].value_counts().to_dict(),
            "gh_family_distribution": matrix_df[matrix_df["GH/AA Family"] != ""]["GH/AA Family"].value_counts().to_dict(),
            "avg_confidence": matrix_df["Confidence"].mean(),
            "high_confidence_count": len(matrix_df[matrix_df["Confidence"] >= 0.8]),
            "gut_expressed_count": len(matrix_df[matrix_df["Tissue"].str.contains("gut", na=False)]),
            "larval_stage_count": len(matrix_df[matrix_df["Stage"].str.contains("larval", na=False)])
        }

        return summary

    def identify_enzyme_clusters(self, matrix_df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        Identify enzyme clusters by function

        Args:
            matrix_df: Enzyme matrix DataFrame

        Returns:
            Dictionary of enzyme clusters
        """
        clusters = {
            "Cellulose Degradation": [],
            "Lignin Degradation": [],
            "Hemicellulose Degradation": [],
            "Oxidative Enzymes": [],
            "Other": []
        }

        for _, row in matrix_df.iterrows():
            enzyme = row["Enzyme"]
            gene_id = row["Gene ID"]

            if enzyme in ["cellulase", "beta-glucosidase"]:
                clusters["Cellulose Degradation"].append(gene_id)
            elif enzyme in ["laccase", "peroxidase"]:
                clusters["Lignin Degradation"].append(gene_id)
            elif enzyme in ["xylanase", "mannanase"]:
                clusters["Hemicellulose Degradation"].append(gene_id)
            elif enzyme in ["oxidase"]:
                clusters["Oxidative Enzymes"].append(gene_id)
            else:
                clusters["Other"].append(gene_id)

        return clusters

    def rank_by_criteria(
        self,
        matrix_df: pd.DataFrame,
        criteria: str = "overall"
    ) -> pd.DataFrame:
        """
        Rank enzymes by specific criteria

        Args:
            matrix_df: Enzyme matrix DataFrame
            criteria: Ranking criteria (overall, confidence, expression, blast)

        Returns:
            Ranked DataFrame
        """
        if criteria == "overall":
            # Composite score
            matrix_df["Rank Score"] = (
                matrix_df["Confidence"] * 0.5 +
                matrix_df["Expression"] * 0.3 +
                matrix_df["BLAST Score"] * 0.2
            )
            return matrix_df.sort_values("Rank Score", ascending=False)

        elif criteria == "confidence":
            return matrix_df.sort_values("Confidence", ascending=False)

        elif criteria == "expression":
            return matrix_df.sort_values("Expression", ascending=False)

        elif criteria == "blast":
            return matrix_df.sort_values("BLAST Score", ascending=False)

        return matrix_df

    def export_matrix(
        self,
        matrix_df: pd.DataFrame,
        output_file: str,
        format: str = "csv"
    ):
        """
        Export matrix to file

        Args:
            matrix_df: Enzyme matrix DataFrame
            output_file: Output file path
            format: Output format (csv, json, excel)
        """
        if format == "csv":
            matrix_df.to_csv(output_file, index=False)
        elif format == "json":
            matrix_df.to_json(output_file, orient="records", indent=2)
        elif format == "excel":
            matrix_df.to_excel(output_file, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"Exported matrix to {output_file}")

    def generate_report(
        self,
        matrix_df: pd.DataFrame,
        output_file: str
    ):
        """
        Generate comprehensive text report

        Args:
            matrix_df: Enzyme matrix DataFrame
            output_file: Output text file path
        """
        summary = self.generate_summary(matrix_df)
        clusters = self.identify_enzyme_clusters(matrix_df)

        with open(output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("EMERALD ASH BORER DIGESTIVE ENZYME DISCOVERY REPORT\n")
            f.write("=" * 80 + "\n\n")

            f.write("SUMMARY STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Enzymes Identified: {summary['total_enzymes']}\n")
            f.write(f"Unique Enzyme Types: {summary['unique_enzyme_types']}\n")
            f.write(f"Average Confidence: {summary['avg_confidence']:.2f}\n")
            f.write(f"High Confidence (≥0.8): {summary['high_confidence_count']}\n")
            f.write(f"Gut-Expressed: {summary['gut_expressed_count']}\n")
            f.write(f"Larval Stage: {summary['larval_stage_count']}\n\n")

            f.write("ENZYME TYPE DISTRIBUTION\n")
            f.write("-" * 80 + "\n")
            for enzyme, count in summary['enzyme_distribution'].items():
                f.write(f"  {enzyme}: {count}\n")
            f.write("\n")

            f.write("ORGANISM DISTRIBUTION\n")
            f.write("-" * 80 + "\n")
            for org, count in summary['organism_distribution'].items():
                f.write(f"  {org}: {count}\n")
            f.write("\n")

            f.write("GH/AA FAMILY DISTRIBUTION\n")
            f.write("-" * 80 + "\n")
            for family, count in summary.get('gh_family_distribution', {}).items():
                f.write(f"  {family}: {count}\n")
            f.write("\n")

            f.write("FUNCTIONAL ENZYME CLUSTERS\n")
            f.write("-" * 80 + "\n")
            for cluster_name, gene_ids in clusters.items():
                f.write(f"\n{cluster_name} ({len(gene_ids)} enzymes):\n")
                for gene_id in gene_ids[:10]:  # Show top 10
                    f.write(f"  - {gene_id}\n")
                if len(gene_ids) > 10:
                    f.write(f"  ... and {len(gene_ids) - 10} more\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("TOP 20 CANDIDATE ENZYMES (by confidence)\n")
            f.write("=" * 80 + "\n\n")

            top_enzymes = matrix_df.head(20)
            for idx, row in top_enzymes.iterrows():
                f.write(f"\n{row['Gene ID']} - {row['Enzyme']}\n")
                f.write(f"  Protein: {row['Protein']}\n")
                f.write(f"  Organism: {row['Organism']}\n")
                f.write(f"  Tissue: {row['Tissue']} | Stage: {row['Stage']}\n")
                f.write(f"  EC: {row['EC']} | GH Family: {row['GH/AA Family']}\n")
                f.write(f"  Confidence: {row['Confidence']:.3f} | Expression: {row['Expression']:.3f}\n")
                f.write(f"  Function: {row['Function']}\n")

        logger.info(f"Generated report at {output_file}")


def create_matrix_builder() -> DigestiveMatrixBuilder:
    """Factory function to create DigestiveMatrixBuilder instance"""
    return DigestiveMatrixBuilder()


if __name__ == "__main__":
    # Test matrix builder
    builder = create_matrix_builder()

    # Sample data
    sample_sequences = [
        {
            "accession": "XP_018093312",
            "enzyme_type": "cellulase",
            "ec_number_annotated": "3.2.1.4",
            "gh_family": "GH5",
            "gene_name": "cel5",
            "protein_name": "endoglucanase",
            "organism": "Agrilus planipennis",
            "tissue": "midgut",
            "stage": "larval",
            "length": 450,
            "confidence": 0.92,
            "expression_score": 0.85,
            "blast_score": 0.88
        }
    ]

    matrix = builder.build_matrix(sample_sequences)
    print(matrix)

    summary = builder.generate_summary(matrix)
    print("\nSummary:", json.dumps(summary, indent=2))
