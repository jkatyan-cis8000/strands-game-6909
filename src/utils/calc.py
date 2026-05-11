"""Position and path calculation utilities."""

from src.types_mod import GRID_ROWS, GRID_COLS


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
