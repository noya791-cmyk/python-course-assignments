"""
Configuration Module

Central configuration for NCBI settings, GUI theme, and organisms.
"""

# NCBI Settings
NCBI_EMAIL = "student@python-course.com"
NCBI_RATE_LIMIT_DELAY = 0.4  # seconds between requests
NCBI_RETMAX = 5  # maximum results per search
NCBI_TIMEOUT = 30  # connection timeout in seconds

# Organisms to compare
PRIMARY_ORGANISM = "Homo sapiens"
SECONDARY_ORGANISM = "Danio rerio"

ORGANISMS = [PRIMARY_ORGANISM, SECONDARY_ORGANISM]

# Organism display names
ORGANISM_DISPLAY_NAMES = {
    "Homo sapiens": "Human",
    "Danio rerio": "Zebrafish"
}

# GUI Theme Colors
GUI_THEME = {
    "background": "#2B2D42",
    "foreground": "#00D9FF",
    "accent": "#00D9FF",
    "success": "#90EE90",
    "error": "#FF6B6B",
    "warning": "#FFD700",
    "info": "#87CEEB",
    "dark": "#1A1A2E"
}

# GUI Fonts
GUI_FONT_SIZE = {
    "title": ("Helvetica", 16, "bold"),
    "header": ("Helvetica", 11, "bold"),
    "normal": ("Helvetica", 10),
    "small": ("Helvetica", 9),
    "mono": ("Courier", 9)
}

# Comparison Thresholds
IDENTITY_THRESHOLD_HIGH = 80.0      # >80% = high similarity
IDENTITY_THRESHOLD_MODERATE = 50.0  # 50-80% = moderate similarity
# <50% = low similarity

# Standard Amino Acids
AMINO_ACIDS = {
    'A': 'Alanine',
    'R': 'Arginine',
    'N': 'Asparagine',
    'D': 'Aspartic acid',
    'C': 'Cysteine',
    'Q': 'Glutamine',
    'E': 'Glutamic acid',
    'G': 'Glycine',
    'H': 'Histidine',
    'I': 'Isoleucine',
    'L': 'Leucine',
    'K': 'Lysine',
    'M': 'Methionine',
    'F': 'Phenylalanine',
    'P': 'Proline',
    'S': 'Serine',
    'T': 'Threonine',
    'W': 'Tryptophan',
    'Y': 'Tyrosine',
    'V': 'Valine'
}
