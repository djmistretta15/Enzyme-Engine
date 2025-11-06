"""
Annotation Module
Classifies and annotates enzyme sequences with functional information
"""
import re
from typing import Dict, List, Optional, Set, Tuple
from collections import Counter
import logging

from ..config import ENZYME_KEYWORDS, GUT_TISSUES, CONFIDENCE_WEIGHTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnzymeAnnotator:
    """Annotate and classify enzyme sequences"""

    def __init__(self):
        self.enzyme_patterns = self._compile_patterns()
        self.gh_pattern = re.compile(r'\b(GH\d+|AA\d+|CE\d+|PL\d+)\b', re.IGNORECASE)
        self.ec_pattern = re.compile(r'\b(\d+\.\d+\.\d+\.\d+)\b')

    def _compile_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Compile regex patterns for enzyme keywords"""
        patterns = {}
        for enzyme_type, data in ENZYME_KEYWORDS.items():
            enzyme_patterns = []
            for keyword in data["keywords"]:
                # Create case-insensitive pattern with word boundaries
                pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
                enzyme_patterns.append(pattern)
            patterns[enzyme_type] = enzyme_patterns
        return patterns

    def classify_enzyme(self, sequence_data: Dict) -> Dict:
        """
        Classify an enzyme based on its metadata

        Args:
            sequence_data: Parsed sequence dictionary

        Returns:
            Dictionary with classification results
        """
        classification = {
            "enzyme_types": [],
            "enzyme_scores": {},
            "gh_families": [],
            "ec_numbers": [],
            "confidence": 0.0,
            "is_gut_expressed": False,
            "keywords_found": []
        }

        # Combine all text fields for searching
        search_text = " ".join([
            sequence_data.get("description", ""),
            sequence_data.get("protein_name", ""),
            sequence_data.get("gene_name", ""),
            " ".join(sequence_data.get("keywords", [])),
            str(sequence_data.get("features", []))
        ])

        # Classify enzyme type by keyword matching
        for enzyme_type, patterns in self.enzyme_patterns.items():
            matches = 0
            for pattern in patterns:
                if pattern.search(search_text):
                    matches += 1

            if matches > 0:
                classification["enzyme_types"].append(enzyme_type)
                classification["enzyme_scores"][enzyme_type] = matches / len(patterns)

        # Extract GH/AA families
        gh_matches = self.gh_pattern.findall(search_text)
        classification["gh_families"] = list(set([gh.upper() for gh in gh_matches]))

        # Extract EC numbers
        if sequence_data.get("ec_number"):
            classification["ec_numbers"].append(sequence_data["ec_number"])

        ec_matches = self.ec_pattern.findall(search_text)
        classification["ec_numbers"].extend(ec_matches)
        classification["ec_numbers"] = list(set(classification["ec_numbers"]))

        # Check gut tissue expression
        tissue = sequence_data.get("tissue", "").lower()
        for gut_tissue in GUT_TISSUES:
            if gut_tissue in tissue or gut_tissue in search_text.lower():
                classification["is_gut_expressed"] = True
                break

        # Extract keywords found
        all_keywords = []
        for enzyme_data in ENZYME_KEYWORDS.values():
            all_keywords.extend(enzyme_data["keywords"])

        for keyword in set(all_keywords):
            if re.search(r'\b' + re.escape(keyword) + r'\b', search_text, re.IGNORECASE):
                classification["keywords_found"].append(keyword)

        # Calculate confidence score
        classification["confidence"] = self.calculate_confidence(
            sequence_data, classification
        )

        return classification

    def calculate_confidence(
        self,
        sequence_data: Dict,
        classification: Dict
    ) -> float:
        """
        Calculate confidence score for enzyme classification

        Args:
            sequence_data: Parsed sequence data
            classification: Classification results

        Returns:
            Confidence score (0.0 to 1.0)
        """
        score = 0.0

        # Keyword match score
        if classification["keywords_found"]:
            keyword_score = min(len(classification["keywords_found"]) / 5.0, 1.0)
            score += CONFIDENCE_WEIGHTS["keyword_match"] * keyword_score

        # EC number match
        if classification["ec_numbers"]:
            score += CONFIDENCE_WEIGHTS["ec_match"]

        # GH family match
        if classification["gh_families"]:
            score += CONFIDENCE_WEIGHTS["gh_family_match"]

        # Gut tissue expression
        if classification["is_gut_expressed"]:
            score += CONFIDENCE_WEIGHTS["gut_tissue"]

        # Has enzyme type classification
        if classification["enzyme_types"]:
            # Average enzyme scores
            avg_enzyme_score = sum(classification["enzyme_scores"].values()) / len(classification["enzyme_scores"])
            score += 0.2 * avg_enzyme_score

        # Normalize to 0.0-1.0 range
        return min(score, 1.0)

    def annotate_batch(self, sequences: List[Dict]) -> List[Dict]:
        """
        Annotate a batch of sequences

        Args:
            sequences: List of parsed sequence dictionaries

        Returns:
            List of sequences with added annotation data
        """
        annotated = []

        for seq in sequences:
            classification = self.classify_enzyme(seq)

            # Add classification to sequence data
            seq["annotation"] = classification
            seq["enzyme_type"] = classification["enzyme_types"][0] if classification["enzyme_types"] else "unknown"
            seq["confidence"] = classification["confidence"]
            seq["gh_family"] = classification["gh_families"][0] if classification["gh_families"] else None
            seq["ec_number_annotated"] = classification["ec_numbers"][0] if classification["ec_numbers"] else seq.get("ec_number")

            annotated.append(seq)

        logger.info(f"Annotated {len(annotated)} sequences")
        return annotated

    def filter_by_confidence(
        self,
        sequences: List[Dict],
        min_confidence: float = 0.5
    ) -> List[Dict]:
        """
        Filter sequences by confidence threshold

        Args:
            sequences: List of annotated sequences
            min_confidence: Minimum confidence score

        Returns:
            Filtered list of sequences
        """
        filtered = [seq for seq in sequences if seq.get("confidence", 0) >= min_confidence]
        logger.info(f"Filtered {len(sequences)} sequences to {len(filtered)} (min confidence: {min_confidence})")
        return filtered

    def get_enzyme_statistics(self, sequences: List[Dict]) -> Dict:
        """
        Generate statistics about enzyme types in the dataset

        Args:
            sequences: List of annotated sequences

        Returns:
            Dictionary with statistics
        """
        stats = {
            "total_sequences": len(sequences),
            "enzyme_type_counts": Counter(),
            "gh_family_counts": Counter(),
            "ec_number_counts": Counter(),
            "organism_counts": Counter(),
            "tissue_counts": Counter(),
            "avg_confidence": 0.0,
            "high_confidence_count": 0
        }

        confidences = []

        for seq in sequences:
            # Count enzyme types
            enzyme_type = seq.get("enzyme_type", "unknown")
            stats["enzyme_type_counts"][enzyme_type] += 1

            # Count GH families
            gh_family = seq.get("gh_family")
            if gh_family:
                stats["gh_family_counts"][gh_family] += 1

            # Count EC numbers
            ec = seq.get("ec_number_annotated")
            if ec:
                stats["ec_number_counts"][ec] += 1

            # Count organisms
            organism = seq.get("organism", "unknown")
            stats["organism_counts"][organism] += 1

            # Count tissues
            tissue = seq.get("tissue", "unknown")
            stats["tissue_counts"][tissue] += 1

            # Confidence stats
            confidence = seq.get("confidence", 0)
            confidences.append(confidence)
            if confidence >= 0.8:
                stats["high_confidence_count"] += 1

        # Calculate average confidence
        if confidences:
            stats["avg_confidence"] = sum(confidences) / len(confidences)

        return stats

    def rank_sequences(
        self,
        sequences: List[Dict],
        criteria: str = "confidence"
    ) -> List[Dict]:
        """
        Rank sequences by specified criteria

        Args:
            sequences: List of annotated sequences
            criteria: Ranking criteria ('confidence', 'length', 'enzyme_score')

        Returns:
            Sorted list of sequences
        """
        if criteria == "confidence":
            return sorted(sequences, key=lambda x: x.get("confidence", 0), reverse=True)
        elif criteria == "length":
            return sorted(sequences, key=lambda x: x.get("length", 0), reverse=True)
        elif criteria == "enzyme_score":
            return sorted(
                sequences,
                key=lambda x: max(x.get("annotation", {}).get("enzyme_scores", {}).values(), default=0),
                reverse=True
            )
        else:
            return sequences


def create_annotator() -> EnzymeAnnotator:
    """Factory function to create EnzymeAnnotator instance"""
    return EnzymeAnnotator()


if __name__ == "__main__":
    # Test the annotator
    annotator = create_annotator()

    # Test sequence
    test_seq = {
        "accession": "XP_018093312",
        "description": "endo-beta-1,4-glucanase [Agrilus planipennis]",
        "protein_name": "endo-beta-1,4-glucanase",
        "gene_name": "cellulase",
        "organism": "Agrilus planipennis",
        "tissue": "midgut",
        "ec_number": "3.2.1.4",
        "keywords": ["cellulase", "glycoside hydrolase", "GH5"],
        "length": 450
    }

    classification = annotator.classify_enzyme(test_seq)
    print("Classification:")
    print(f"  Enzyme types: {classification['enzyme_types']}")
    print(f"  GH families: {classification['gh_families']}")
    print(f"  EC numbers: {classification['ec_numbers']}")
    print(f"  Gut expressed: {classification['is_gut_expressed']}")
    print(f"  Confidence: {classification['confidence']:.2f}")
