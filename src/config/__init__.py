"""Game configuration constants."""

from src.types_mod import GRID_ROWS, GRID_COLS
from typing import Final

# Grid dimensions
GRID_SIZE: Final[tuple[int, int]] = (GRID_ROWS, GRID_COLS)

# Game rules
MIN_THEME_WORDS: Final[int] = 6
MAX_THEME_WORDS: Final[int] = 8
MIN_WORDS_FOR_HINT: Final[int] = 3

# Board requirements
SPANGRAM_LENGTH_MIN: Final[int] = 8  # Must touch both sides
SPANGRAM_LENGTH_MAX: Final[int] = 14

# Scoring
BASE_WORD_SCORE: Final[int] = 10
SPANGRAM_BONUS: Final[int] = 100
HINT_PENALTY: Final[int] = 50

# Colors (for UI)
COLOR_THEME: Final[str] = "blue"
COLOR_SPANGRAM: Final[str] = "yellow"

# File paths for theme words
THEME_WORDS_FILE: Final[str] = "data/theme_words.json"
LEXICON_FILE: Final[str] = "data/lexicon.txt"
