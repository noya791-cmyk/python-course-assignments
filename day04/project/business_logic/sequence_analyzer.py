"""
Sequence Analyzer Module

Analyzes and compares protein sequences using string matching algorithms.
Calculates identity percentages and similarity scores.
"""

from difflib import SequenceMatcher


class SequenceAnalyzer:
    """Analyzes protein sequences and performs comparisons."""
    
    @staticmethod
    def calculate_identity_percentage(seq1, seq2):
        """
        Calculate the percentage of identical positions between two sequences.
        
        Args:
            seq1 (str): First protein sequence
            seq2 (str): Second protein sequence
        
        Returns:
            float: Identity percentage (0-100), rounded to 2 decimal places
        """
        if not seq1 or not seq2:
            return 0.0
        
        matcher = SequenceMatcher(None, seq1, seq2)
        matching_chars = sum(block.size for block in matcher.get_matching_blocks())
        max_length = max(len(seq1), len(seq2))
        
        identity = (matching_chars / max_length) * 100
        return round(identity, 2)
    
    @staticmethod
    def calculate_similarity_score(seq1, seq2):
        """
        Calculate overall sequence similarity using SequenceMatcher ratio.
        
        Args:
            seq1 (str): First protein sequence
            seq2 (str): Second protein sequence
        
        Returns:
            float: Similarity ratio (0.0 to 1.0)
        """
        if not seq1 or not seq2:
            return 0.0
        
        matcher = SequenceMatcher(None, seq1, seq2)
        return round(matcher.ratio(), 4)
    
    @staticmethod
    def get_sequence_statistics(sequence):
        """
        Generate amino acid composition statistics for a sequence.
        
        Args:
            sequence (str): Protein sequence
        
        Returns:
            dict: Statistics including length and composition
        """
        if not sequence:
            return {'length': 0, 'composition': {}}
        
        composition = {}
        for aa in sequence:
            if aa not in composition:
                composition[aa] = {'count': 0, 'percentage': 0.0}
            composition[aa]['count'] += 1
        
        seq_length = len(sequence)
        for aa in composition:
            composition[aa]['percentage'] = round(
                (composition[aa]['count'] / seq_length) * 100, 2
            )
        
        return {
            'length': seq_length,
            'composition': composition
        }
    
    @staticmethod
    def compare_sequences(seq1_data, seq2_data):
        """
        Comprehensive comparison of two protein sequences.
        
        Args:
            seq1_data (dict): Dictionary with keys 'sequence' and 'title'
            seq2_data (dict): Dictionary with keys 'sequence' and 'title'
        
        Returns:
            dict: Comparison results including identity, similarity, and stats
        """
        try:
            seq1 = seq1_data.get('sequence', '')
            seq2 = seq2_data.get('sequence', '')
            
            if not seq1 or not seq2:
                return {
                    'error': 'One or both sequences are empty',
                    'identity_percentage': 0.0,
                    'similarity_ratio': 0.0
                }
            
            identity = SequenceAnalyzer.calculate_identity_percentage(seq1, seq2)
            similarity = SequenceAnalyzer.calculate_similarity_score(seq1, seq2)
            
            seq1_stats = SequenceAnalyzer.get_sequence_statistics(seq1)
            seq2_stats = SequenceAnalyzer.get_sequence_statistics(seq2)
            
            return {
                'identity_percentage': identity,
                'similarity_ratio': similarity,
                'seq1': {
                    'title': seq1_data.get('title', 'Sequence 1'),
                    'length': len(seq1),
                    'stats': seq1_stats
                },
                'seq2': {
                    'title': seq2_data.get('title', 'Sequence 2'),
                    'length': len(seq2),
                    'stats': seq2_stats
                }
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'identity_percentage': 0.0,
                'similarity_ratio': 0.0
            }
