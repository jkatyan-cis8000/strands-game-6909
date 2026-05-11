"""Utility functions for the game."""

from src.types_mod import Path
from src.utils.calc import get_adjacent_positions, is_valid_position, is_valid_path as is_valid_path_calc

def is_valid_path(path: Path) -> bool:
    """Check if a path is valid."""
    return path.is_valid_path()
