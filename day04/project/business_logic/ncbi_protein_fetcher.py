"""
NCBI Protein Fetcher Module

Handles all interactions with the NCBI Protein database via BioPython.
Searches for proteins and retrieves amino acid sequences.
"""

import time
from Bio import Entrez


class ProteinFetcher:
    """Fetches protein sequences from NCBI Protein database."""
    
    def __init__(self, email="student@python-course.com", delay=0.4):
        """
        Initialize the protein fetcher.
        
        Args:
            email (str): Email for NCBI (required by NCBI guidelines)
            delay (float): Delay between requests in seconds (respect NCBI rate limits)
        """
        Entrez.email = email
        self.delay = delay
        self.last_request_time = 0
    
    def _respect_rate_limit(self):
        """Ensure minimum delay between NCBI requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def search_protein(self, protein_name, organism, max_results=5):
        """
        Search for a protein in a specific organism.
        
        Args:
            protein_name (str): Name of the protein (e.g., "hemoglobin")
            organism (str): Scientific organism name (e.g., "Homo sapiens")
            max_results (int): Maximum number of results to return
        
        Returns:
            list: List of (accession_id, title, organism_name) tuples
        """
        try:
            self._respect_rate_limit()
            
            search_term = f"{protein_name}[Title] AND {organism}[Organism]"
            handle = Entrez.esearch(
                db="protein",
                term=search_term,
                retmax=max_results,
                rettype="xml"
            )
            record = Entrez.read(handle)
            handle.close()
            
            if not record["IdList"]:
                return []
            
            results = []
            for protein_id in record["IdList"]:
                # Fetch details for each protein
                self._respect_rate_limit()
                handle = Entrez.efetch(
                    db="protein",
                    id=protein_id,
                    rettype="xml"
                )
                records = Entrez.read(handle)
                handle.close()
                
                if records:
                    protein_record = records[0]
                    accession = protein_record.get("GBSeq_primary-accession", protein_id)
                    title = protein_record.get("GBSeq_definition", "Unknown")
                    results.append((accession, title, organism))
            
            return results
        
        except Exception as e:
            raise Exception(f"NCBI search error: {str(e)}")
    
    def fetch_sequence(self, accession_id):
        """
        Retrieve the amino acid sequence for a protein.
        
        Args:
            accession_id (str): NCBI protein accession ID
        
        Returns:
            str: Protein sequence, or None if retrieval fails
        """
        try:
            self._respect_rate_limit()
            
            handle = Entrez.efetch(
                db="protein",
                id=accession_id,
                rettype="fasta"
            )
            record = handle.read()
            handle.close()
            
            # Extract sequence from FASTA format
            lines = record.strip().split('\n')
            if len(lines) > 1:
                sequence = ''.join(lines[1:])
                return sequence
            
            return None
        
        except Exception as e:
            raise Exception(f"Sequence fetch error: {str(e)}")
    
    def get_protein_in_organisms(self, protein_name, organisms):
        """
        Search for a protein in multiple organisms.
        
        Args:
            protein_name (str): Name of the protein
            organisms (list): List of organism names
        
        Returns:
            dict: Mapping of organism names to protein data or None
                {
                    "Homo sapiens": {
                        'accession': str,
                        'sequence': str,
                        'title': str,
                        'length': int
                    } or None,
                    "Danio rerio": {...} or None
                }
        """
        results = {}
        
        for organism in organisms:
            try:
                search_results = self.search_protein(protein_name, organism, max_results=1)
                
                if search_results:
                    accession, title, org = search_results[0]
                    sequence = self.fetch_sequence(accession)
                    
                    if sequence:
                        results[organism] = {
                            'accession': accession,
                            'sequence': sequence,
                            'title': title,
                            'length': len(sequence)
                        }
                    else:
                        results[organism] = None
                else:
                    results[organism] = None
            
            except Exception as e:
                print(f"Error searching {organism}: {str(e)}")
                results[organism] = None
        
        return results
