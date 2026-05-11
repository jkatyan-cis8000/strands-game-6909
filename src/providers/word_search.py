"""Word search algorithms and validation utilities."""

import random
from src.types_mod import Position, Path, GRID_ROWS, GRID_COLS
from src.providers import GridGenerator
from src.utils import PositionCalculator, PathValidator
from src.repo import LexiconRepository
from typing import Optional


def get_adjacent_positions(row: int, col: int) -> list[tuple[int, int]]:
    """Get all adjacent positions (including diagonals) for a cell."""
    positions = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < GRID_ROWS and 0 <= new_col < GRID_COLS:
                positions.append((new_row, new_col))
    return positions


def is_valid_position(row: int, col: int) -> bool:
    """Check if a position is within the grid bounds."""
    return 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS


def is_valid_path(positions: list[tuple[int, int]]) -> bool:
    """Check if a path is valid (contiguous, no duplicates)."""
    if len(positions) < 2:
        return False
    
    # Check for duplicates
    if len(positions) != len(set(positions)):
        return False
    
    # Check contiguity
    for i in range(len(positions) - 1):
        r1, c1 = positions[i]
        r2, c2 = positions[i + 1]
        if not (abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1):
            return False
    
    return True


def find_paths_from(
    start: tuple[int, int],
    length: int,
    grid: tuple[tuple[str, ...], ...],
    lexicon: Optional[LexiconRepository] = None
) -> list[Path]:
    """Find all valid paths of a given length from a starting position."""
    if length < 2:
        return []
    
    paths = []
    visited = set()
    visited.add(start)
    
    def backtrack(pos: tuple[int, int], current_path: list[tuple[int, int]]):
        if len(current_path) == length:
            # Create Path object and validate
            positions_tuple = tuple(Position(r, c) for r, c in current_path)
            path = Path(positions_tuple)
            if path.is_valid_path():
                paths.append(path)
            return
        
        r, c = pos
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_r, new_c = r + dr, c + dc
                if (new_r, new_c) not in visited and is_valid_position(new_r, new_c):
                    visited.add((new_r, new_c))
                    current_path.append((new_r, new_c))
                    backtrack((new_r, new_c), current_path)
                    current_path.pop()
                    visited.remove((new_r, new_c))
    
    backtrack(start, list([start]))
    return paths


def generate_random_grid() -> tuple[tuple[str, ...], ...]:
    """Generate a random 6x8 grid of letters."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    grid = []
    for _ in range(GRID_ROWS):
        row = tuple(random.choice(alphabet) for _ in range(GRID_COLS))
        grid.append(row)
    return tuple(grid)


def is_spangram(path: Path) -> bool:
    """Check if a path forms a spangram (touches opposite sides)."""
    positions = path.positions
    first_pos = positions[0]
    last_pos = positions[-1]
    
    # Check if first is on left and last is on right, or vice versa
    first_left = first_pos.col == 0
    first_right = first_pos.col == GRID_COLS - 1
    last_left = last_pos.col == 0
    last_right = last_pos.col == GRID_COLS - 1
    
    # Check if first is on top and last is on bottom, or vice versa
    first_top = first_pos.row == 0
    first_bottom = first_pos.row == GRID_ROWS - 1
    last_top = last_pos.row == 0
    last_bottom = last_pos.row == GRID_ROWS - 1
    
    return (first_left and last_right) or (first_right and last_left) or \
           (first_top and last_bottom) or (first_bottom and last_top)


class GridGeneratorImpl:
    """Implementation of GridGenerator protocol."""
    
    def __init__(self, lexicon: LexiconRepository):
        self._lexicon = lexicon
    
    def generate_grid(self, theme_words: list[str]) -> tuple[tuple[str, ...], ...]:
        """Generate a new grid with the given theme words."""
        # Start with empty grid
        grid = [["" for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        
        # Place theme words
        for word in theme_words:
            self._place_word_in_grid(grid, word)
        
        # Fill remaining cells
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                if not grid[r][c]:
                    grid[r][c] = random.choice(alphabet)
        
        return tuple(tuple(row) for row in grid)
    
    def _place_word_in_grid(
        self,
        grid: list[list[str]],
        word: str
    ) -> bool:
        """Try to place a word in the grid."""
        directions = [
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (1, 1),   # diagonal down-right
            (1, -1),  # diagonal down-left
        ]
        
        for _ in range(100):  # Try 100 times
            r = random.randint(0, GRID_ROWS - 1)
            c = random.randint(0, GRID_COLS - 1)
            dr, dc = random.choice(directions)
            
            if self._can_place_word(grid, word, r, c, dr, dc):
                self._place_word(grid, word, r, c, dr, dc)
                return True
        
        return False
    
    def _can_place_word(
        self,
        grid: list[list[str]],
        word: str,
        start_r: int,
        start_c: int,
        dr: int,
        dc: int
    ) -> bool:
        """Check if a word can be placed at the given position."""
        r, c = start_r, start_c
        for char in word:
            if not is_valid_position(r, c):
                return False
            if grid[r][c] and grid[r][c] != char:
                return False
            r += dr
            c += dc
        return True
    
    def _place_word(
        self,
        grid: list[list[str]],
        word: str,
        start_r: int,
        start_c: int,
        dr: int,
        dc: int
    ):
        """Place a word in the grid."""
        r, c = start_r, start_c
        for char in word:
            grid[r][c] = char
            r += dr
            c += dc
