"""
BLAST Filter Module
Performs homology-based filtering of enzyme candidates
"""
from typing import List, Dict, Optional
from Bio.Blast import NCBIWWW, NCBIXML
import logging
import time

from ..config import (
    BLAST_EVALUE_THRESHOLD,
    BLAST_IDENTITY_THRESHOLD,
    BLAST_COVERAGE_THRESHOLD
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BLASTFilter:
    """Filter enzyme sequences using BLAST homology search"""

    def __init__(
        self,
        evalue_threshold: float = BLAST_EVALUE_THRESHOLD,
        identity_threshold: float = BLAST_IDENTITY_THRESHOLD,
        coverage_threshold: float = BLAST_COVERAGE_THRESHOLD
    ):
        self.evalue_threshold = evalue_threshold
        self.identity_threshold = identity_threshold
        self.coverage_threshold = coverage_threshold

    def run_blast_remote(
        self,
        sequence: str,
        database: str = "nr",
        program: str = "blastp",
        entrez_query: Optional[str] = None
    ) -> Optional[str]:
        """
        Run BLAST search against NCBI database

        Args:
            sequence: Query sequence (protein or nucleotide)
            database: BLAST database name
            program: BLAST program (blastp, blastn, etc.)
            entrez_query: Optional Entrez query to filter results

        Returns:
            BLAST results in XML format
        """
        try:
            logger.info(f"Running {program} search against {database}...")

            result_handle = NCBIWWW.qblast(
                program=program,
                database=database,
                sequence=sequence,
                entrez_query=entrez_query,
                expect=self.evalue_threshold * 10,  # Get more results for filtering
                hitlist_size=50
            )

            blast_results = result_handle.read()
            result_handle.close()

            return blast_results

        except Exception as e:
            logger.error(f"Error running BLAST: {e}")
            return None

    def parse_blast_results(self, blast_xml: str) -> List[Dict]:
        """
        Parse BLAST XML results

        Args:
            blast_xml: BLAST results in XML format

        Returns:
            List of hit dictionaries
        """
        from io import StringIO

        hits = []

        try:
            result_handle = StringIO(blast_xml)
            blast_records = NCBIXML.parse(result_handle)

            for blast_record in blast_records:
                for alignment in blast_record.alignments:
                    for hsp in alignment.hsps:
                        # Calculate metrics
                        identity = (hsp.identities / hsp.align_length) * 100
                        coverage = (hsp.align_length / blast_record.query_length) * 100

                        hit = {
                            "subject_id": alignment.hit_id,
                            "subject_def": alignment.hit_def,
                            "evalue": hsp.expect,
                            "bitscore": hsp.bits,
                            "identity": identity,
                            "coverage": coverage,
                            "alignment_length": hsp.align_length,
                            "query_start": hsp.query_start,
                            "query_end": hsp.query_end,
                            "subject_start": hsp.sbjct_start,
                            "subject_end": hsp.sbjct_end,
                            "gaps": hsp.gaps
                        }

                        hits.append(hit)

            result_handle.close()

        except Exception as e:
            logger.error(f"Error parsing BLAST results: {e}")

        return hits

    def filter_hits(self, hits: List[Dict]) -> List[Dict]:
        """
        Filter BLAST hits by thresholds

        Args:
            hits: List of BLAST hit dictionaries

        Returns:
            Filtered list of high-quality hits
        """
        filtered = []

        for hit in hits:
            if (hit["evalue"] <= self.evalue_threshold and
                hit["identity"] >= self.identity_threshold and
                hit["coverage"] >= self.coverage_threshold):
                filtered.append(hit)

        logger.info(f"Filtered {len(hits)} hits to {len(filtered)} high-quality matches")
        return filtered

    def blast_and_filter(
        self,
        sequence: str,
        database: str = "nr",
        program: str = "blastp"
    ) -> List[Dict]:
        """
        Run BLAST and return filtered results

        Args:
            sequence: Query sequence
            database: BLAST database
            program: BLAST program

        Returns:
            List of filtered hit dictionaries
        """
        # Run BLAST
        blast_xml = self.run_blast_remote(sequence, database, program)
        if not blast_xml:
            return []

        # Parse results
        hits = self.parse_blast_results(blast_xml)

        # Filter by thresholds
        filtered_hits = self.filter_hits(hits)

        return filtered_hits

    def batch_blast(
        self,
        sequences: List[Dict],
        delay: float = 3.0
    ) -> Dict[str, List[Dict]]:
        """
        Run BLAST for multiple sequences with rate limiting

        Args:
            sequences: List of sequence dictionaries with 'accession' and 'sequence'
            delay: Delay between requests in seconds

        Returns:
            Dictionary mapping accession to BLAST hits
        """
        results = {}

        for i, seq_data in enumerate(sequences):
            accession = seq_data.get("accession", f"seq_{i}")
            sequence = seq_data.get("sequence", "")

            if not sequence:
                continue

            logger.info(f"BLASTing {accession} ({i+1}/{len(sequences)})...")

            hits = self.blast_and_filter(sequence)
            results[accession] = hits

            # Rate limiting
            if i < len(sequences) - 1:
                time.sleep(delay)

        return results

    def calculate_homology_score(self, hits: List[Dict]) -> float:
        """
        Calculate overall homology score based on BLAST hits

        Args:
            hits: List of BLAST hit dictionaries

        Returns:
            Homology score (0.0 to 1.0)
        """
        if not hits:
            return 0.0

        # Take best hit
        best_hit = max(hits, key=lambda x: x["bitscore"])

        # Normalize scores
        identity_score = min(best_hit["identity"] / 100.0, 1.0)
        coverage_score = min(best_hit["coverage"] / 100.0, 1.0)
        evalue_score = max(0, 1.0 - (best_hit["evalue"] / self.evalue_threshold))

        # Weighted average
        score = (identity_score * 0.4 + coverage_score * 0.3 + evalue_score * 0.3)

        return score

    def annotate_with_blast(self, sequences: List[Dict]) -> List[Dict]:
        """
        Add BLAST-based annotations to sequences

        Args:
            sequences: List of sequence dictionaries

        Returns:
            Annotated sequences with BLAST data
        """
        for seq_data in sequences:
            sequence = seq_data.get("sequence", "")
            if not sequence or len(sequence) < 50:
                seq_data["blast_score"] = 0.0
                seq_data["blast_hits"] = []
                continue

            # Run BLAST
            hits = self.blast_and_filter(sequence)

            # Calculate score
            homology_score = self.calculate_homology_score(hits)

            # Add to sequence data
            seq_data["blast_hits"] = hits
            seq_data["blast_score"] = homology_score

            # Update confidence score with BLAST data
            if "confidence" in seq_data:
                # Weighted combination of annotation and BLAST confidence
                seq_data["confidence"] = (
                    seq_data["confidence"] * 0.6 +
                    homology_score * 0.4
                )

        return sequences


def create_blast_filter() -> BLASTFilter:
    """Factory function to create BLASTFilter instance"""
    return BLASTFilter()


if __name__ == "__main__":
    # Test BLAST filter
    blast_filter = create_blast_filter()

    # Example protein sequence (truncated)
    test_sequence = "MKLVLSLSLVATLLLLAGCKPVQAKVQDVRNLVVGVYSDQFSMVVTDLGKDLNSCFIRLLPEKDVWLTVTLNSVNYGKVSKTTLPGGVPCIPFIQNTRSCLLCTTEHVADATGEIIKCEVPGTYLRLLKKAEHPDNRVLTIGGPIVEDIQKVQFVVSVD"

    print("Running BLAST search...")
    hits = blast_filter.blast_and_filter(test_sequence)

    print(f"\nFound {len(hits)} high-quality hits:")
    for hit in hits[:5]:
        print(f"  {hit['subject_def'][:60]}")
        print(f"    Identity: {hit['identity']:.1f}%, E-value: {hit['evalue']:.2e}")
