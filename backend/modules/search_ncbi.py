"""
NCBI Search Module
Handles searching across NCBI databases for EAB enzyme-related sequences
"""
import time
from typing import List, Dict, Optional, Set
from Bio import Entrez
import logging
from collections import defaultdict

from ..config import (
    NCBI_EMAIL, NCBI_API_KEY, NCBI_TOOL, NCBI_RATE_LIMIT,
    PRIMARY_ORGANISM, RELATED_SPECIES, ENZYME_KEYWORDS,
    GUT_TISSUES, DEVELOPMENTAL_STAGES, DATABASES, MAX_RESULTS_PER_QUERY
)

# Configure Entrez
Entrez.email = NCBI_EMAIL
Entrez.tool = NCBI_TOOL
if NCBI_API_KEY:
    Entrez.api_key = NCBI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NCBISearcher:
    """Search NCBI databases for enzyme sequences"""

    def __init__(self, rate_limit: float = NCBI_RATE_LIMIT):
        self.rate_limit = rate_limit
        self.last_request_time = 0

    def _rate_limit_wait(self):
        """Ensure compliance with NCBI rate limits"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    def search_database(
        self,
        database: str,
        query: str,
        max_results: int = MAX_RESULTS_PER_QUERY,
        retstart: int = 0
    ) -> Dict[str, any]:
        """
        Search a specific NCBI database

        Args:
            database: NCBI database name (e.g., 'nucleotide', 'protein')
            query: Search query string
            max_results: Maximum number of results to return
            retstart: Starting index for pagination

        Returns:
            Dictionary containing search results and metadata
        """
        self._rate_limit_wait()

        try:
            logger.info(f"Searching {database} with query: {query[:100]}...")

            # Search for IDs
            handle = Entrez.esearch(
                db=database,
                term=query,
                retmax=max_results,
                retstart=retstart,
                usehistory="y"
            )
            search_results = Entrez.read(handle)
            handle.close()

            id_list = search_results.get("IdList", [])
            count = int(search_results.get("Count", 0))

            logger.info(f"Found {count} total results, retrieved {len(id_list)} IDs")

            return {
                "database": database,
                "query": query,
                "id_list": id_list,
                "count": count,
                "webenv": search_results.get("WebEnv"),
                "query_key": search_results.get("QueryKey")
            }

        except Exception as e:
            logger.error(f"Error searching {database}: {e}")
            return {
                "database": database,
                "query": query,
                "id_list": [],
                "count": 0,
                "error": str(e)
            }

    def build_enzyme_query(
        self,
        organism: str,
        enzyme_type: Optional[str] = None,
        include_gut: bool = True,
        include_stages: bool = True
    ) -> str:
        """
        Build a comprehensive search query for enzyme discovery

        Args:
            organism: Target organism name
            enzyme_type: Specific enzyme type (e.g., 'cellulase') or None for all
            include_gut: Include gut tissue keywords
            include_stages: Include developmental stage keywords

        Returns:
            Formatted search query string
        """
        query_parts = [f'"{organism}"[Organism]']

        # Add enzyme keywords
        if enzyme_type and enzyme_type in ENZYME_KEYWORDS:
            enzyme_data = ENZYME_KEYWORDS[enzyme_type]
            keywords = " OR ".join(enzyme_data["keywords"])
            query_parts.append(f"({keywords})")
        else:
            # All enzyme types
            all_keywords = []
            for enzyme_data in ENZYME_KEYWORDS.values():
                all_keywords.extend(enzyme_data["keywords"])
            keywords = " OR ".join(set(all_keywords))
            query_parts.append(f"({keywords})")

        # Add tissue keywords
        if include_gut:
            tissues = " OR ".join(GUT_TISSUES)
            query_parts.append(f"({tissues})")

        # Add developmental stage keywords
        if include_stages:
            stages = " OR ".join(DEVELOPMENTAL_STAGES)
            query_parts.append(f"({stages})")

        return " AND ".join(query_parts)

    def search_all_organisms(
        self,
        database: str = "protein",
        enzyme_type: Optional[str] = None,
        include_related: bool = True
    ) -> List[Dict[str, any]]:
        """
        Search for enzymes across primary organism and related species

        Args:
            database: NCBI database to search
            enzyme_type: Specific enzyme type or None for all
            include_related: Include related Buprestidae species

        Returns:
            List of search result dictionaries
        """
        organisms = [PRIMARY_ORGANISM]
        if include_related:
            organisms.extend(RELATED_SPECIES)

        all_results = []

        for organism in organisms:
            query = self.build_enzyme_query(
                organism=organism,
                enzyme_type=enzyme_type,
                include_gut=True,
                include_stages=True
            )

            results = self.search_database(
                database=database,
                query=query
            )
            results["organism"] = organism
            all_results.append(results)

        return all_results

    def search_transcriptomes(
        self,
        organism: str = PRIMARY_ORGANISM
    ) -> Dict[str, any]:
        """
        Search for transcriptome and RNA-Seq datasets

        Args:
            organism: Target organism name

        Returns:
            Search results dictionary
        """
        tissues = " OR ".join(GUT_TISSUES)
        stages = " OR ".join(DEVELOPMENTAL_STAGES)

        query = (
            f'"{organism}"[Organism] AND '
            f'({tissues}) AND '
            f'({stages}) AND '
            f'(transcriptome OR "RNA-Seq" OR "RNA sequencing")'
        )

        return self.search_database(database="sra", query=query)

    def search_by_ec_number(
        self,
        ec_number: str,
        organism: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Search for sequences by EC number

        Args:
            ec_number: EC number (e.g., '3.2.1.4')
            organism: Optional organism filter

        Returns:
            Search results dictionary
        """
        query = f'"{ec_number}"[EC/RN Number]'

        if organism:
            query += f' AND "{organism}"[Organism]'

        return self.search_database(database="protein", query=query)

    def search_bioprojects(
        self,
        organism: str = PRIMARY_ORGANISM,
        keywords: Optional[List[str]] = None
    ) -> Dict[str, any]:
        """
        Search for BioProjects related to organism

        Args:
            organism: Target organism name
            keywords: Additional keywords to include

        Returns:
            Search results dictionary
        """
        query = f'"{organism}"[Organism]'

        if keywords:
            keyword_str = " OR ".join(keywords)
            query += f' AND ({keyword_str})'

        return self.search_database(database="bioproject", query=query)

    def get_taxonomy_ids(self, family: str = "Buprestidae") -> List[str]:
        """
        Get all taxonomy IDs for a given family

        Args:
            family: Taxonomic family name

        Returns:
            List of taxonomy IDs
        """
        self._rate_limit_wait()

        try:
            handle = Entrez.esearch(
                db="taxonomy",
                term=f'"{family}"[Scientific Name]'
            )
            results = Entrez.read(handle)
            handle.close()

            return results.get("IdList", [])

        except Exception as e:
            logger.error(f"Error fetching taxonomy IDs: {e}")
            return []

    def link_databases(
        self,
        db_from: str,
        db_to: str,
        id_list: List[str]
    ) -> List[str]:
        """
        Use ELink to find connections between databases

        Args:
            db_from: Source database
            db_to: Target database
            id_list: List of IDs from source database

        Returns:
            List of linked IDs in target database
        """
        if not id_list:
            return []

        self._rate_limit_wait()

        try:
            handle = Entrez.elink(
                dbfrom=db_from,
                db=db_to,
                id=",".join(str(i) for i in id_list)
            )
            results = Entrez.read(handle)
            handle.close()

            linked_ids = []
            for linkset in results:
                if "LinkSetDb" in linkset:
                    for link_db in linkset["LinkSetDb"]:
                        for link in link_db.get("Link", []):
                            linked_ids.append(link["Id"])

            return list(set(linked_ids))

        except Exception as e:
            logger.error(f"Error linking databases: {e}")
            return []

    def comprehensive_search(
        self,
        enzyme_type: Optional[str] = None,
        databases: Optional[List[str]] = None
    ) -> Dict[str, List[Dict]]:
        """
        Perform comprehensive search across multiple databases and organisms

        Args:
            enzyme_type: Specific enzyme type or None for all
            databases: List of databases to search (default: all configured)

        Returns:
            Dictionary mapping database names to search results
        """
        if databases is None:
            databases = ["protein", "nucleotide", "sra"]

        logger.info(f"Starting comprehensive search for enzyme: {enzyme_type or 'all'}")

        results_by_db = defaultdict(list)

        for database in databases:
            logger.info(f"Searching {database}...")

            # Search primary organism and related species
            organism_results = self.search_all_organisms(
                database=database,
                enzyme_type=enzyme_type,
                include_related=True
            )

            results_by_db[database].extend(organism_results)

        # Also search for transcriptomes in SRA
        if "sra" in databases:
            logger.info("Searching transcriptomes...")
            transcriptome_results = self.search_transcriptomes()
            results_by_db["sra_transcriptomes"] = [transcriptome_results]

        logger.info("Comprehensive search complete")
        return dict(results_by_db)


def create_searcher() -> NCBISearcher:
    """Factory function to create NCBISearcher instance"""
    return NCBISearcher()


if __name__ == "__main__":
    # Test the searcher
    searcher = create_searcher()

    # Test search for cellulase
    results = searcher.search_all_organisms(
        database="protein",
        enzyme_type="cellulase"
    )

    for result in results:
        print(f"\nOrganism: {result['organism']}")
        print(f"Found: {result['count']} results")
        print(f"Retrieved: {len(result['id_list'])} IDs")
