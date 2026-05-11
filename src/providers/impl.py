"""Provider implementations for word generation and scoring."""

import random
from src.providers import GridGenerator, Logger
from src.types_mod import GRID_ROWS, GRID_COLS, CellState
from typing import Optional


class SimpleGridGenerator(GridGenerator):
    """Simple grid generator implementation."""
    
    def __init__(self, logger: Optional[Logger] = None):
        self._logger = logger
    
    def generate_grid(self, theme_words: list[str]) -> tuple[tuple[str, ...], ...]:
        """Generate a new grid with the given theme words."""
        if self._logger:
            self._logger.info(f"Generating grid with {len(theme_words)} theme words")
        
        # Initialize empty grid
        grid = tuple(
            tuple(CellState.EMPTY for _ in range(GRID_COLS)) 
            for _ in range(GRID_ROWS)
        )
        
        # Place spangram first (must touch opposite sides)
        spangram = self._find_spangram(theme_words)
        if spangram:
            grid = self._place_spangram(grid, spangram)
        
        # Place remaining theme words
        remaining = [w for w in theme_words if w != spangram]
        for word in remaining:
            grid = self._place_word(grid, word)
        
        # Fill remaining cells
        grid = self._fill_remaining(grid)
        
        return grid
    
    def _find_spangram(self, words: list[str]) -> Optional[str]:
        """Find a spangram from the word list."""
        for word in words:
            if len(word) >= 8:  # Spangram must span grid width
                return word
        return None
    
    def _place_spangram(self, grid, spangram: str):
        """Place spangram horizontally."""
        row = random.randint(0, GRID_ROWS - 1)
        col = 0
        new_grid = [list(row) for row in grid]
        
        for i, letter in enumerate(spangram):
            if col + i < GRID_COLS:
                new_grid[row][col + i] = letter
        
        return tuple(tuple(row) for row in new_grid)
    
    def _place_word(self, grid, word: str):
        """Place a single word on the grid."""
        new_grid = [list(row) for row in grid]
        
        # Try random positions
        for _ in range(100):
            row = random.randint(0, GRID_ROWS - 1)
            col = random.randint(0, GRID_COLS - len(word))
            
            # Check if space is available
            can_place = all(
                new_grid[row][col + i] in (CellState.EMPTY, word[i])
                for i in range(len(word))
            )
            
            if can_place:
                for i, letter in enumerate(word):
                    new_grid[row][col + i] = letter
                break
        
        return tuple(tuple(row) for row in new_grid)
    
    def _fill_remaining(self, grid):
        """Fill empty cells with random letters."""
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        new_grid = []
        
        for row in grid:
            new_row = []
            for cell in row:
                if cell == CellState.EMPTY:
                    new_row.append(random.choice(letters))
                else:
                    new_row.append(cell)
            new_grid.append(tuple(new_row))
        
        return tuple(new_grid)


class SimpleLogger(Logger):
    """Simple console logger implementation."""
    
    def info(self, message: str) -> None:
        print(f"[INFO] {message}")
    
    def error(self, message: str) -> None:
        print(f"[ERROR] {message}")
    
    def debug(self, message: str) -> None:
        print(f"[DEBUG] {message}")
