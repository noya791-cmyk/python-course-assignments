"""
Business Logic Package

Core business logic for protein comparison, completely independent of UI.
"""

from .protein_comparator import ProteinComparator
from .ncbi_protein_fetcher import ProteinFetcher
from .sequence_analyzer import SequenceAnalyzer

__all__ = [
    'ProteinComparator',
    'ProteinFetcher',
    'SequenceAnalyzer'
]
