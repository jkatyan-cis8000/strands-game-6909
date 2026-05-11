"""Type definitions for the Strands game."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Final

# Grid dimensions
GRID_ROWS: Final[int] = 6
GRID_COLS: Final[int] = 8


class CellState(Enum):
    """State of a grid cell."""
    EMPTY = "empty"
    SELECTED = "selected"
    HIDDEN = "hidden"


@dataclass(frozen=True)
class Position:
    """A position in the grid."""
    row: int
    col: int

    def __post_init__(self):
        if not (0 <= self.row < GRID_ROWS and 0 <= self.col < GRID_COLS):
            raise ValueError(f"Position ({self.row}, {self.col}) is out of bounds")


@dataclass(frozen=True)
class LetterCell:
    """A single cell in the grid containing a letter."""
    position: Position
    letter: str
    state: CellState = CellState.HIDDEN


@dataclass(frozen=True)
class Path:
    """A sequence of connected positions forming a word."""
    positions: tuple[Position, ...]

    def __post_init__(self):
        if len(self.positions) < 2:
            raise ValueError("Path must have at least 2 positions")
        # Validate all positions are unique
        if len(self.positions) != len(set(self.positions)):
            raise ValueError("Path contains duplicate positions")

    def get_letters(self, grid: tuple[tuple[str, ...], ...]) -> str:
        """Get the letters forming this path."""
        return "".join(grid[p.row][p.col] for p in self.positions)

    def is_adjacent(self, pos1: Position, pos2: Position) -> bool:
        """Check if two positions are adjacent (including diagonally)."""
        return (
            abs(pos1.row - pos2.row) <= 1 and
            abs(pos1.col - pos2.col) <= 1 and
            pos1 != pos2
        )

    def is_valid_path(self) -> bool:
        """Check if the path forms a valid contiguous sequence."""
        for i in range(len(self.positions) - 1):
            if not self.is_adjacent(self.positions[i], self.positions[i + 1]):
                return False
        return True


@dataclass(frozen=True)
class Word:
    """A word with its path and type."""
    text: str
    path: Path
    word_type: str  # "theme", "spangram", "valid"


@dataclass(frozen=True)
class GameState:
    """The complete game state."""
    grid: tuple[tuple[str, ...], ...]
    found_words: tuple[Word, ...] = field(default_factory=tuple)
    found_spangram: bool = False
    non_theme_words_found: int = 0
    theme_words_remaining: tuple[str, ...] = field(default_factory=tuple)
    spangram: str = ""
    
    def calculate_score(self) -> int:
        """Calculate the current score."""
        score = 0
        for word in self.found_words:
            # Base score
            word_score = max(1, len(word.text) - 2) * 10
            
            # Spangram bonus
            if word.word_type == "spangram":
                word_score += 100
            
            score += word_score
        return score


@dataclass(frozen=True)
class Selection:
    """A selection of cells by the player."""
    path: Path
    letters: str = ""

    def __post_init__(self):
        if not self.letters:
            object.__setattr__(self, "letters", self.path.get_letters(
                tuple(tuple("A" * GRID_COLS) for _ in range(GRID_ROWS))
            ))


@dataclass(frozen=True)
class Hint:
    """A hint provided to the player."""
    hint_type: str  # "length", "starts_with", "definition"
    content: str
