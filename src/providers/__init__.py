"""Provider layer - cross-cutting concerns."""

from src.types_mod import GameState
from typing import Protocol


class Logger(Protocol):
    """Interface for logging."""

    def info(self, message: str) -> None:
        """Log an info message."""
        ...

    def error(self, message: str) -> None:
        """Log an error message."""
        ...

    def debug(self, message: str) -> None:
        """Log a debug message."""
        ...


class GridGenerator(Protocol):
    """Interface for grid generation."""

    def generate_grid(self, theme_words: list[str]) -> tuple[tuple[str, ...], ...]:
        """Generate a new grid with the given theme words."""
        ...

    def place_spangram(self, grid, spangram: str) -> tuple[tuple[str, ...], ...]:
        """Place the spangram on the grid."""
        ...

    def fill_remaining(self, grid) -> tuple[tuple[str, ...], ...]:
        """Fill remaining cells with random letters."""
        ...
