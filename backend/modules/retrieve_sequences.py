"""
Sequence Retrieval Module
Handles downloading and parsing sequences from NCBI
"""
import time
from typing import List, Dict, Optional, Tuple
from Bio import Entrez, SeqIO
from Bio.SeqRecord import SeqRecord
import logging
import json
from pathlib import Path

from ..config import (
    NCBI_EMAIL, NCBI_API_KEY, NCBI_TOOL, NCBI_RATE_LIMIT,
    CACHE_DIR
)

Entrez.email = NCBI_EMAIL
Entrez.tool = NCBI_TOOL
if NCBI_API_KEY:
    Entrez.api_key = NCBI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SequenceRetriever:
    """Retrieve and parse sequences from NCBI"""

    def __init__(self, rate_limit: float = NCBI_RATE_LIMIT, use_cache: bool = True):
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.use_cache = use_cache
        self.cache_dir = Path(CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _rate_limit_wait(self):
        """Ensure compliance with NCBI rate limits"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    def _get_cache_path(self, database: str, acc_id: str) -> Path:
        """Get cache file path for an accession"""
        return self.cache_dir / f"{database}_{acc_id}.json"

    def _load_from_cache(self, database: str, acc_id: str) -> Optional[Dict]:
        """Load sequence data from cache"""
        if not self.use_cache:
            return None

        cache_path = self._get_cache_path(database, acc_id)
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error loading cache for {acc_id}: {e}")
        return None

    def _save_to_cache(self, database: str, acc_id: str, data: Dict):
        """Save sequence data to cache"""
        if not self.use_cache:
            return

        cache_path = self._get_cache_path(database, acc_id)
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"Error saving cache for {acc_id}: {e}")

    def fetch_sequence(
        self,
        database: str,
        acc_id: str,
        rettype: str = "gb",
        retmode: str = "text"
    ) -> Optional[str]:
        """
        Fetch a single sequence from NCBI

        Args:
            database: Database name (protein, nucleotide, etc.)
            acc_id: Accession ID
            rettype: Return type (gb, fasta, etc.)
            retmode: Return mode (text, xml)

        Returns:
            Sequence data as string or None if error
        """
        self._rate_limit_wait()

        try:
            logger.debug(f"Fetching {acc_id} from {database}")

            handle = Entrez.efetch(
                db=database,
                id=acc_id,
                rettype=rettype,
                retmode=retmode
            )
            data = handle.read()
            handle.close()

            return data

        except Exception as e:
            logger.error(f"Error fetching {acc_id}: {e}")
            return None

    def parse_genbank_record(self, record: SeqRecord) -> Dict:
        """
        Parse a GenBank SeqRecord into structured data

        Args:
            record: BioPython SeqRecord object

        Returns:
            Dictionary with parsed sequence information
        """
        # Extract basic information
        data = {
            "accession": record.id,
            "description": record.description,
            "sequence": str(record.seq),
            "length": len(record.seq),
            "organism": "",
            "taxonomy": [],
            "gene_name": "",
            "protein_name": "",
            "ec_number": None,
            "tissue": None,
            "stage": None,
            "keywords": [],
            "features": []
        }

        # Extract from annotations
        annotations = record.annotations
        data["organism"] = annotations.get("organism", "")
        data["taxonomy"] = annotations.get("taxonomy", [])
        data["keywords"] = annotations.get("keywords", [])

        # Extract from features
        for feature in record.features:
            feature_data = {
                "type": feature.type,
                "location": str(feature.location),
                "qualifiers": {}
            }

            qualifiers = feature.qualifiers

            # Extract common qualifiers
            if "gene" in qualifiers:
                data["gene_name"] = qualifiers["gene"][0]
                feature_data["qualifiers"]["gene"] = qualifiers["gene"][0]

            if "product" in qualifiers:
                data["protein_name"] = qualifiers["product"][0]
                feature_data["qualifiers"]["product"] = qualifiers["product"][0]

            if "EC_number" in qualifiers:
                data["ec_number"] = qualifiers["EC_number"][0]
                feature_data["qualifiers"]["EC_number"] = qualifiers["EC_number"][0]

            if "tissue_type" in qualifiers:
                data["tissue"] = qualifiers["tissue_type"][0]
                feature_data["qualifiers"]["tissue_type"] = qualifiers["tissue_type"][0]

            if "dev_stage" in qualifiers:
                data["stage"] = qualifiers["dev_stage"][0]
                feature_data["qualifiers"]["dev_stage"] = qualifiers["dev_stage"][0]

            # Store note field if present
            if "note" in qualifiers:
                feature_data["qualifiers"]["note"] = " ".join(qualifiers["note"])

            data["features"].append(feature_data)

        return data

    def retrieve_and_parse(
        self,
        database: str,
        acc_id: str
    ) -> Optional[Dict]:
        """
        Retrieve and parse a sequence, using cache if available

        Args:
            database: Database name
            acc_id: Accession ID

        Returns:
            Parsed sequence dictionary or None
        """
        # Check cache first
        cached_data = self._load_from_cache(database, acc_id)
        if cached_data:
            logger.debug(f"Loaded {acc_id} from cache")
            return cached_data

        # Fetch from NCBI
        gb_data = self.fetch_sequence(database, acc_id, rettype="gb")
        if not gb_data:
            return None

        try:
            # Parse GenBank format
            from io import StringIO
            record = SeqIO.read(StringIO(gb_data), "genbank")
            parsed_data = self.parse_genbank_record(record)

            # Add source metadata
            parsed_data["source_database"] = database
            parsed_data["accession_id"] = acc_id

            # Save to cache
            self._save_to_cache(database, acc_id, parsed_data)

            return parsed_data

        except Exception as e:
            logger.error(f"Error parsing {acc_id}: {e}")
            return None

    def retrieve_batch(
        self,
        database: str,
        id_list: List[str],
        max_batch_size: int = 50
    ) -> List[Dict]:
        """
        Retrieve and parse multiple sequences in batches

        Args:
            database: Database name
            id_list: List of accession IDs
            max_batch_size: Maximum number of IDs per batch request

        Returns:
            List of parsed sequence dictionaries
        """
        all_sequences = []

        for i in range(0, len(id_list), max_batch_size):
            batch = id_list[i:i + max_batch_size]
            logger.info(f"Processing batch {i//max_batch_size + 1} ({len(batch)} sequences)")

            for acc_id in batch:
                seq_data = self.retrieve_and_parse(database, acc_id)
                if seq_data:
                    all_sequences.append(seq_data)

        logger.info(f"Retrieved {len(all_sequences)} sequences successfully")
        return all_sequences

    def export_fasta(
        self,
        sequences: List[Dict],
        output_file: str,
        include_metadata: bool = True
    ):
        """
        Export sequences to FASTA format

        Args:
            sequences: List of sequence dictionaries
            output_file: Output FASTA file path
            include_metadata: Include metadata in FASTA headers
        """
        with open(output_file, 'w') as f:
            for seq in sequences:
                # Build FASTA header
                if include_metadata:
                    header = (
                        f">{seq['accession']} "
                        f"{seq.get('gene_name', 'unknown')} "
                        f"{seq.get('organism', 'unknown')} "
                        f"[tissue={seq.get('tissue', 'unknown')}] "
                        f"[ec={seq.get('ec_number', 'unknown')}]"
                    )
                else:
                    header = f">{seq['accession']} {seq['description']}"

                f.write(header + "\n")

                # Write sequence in 60-character lines
                sequence = seq['sequence']
                for i in range(0, len(sequence), 60):
                    f.write(sequence[i:i+60] + "\n")

        logger.info(f"Exported {len(sequences)} sequences to {output_file}")

    def get_sra_metadata(self, sra_id: str) -> Optional[Dict]:
        """
        Get metadata for an SRA run

        Args:
            sra_id: SRA accession ID

        Returns:
            Dictionary with SRA metadata
        """
        self._rate_limit_wait()

        try:
            handle = Entrez.efetch(db="sra", id=sra_id, retmode="xml")
            records = Entrez.read(handle)
            handle.close()

            if not records:
                return None

            # Extract relevant metadata
            metadata = {
                "accession": sra_id,
                "title": "",
                "organism": "",
                "tissue": "",
                "stage": "",
                "library_strategy": "",
                "instrument": "",
                "bioproject": "",
                "biosample": ""
            }

            # Parse XML structure (simplified)
            # Real implementation would need more robust XML parsing
            record = records[0] if isinstance(records, list) else records

            # This is a simplified extraction - actual SRA XML is more complex
            # You would need to navigate the XML structure properly

            return metadata

        except Exception as e:
            logger.error(f"Error fetching SRA metadata for {sra_id}: {e}")
            return None


def create_retriever(use_cache: bool = True) -> SequenceRetriever:
    """Factory function to create SequenceRetriever instance"""
    return SequenceRetriever(use_cache=use_cache)


if __name__ == "__main__":
    # Test the retriever
    retriever = create_retriever()

    # Test fetching a known protein
    test_id = "XP_018093312"  # Example EAB protein
    result = retriever.retrieve_and_parse("protein", test_id)

    if result:
        print(f"Retrieved: {result['accession']}")
        print(f"Organism: {result['organism']}")
        print(f"Gene: {result['gene_name']}")
        print(f"Protein: {result['protein_name']}")
        print(f"Length: {result['length']} aa")
