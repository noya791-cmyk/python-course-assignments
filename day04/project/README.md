# NCBI Protein Comparator

A Python application that allows the user to enter the name of a particular protein and then uses NCBI Protein database to find the amino acid sequence to compare the protein in humans with that in zebrafish.

## Project Overview

This program allows users to:

1. Enter the name of a particular protein
2. Search the NCBI Protein database to find the amino acid sequence
3. Compare the protein between humans and zebrafish
4. Obtain information about whether the protein is present in both organisms
5. View the results of the comparison between sequences with percentage of identity

The program provides a clean separation between business logic and the user interface (UI), with all generated files (like `__pycache__`) properly excluded from version control via .gitignore.

## Scientific Background and Project Inspiration

I got the idea from one of the projects I'm currently working on where we're screening a number of different FDA-approved drugs for a lymphatic vessel disease that currently has no drug treatment. To do this, we're introducing a copy of the mutant gene from a patient into zebrafish, which we're using as a model. The gene we're working with is known to be conserved between humans and zebrafish, and we want to see if a mutation in it causes the same disease. This project should also serve as a pipeline for genes that cause other diseases down the road.

## Features

NCBI Integration
  Search the NCBI Protein database for specific proteins

Multi-organism Search
  Automatically searches for the same protein in both humans and zebrafish

Sequence Retrieval
  Fetches complete amino acid sequences for found proteins

Sequence Comparison
  Calculates sequence identity percentage
  Computes similarity ratios
  Analyzes amino acid composition

User-Friendly GUI
  Built with tkinter for easy interaction

NCBI Rate Limiting
  Respects NCBI's rate limits (0.4 seconds between requests)

## Architecture: Separated Business Logic and UI

This program implements a clean separation of concerns with professional software architecture:

Business Logic (business_logic/ package)
  Pure Python modules with NO UI dependencies
  Contains all NCBI interactions and sequence analysis
  Can be used independently in CLI, Web, or other applications
  Easy to test and reuse in different contexts

User Interface (ui/ package)
  tkinter-based GUI implementation
  Depends only on the business_logic package
  Handles all user interaction and display
  Can be replaced with alternative UI frameworks

This separation ensures:
  Clean code organization
  Testability of business logic
  Reusability across different interfaces
  Easy maintenance and extension

## .gitignore Configuration

The project includes proper .gitignore configuration to prevent uploading:
  __pycache__/ - Python cache directories
  *.pyc - Compiled Python files
  *.pyo - Optimized Python files
  *.pyd - Python dynamic modules
  .venv/ and venv/ - Virtual environment folders
  .vscode/ and .idea/ - IDE configuration
  *.egg-info/ - Package metadata
  dist/ and build/ - Build artifacts
  .env and .env.local - Environment variables
  *.cache and *.tmp - Temporary files
  *.log - Log files

This ensures only source code and essential files are committed to GitHub.

## Installation

Prerequisites:
  Python 3.7 or higher
  pip package manager

Setup:

1. Navigate to the project directory:
   cd day04/project

2. Install required packages:
   pip install -r requirements.txt

## Usage

Running the GUI Application

   python main.py

This will launch a GUI window where you can:

1. Enter a protein name (e.g., "hemoglobin", "insulin", "catalase")
2. Click "Search & Compare" to:
   - Search NCBI for the protein in humans
   - Search NCBI for the protein in zebrafish
   - Retrieve both sequences
   - Compare them and display results
3. View Results showing:
   - Whether the protein was found in each organism
   - Protein accession IDs
   - Sequence lengths
   - Identity percentage between sequences
   - Similarity interpretation

## Project Structure

day04/project/
  
  business_logic/              - Core logic (NO UI dependencies)
    __init__.py               - Package initialization
    protein_comparator.py     - Main orchestrator
    ncbi_protein_fetcher.py   - NCBI database access
    sequence_analyzer.py      - Sequence comparison
  
  ui/                         - User interface
    __init__.py               - Package initialization
    gui.py                    - tkinter GUI implementation
  
  main.py                     - Entry point
  config.py                   - Configuration
  requirements.txt            - Dependencies
  README.md                   - This file

## Module Documentation

ncbi_protein_fetcher.py

ProteinFetcher class:
  search_protein(protein_name, organism)
    Search for a protein in a specific organism

  fetch_sequence(accession_id)
    Retrieve the amino acid sequence

  get_protein_in_organisms(protein_name, organisms)
    Find a protein in multiple organisms

Features:
  Automatic rate limiting for NCBI API (0.4 seconds between requests)
  Error handling for network and API issues
  Returns accession IDs, sequences, titles, and metadata

sequence_analyzer.py

SequenceAnalyzer class:
  calculate_identity_percentage()
    Calculates percentage of identical amino acids

  calculate_similarity_score()
    Computes similarity ratio using sequence matching

  get_sequence_statistics()
    Analyzes amino acid composition

  compare_sequences()
    Comprehensive comparison of two sequences

protein_comparator.py

ProteinComparator class:
  search_and_compare()
    Coordinates search across multiple organisms

  compare_sequences()
    Initiates sequence comparison

  format_results()
    Prepares results for display

## Example Usage

Command Line (Python script)

   from business_logic import ProteinComparator

   # Initialize
   comparator = ProteinComparator()

   # Search for hemoglobin
   results = comparator.search_and_compare(
       "hemoglobin",
       ["Homo sapiens", "Danio rerio"]
   )

   # Compare if both found
   if results["Homo sapiens"] and results["Danio rerio"]:
       comparison = comparator.compare_sequences(
           results["Homo sapiens"],
           results["Danio rerio"]
       )
       print(f"Identity: {comparison['identity_percentage']:.2f}%")

## Important Notes

NCBI Guidelines
  This application respects NCBI's usage guidelines by implementing rate limiting
  An email address is required and is set to "student@python-course.com" by default
  For production use, change the email in config.py

Search Tips
  1. Use common protein names (e.g., "hemoglobin", "insulin", "myoglobin")
  2. More specific searches are often more successful
  3. Some proteins may only be annotated in one organism

Known Limitations
  Simple sequence matching (not advanced alignment algorithms like BLAST)
  Identity percentage based on longest sequence as reference
  Limited to the first matching result for each organism
  Requires internet connection for NCBI access

## Supported Organisms

Homo sapiens (Human)
Danio rerio (Zebrafish)

## Results Interpretation

Identity Percentage
  >80%:    High similarity, likely homologous proteins
  50-80%:  Moderate similarity, probable function conservation
  <50%:    Low similarity, different protein families

Sequence Statistics
  Shows the distribution of amino acids in each sequence
  Helps identify compositional differences between organisms

## Troubleshooting

"NCBI search error"
  Check your internet connection
  Ensure you have recent versions of required packages
  NCBI servers may be temporarily unavailable

"Protein not found"
  Try a different protein name
  Use the full protein name instead of abbreviation
  Some proteins may not be in the NCBI database

"No sequences returned"
  NCBI may have the protein but without sequence data
  Try searching for a different protein variant

## Architecture

Clean Separation of Concerns

business_logic/ - Pure Python, NO tkinter or UI dependencies
  Can be used independently in CLI, Web, or other applications
  Easy to test without GUI
  Can be imported and reused in other projects

ui/ - GUI Implementation
  Depends on business_logic
  Handles all user interaction and display
  Can be replaced with alternative UI (Qt, Web, etc.)

## Future Enhancements

Support for multiple organisms
Advanced alignment algorithms (MUSCLE, ClustalW)
Multiple sequence alignment visualization
Export results to FASTA format
Phylogenetic tree generation
WebLogo visualization of sequence alignment
Command-line interface (CLI)
Web-based interface (Flask/Django)

## Dependencies

biopython - For NCBI interaction and sequence handling
           https://biopython.org/

requests - For HTTP requests (dependency of biopython)
          https://requests.readthedocs.io/

## References

NCBI Entrez API
  https://www.ncbi.nlm.nih.gov/books/NBK25499/

BioPython Documentation
  https://biopython.org/

NCBI Protein Database
  https://www.ncbi.nlm.nih.gov/protein/

## License

This educational project is provided as-is for learning purposes.

## Author

Created for Python course assignments - Educational Project

Last Updated: November 2025
