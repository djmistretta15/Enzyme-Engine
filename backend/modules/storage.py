"""
Storage Module
Handles SQLite database operations for enzyme data
"""
import sqlite3
import json
from typing import List, Dict, Optional, Any
from pathlib import Path
import logging
from datetime import datetime

from ..config import DB_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manage SQLite database for enzyme sequences"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._ensure_database()

    def _ensure_database(self):
        """Create database and tables if they don't exist"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Organisms table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS organisms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    taxid TEXT UNIQUE,
                    name TEXT NOT NULL,
                    family TEXT,
                    taxonomy TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Sequences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sequences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    accession TEXT UNIQUE NOT NULL,
                    source_db TEXT NOT NULL,
                    organism_id INTEGER,
                    gene_name TEXT,
                    protein_name TEXT,
                    enzyme_type TEXT,
                    ec_number TEXT,
                    gh_family TEXT,
                    sequence TEXT,
                    length INTEGER,
                    description TEXT,
                    tissue TEXT,
                    dev_stage TEXT,
                    confidence REAL,
                    annotation_data TEXT,
                    features TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (organism_id) REFERENCES organisms(id)
                )
            ''')

            # BioProjects table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bioprojects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bioproject_id TEXT UNIQUE NOT NULL,
                    title TEXT,
                    organism_id INTEGER,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (organism_id) REFERENCES organisms(id)
                )
            ''')

            # SRA runs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sra_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sra_id TEXT UNIQUE NOT NULL,
                    bioproject_id INTEGER,
                    organism_id INTEGER,
                    tissue TEXT,
                    dev_stage TEXT,
                    library_strategy TEXT,
                    instrument TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (bioproject_id) REFERENCES bioprojects(id),
                    FOREIGN KEY (organism_id) REFERENCES organisms(id)
                )
            ''')

            # Keywords table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS keywords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT UNIQUE NOT NULL,
                    category TEXT,
                    count INTEGER DEFAULT 0
                )
            ''')

            # Sequence-Keyword junction table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sequence_keywords (
                    sequence_id INTEGER,
                    keyword_id INTEGER,
                    PRIMARY KEY (sequence_id, keyword_id),
                    FOREIGN KEY (sequence_id) REFERENCES sequences(id),
                    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
                )
            ''')

            # BLAST results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blast_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id TEXT NOT NULL,
                    subject_id TEXT NOT NULL,
                    identity REAL,
                    coverage REAL,
                    evalue REAL,
                    bitscore REAL,
                    alignment_length INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sequences_accession ON sequences(accession)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sequences_enzyme_type ON sequences(enzyme_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sequences_organism ON sequences(organism_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sequences_confidence ON sequences(confidence)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_blast_query ON blast_results(query_id)')

            conn.commit()
            logger.info(f"Database initialized at {self.db_path}")

    def insert_organism(self, name: str, taxid: Optional[str] = None, family: Optional[str] = None, taxonomy: Optional[List[str]] = None) -> int:
        """Insert or get organism ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Check if exists
            cursor.execute('SELECT id FROM organisms WHERE name = ?', (name,))
            result = cursor.fetchone()
            if result:
                return result[0]

            # Insert new
            taxonomy_json = json.dumps(taxonomy) if taxonomy else None
            cursor.execute('''
                INSERT INTO organisms (taxid, name, family, taxonomy)
                VALUES (?, ?, ?, ?)
            ''', (taxid, name, family, taxonomy_json))
            conn.commit()
            return cursor.lastrowid

    def insert_sequence(self, sequence_data: Dict) -> int:
        """Insert a sequence into the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Get or create organism
            organism_id = self.insert_organism(
                name=sequence_data.get("organism", "Unknown"),
                taxonomy=sequence_data.get("taxonomy")
            )

            # Prepare data
            annotation_json = json.dumps(sequence_data.get("annotation", {}))
            features_json = json.dumps(sequence_data.get("features", []))

            try:
                cursor.execute('''
                    INSERT INTO sequences (
                        accession, source_db, organism_id, gene_name, protein_name,
                        enzyme_type, ec_number, gh_family, sequence, length,
                        description, tissue, dev_stage, confidence,
                        annotation_data, features
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    sequence_data.get("accession"),
                    sequence_data.get("source_database", "unknown"),
                    organism_id,
                    sequence_data.get("gene_name"),
                    sequence_data.get("protein_name"),
                    sequence_data.get("enzyme_type"),
                    sequence_data.get("ec_number_annotated"),
                    sequence_data.get("gh_family"),
                    sequence_data.get("sequence", ""),
                    sequence_data.get("length", 0),
                    sequence_data.get("description"),
                    sequence_data.get("tissue"),
                    sequence_data.get("stage"),
                    sequence_data.get("confidence", 0.0),
                    annotation_json,
                    features_json
                ))
                conn.commit()
                seq_id = cursor.lastrowid

                # Insert keywords
                keywords = sequence_data.get("annotation", {}).get("keywords_found", [])
                for keyword in keywords:
                    self._insert_keyword_link(seq_id, keyword, "enzyme")

                return seq_id

            except sqlite3.IntegrityError:
                # Sequence already exists, update it
                cursor.execute('''
                    UPDATE sequences SET
                        source_db = ?, organism_id = ?, gene_name = ?,
                        protein_name = ?, enzyme_type = ?, ec_number = ?,
                        gh_family = ?, sequence = ?, length = ?,
                        description = ?, tissue = ?, dev_stage = ?,
                        confidence = ?, annotation_data = ?, features = ?
                    WHERE accession = ?
                ''', (
                    sequence_data.get("source_database", "unknown"),
                    organism_id,
                    sequence_data.get("gene_name"),
                    sequence_data.get("protein_name"),
                    sequence_data.get("enzyme_type"),
                    sequence_data.get("ec_number_annotated"),
                    sequence_data.get("gh_family"),
                    sequence_data.get("sequence", ""),
                    sequence_data.get("length", 0),
                    sequence_data.get("description"),
                    sequence_data.get("tissue"),
                    sequence_data.get("stage"),
                    sequence_data.get("confidence", 0.0),
                    annotation_json,
                    features_json,
                    sequence_data.get("accession")
                ))
                conn.commit()

                # Get existing ID
                cursor.execute('SELECT id FROM sequences WHERE accession = ?', (sequence_data.get("accession"),))
                return cursor.fetchone()[0]

    def _insert_keyword_link(self, sequence_id: int, keyword: str, category: str):
        """Link a keyword to a sequence"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Insert or get keyword
            cursor.execute('SELECT id FROM keywords WHERE keyword = ?', (keyword,))
            result = cursor.fetchone()

            if result:
                keyword_id = result[0]
                cursor.execute('UPDATE keywords SET count = count + 1 WHERE id = ?', (keyword_id,))
            else:
                cursor.execute('INSERT INTO keywords (keyword, category, count) VALUES (?, ?, 1)', (keyword, category))
                keyword_id = cursor.lastrowid

            # Link sequence to keyword
            cursor.execute('''
                INSERT OR IGNORE INTO sequence_keywords (sequence_id, keyword_id)
                VALUES (?, ?)
            ''', (sequence_id, keyword_id))

            conn.commit()

    def insert_batch(self, sequences: List[Dict]) -> int:
        """Insert multiple sequences"""
        count = 0
        for seq in sequences:
            try:
                self.insert_sequence(seq)
                count += 1
            except Exception as e:
                logger.error(f"Error inserting {seq.get('accession')}: {e}")

        logger.info(f"Inserted {count}/{len(sequences)} sequences")
        return count

    def query_sequences(
        self,
        enzyme_type: Optional[str] = None,
        min_confidence: float = 0.0,
        organism: Optional[str] = None,
        tissue: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """Query sequences with filters"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = '''
                SELECT s.*, o.name as organism_name, o.family
                FROM sequences s
                LEFT JOIN organisms o ON s.organism_id = o.id
                WHERE s.confidence >= ?
            '''
            params = [min_confidence]

            if enzyme_type:
                query += ' AND s.enzyme_type = ?'
                params.append(enzyme_type)

            if organism:
                query += ' AND o.name LIKE ?'
                params.append(f'%{organism}%')

            if tissue:
                query += ' AND s.tissue LIKE ?'
                params.append(f'%{tissue}%')

            query += ' ORDER BY s.confidence DESC'

            if limit:
                query += f' LIMIT {limit}'

            cursor.execute(query, params)
            rows = cursor.fetchall()

            return [dict(row) for row in rows]

    def get_statistics(self) -> Dict:
        """Get database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            stats = {}

            # Total counts
            cursor.execute('SELECT COUNT(*) FROM sequences')
            stats['total_sequences'] = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM organisms')
            stats['total_organisms'] = cursor.fetchone()[0]

            # Enzyme type distribution
            cursor.execute('''
                SELECT enzyme_type, COUNT(*) as count
                FROM sequences
                WHERE enzyme_type IS NOT NULL
                GROUP BY enzyme_type
                ORDER BY count DESC
            ''')
            stats['enzyme_types'] = dict(cursor.fetchall())

            # Top organisms
            cursor.execute('''
                SELECT o.name, COUNT(s.id) as count
                FROM organisms o
                JOIN sequences s ON o.id = s.organism_id
                GROUP BY o.name
                ORDER BY count DESC
                LIMIT 10
            ''')
            stats['top_organisms'] = dict(cursor.fetchall())

            # Average confidence
            cursor.execute('SELECT AVG(confidence) FROM sequences')
            stats['avg_confidence'] = cursor.fetchone()[0] or 0.0

            return stats

    def export_to_csv(self, output_file: str, filters: Optional[Dict] = None):
        """Export sequences to CSV"""
        import csv

        sequences = self.query_sequences(**(filters or {}))

        with open(output_file, 'w', newline='') as f:
            if not sequences:
                return

            writer = csv.DictWriter(f, fieldnames=sequences[0].keys())
            writer.writeheader()
            writer.writerows(sequences)

        logger.info(f"Exported {len(sequences)} sequences to {output_file}")


def create_database_manager() -> DatabaseManager:
    """Factory function to create DatabaseManager instance"""
    return DatabaseManager()


if __name__ == "__main__":
    # Test the database
    db = create_database_manager()

    # Get statistics
    stats = db.get_statistics()
    print("Database Statistics:")
    print(f"  Total sequences: {stats['total_sequences']}")
    print(f"  Total organisms: {stats['total_organisms']}")
    print(f"  Average confidence: {stats['avg_confidence']:.2f}")
