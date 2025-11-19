"""
Protein Comparator Module

Main orchestrator that coordinates between NCBI fetcher and sequence analyzer.
"""

from .ncbi_protein_fetcher import ProteinFetcher
from .sequence_analyzer import SequenceAnalyzer


class ProteinComparator:
    """Main orchestrator for protein comparison workflow."""
    
    def __init__(self):
        """Initialize the comparator with fetcher and analyzer."""
        self.fetcher = ProteinFetcher()
        self.analyzer = SequenceAnalyzer()
    
    def search_and_compare(self, protein_name, organisms):
        """
        Search for a protein in multiple organisms and prepare for comparison.
        
        Args:
            protein_name (str): Name of the protein to search
            organisms (list): List of organism names
        
        Returns:
            dict: Search results mapping organism names to protein data
        """
        return self.fetcher.get_protein_in_organisms(protein_name, organisms)
    
    def compare_sequences(self, seq1_data, seq2_data):
        """
        Compare two protein sequences.
        
        Args:
            seq1_data (dict): Protein data for sequence 1
            seq2_data (dict): Protein data for sequence 2
        
        Returns:
            dict: Comparison results with identity and similarity
        """
        return self.analyzer.compare_sequences(seq1_data, seq2_data)
    
    def format_results(self, protein_name, search_results):
        """
        Format search results for display.
        
        Args:
            protein_name (str): Name of the protein searched
            search_results (dict): Results from search_and_compare
        
        Returns:
            dict: Formatted results ready for UI display
        """
        formatted = {
            'protein_name': protein_name,
            'search_results': search_results,
            'found_count': sum(1 for v in search_results.values() if v is not None),
            'organisms_checked': len(search_results)
        }
        return formatted
