"""
Expression Validation Module
Validates gut-specific expression of enzyme candidates
"""
from typing import List, Dict, Optional, Set
import re
import logging

from ..config import GUT_TISSUES, DEVELOPMENTAL_STAGES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExpressionValidator:
    """Validate tissue-specific expression of enzymes"""

    def __init__(self):
        self.gut_tissues = [tissue.lower() for tissue in GUT_TISSUES]
        self.dev_stages = [stage.lower() for stage in DEVELOPMENTAL_STAGES]

    def is_gut_expressed(self, sequence_data: Dict) -> bool:
        """
        Check if sequence is expressed in gut tissue

        Args:
            sequence_data: Sequence dictionary with metadata

        Returns:
            True if gut-expressed
        """
        # Check tissue field
        tissue = sequence_data.get("tissue", "").lower()
        for gut_tissue in self.gut_tissues:
            if gut_tissue in tissue:
                return True

        # Check description and other text fields
        search_text = " ".join([
            sequence_data.get("description", ""),
            sequence_data.get("protein_name", ""),
            str(sequence_data.get("keywords", []))
        ]).lower()

        for gut_tissue in self.gut_tissues:
            if gut_tissue in search_text:
                return True

        return False

    def get_tissue_type(self, sequence_data: Dict) -> Optional[str]:
        """
        Extract specific tissue type

        Args:
            sequence_data: Sequence dictionary

        Returns:
            Tissue type or None
        """
        tissue = sequence_data.get("tissue", "").lower()

        # Check for specific gut regions
        if "midgut" in tissue:
            return "midgut"
        elif "foregut" in tissue:
            return "foregut"
        elif "hindgut" in tissue:
            return "hindgut"
        elif any(g in tissue for g in self.gut_tissues):
            return "gut"

        return None

    def get_developmental_stage(self, sequence_data: Dict) -> Optional[str]:
        """
        Extract developmental stage

        Args:
            sequence_data: Sequence dictionary

        Returns:
            Developmental stage or None
        """
        stage = sequence_data.get("stage", "").lower()

        if "larva" in stage or "larval" in stage:
            return "larval"
        elif "adult" in stage:
            return "adult"
        elif "pupa" in stage or "pupal" in stage:
            return "pupal"

        # Check description
        description = sequence_data.get("description", "").lower()
        for dev_stage in self.dev_stages:
            if dev_stage in description:
                return dev_stage

        return None

    def calculate_expression_score(self, sequence_data: Dict) -> float:
        """
        Calculate expression confidence score

        Args:
            sequence_data: Sequence dictionary

        Returns:
            Expression score (0.0 to 1.0)
        """
        score = 0.0

        # Gut tissue presence
        if self.is_gut_expressed(sequence_data):
            score += 0.4

            # Bonus for specific gut region
            tissue_type = self.get_tissue_type(sequence_data)
            if tissue_type in ["midgut", "foregut", "hindgut"]:
                score += 0.2

        # Developmental stage presence
        if self.get_developmental_stage(sequence_data):
            score += 0.2

        # Larval stage bonus (most relevant for wood digestion)
        stage = self.get_developmental_stage(sequence_data)
        if stage == "larval":
            score += 0.2

        return min(score, 1.0)

    def validate_batch(self, sequences: List[Dict]) -> List[Dict]:
        """
        Validate expression for batch of sequences

        Args:
            sequences: List of sequence dictionaries

        Returns:
            Sequences with expression validation data
        """
        for seq in sequences:
            seq["is_gut_expressed"] = self.is_gut_expressed(seq)
            seq["tissue_type"] = self.get_tissue_type(seq)
            seq["dev_stage_validated"] = self.get_developmental_stage(seq)
            seq["expression_score"] = self.calculate_expression_score(seq)

            # Update overall confidence with expression score
            if "confidence" in seq:
                # Weighted combination
                seq["confidence"] = (
                    seq["confidence"] * 0.7 +
                    seq["expression_score"] * 0.3
                )

        logger.info(f"Validated expression for {len(sequences)} sequences")
        return sequences

    def filter_gut_expressed(
        self,
        sequences: List[Dict],
        require_gut: bool = True,
        require_larval: bool = False
    ) -> List[Dict]:
        """
        Filter sequences by expression criteria

        Args:
            sequences: List of sequences
            require_gut: Require gut expression
            require_larval: Require larval stage

        Returns:
            Filtered sequences
        """
        filtered = sequences

        if require_gut:
            filtered = [s for s in filtered if s.get("is_gut_expressed", False)]

        if require_larval:
            filtered = [s for s in filtered if s.get("dev_stage_validated") == "larval"]

        logger.info(
            f"Filtered {len(sequences)} to {len(filtered)} sequences "
            f"(gut={require_gut}, larval={require_larval})"
        )

        return filtered

    def get_expression_statistics(self, sequences: List[Dict]) -> Dict:
        """
        Generate expression statistics

        Args:
            sequences: List of sequences

        Returns:
            Statistics dictionary
        """
        stats = {
            "total": len(sequences),
            "gut_expressed": 0,
            "tissue_distribution": {},
            "stage_distribution": {},
            "avg_expression_score": 0.0
        }

        expression_scores = []

        for seq in sequences:
            if seq.get("is_gut_expressed"):
                stats["gut_expressed"] += 1

            tissue = seq.get("tissue_type", "unknown")
            stats["tissue_distribution"][tissue] = stats["tissue_distribution"].get(tissue, 0) + 1

            stage = seq.get("dev_stage_validated", "unknown")
            stats["stage_distribution"][stage] = stats["stage_distribution"].get(stage, 0) + 1

            expression_scores.append(seq.get("expression_score", 0.0))

        if expression_scores:
            stats["avg_expression_score"] = sum(expression_scores) / len(expression_scores)

        return stats

    def parse_sra_expression(self, sra_metadata: Dict) -> Dict:
        """
        Parse expression data from SRA metadata

        Args:
            sra_metadata: SRA metadata dictionary

        Returns:
            Expression data dictionary
        """
        expression = {
            "tissue": None,
            "stage": None,
            "is_gut": False,
            "is_transcriptome": False
        }

        # Extract tissue
        tissue = sra_metadata.get("tissue", "").lower()
        for gut_tissue in self.gut_tissues:
            if gut_tissue in tissue:
                expression["tissue"] = gut_tissue
                expression["is_gut"] = True
                break

        # Extract stage
        stage = sra_metadata.get("stage", "").lower()
        for dev_stage in self.dev_stages:
            if dev_stage in stage:
                expression["stage"] = dev_stage
                break

        # Check if transcriptome
        library = sra_metadata.get("library_strategy", "").lower()
        if "rna" in library or "transcriptom" in library:
            expression["is_transcriptome"] = True

        return expression


def create_expression_validator() -> ExpressionValidator:
    """Factory function to create ExpressionValidator instance"""
    return ExpressionValidator()


if __name__ == "__main__":
    # Test validator
    validator = create_expression_validator()

    # Test sequence
    test_seq = {
        "accession": "XP_018093312",
        "description": "cellulase from larval midgut [Agrilus planipennis]",
        "tissue": "midgut",
        "stage": "larval",
        "protein_name": "endo-beta-1,4-glucanase"
    }

    print("Validating expression...")
    validated = validator.validate_batch([test_seq])[0]

    print(f"Gut expressed: {validated['is_gut_expressed']}")
    print(f"Tissue type: {validated['tissue_type']}")
    print(f"Dev stage: {validated['dev_stage_validated']}")
    print(f"Expression score: {validated['expression_score']:.2f}")
