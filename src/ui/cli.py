"""CLI UI implementation."""

from src.types_mod import GameState, Word
from src.config import GRID_ROWS, GRID_COLS


class CliRenderer:
    """CLI renderer for the game."""
    
    def display_grid(self, state: GameState) -> None:
        """Display the game grid."""
        grid = state.grid
        print("\n+" + "-" * (GRID_COLS * 2 - 1) + "+")
        
        for row_idx, row in enumerate(grid):
            line = "|"
            for col_idx, cell in enumerate(row):
                # Check if this cell is part of a found word
                cell_color = self._get_cell_color(row_idx, col_idx, state)
                line += f" {cell} "
            line += "|"
            print(line)
        
        print("+" + "-" * (GRID_COLS * 2 - 1) + "+")
    
    def _get_cell_color(self, row: int, col: int, state: GameState) -> str:
        """Get color indicator for a cell."""
        return ""
    
    def display_status(self, state: GameState) -> None:
        """Display game status."""
        print(f"\nScore: {state.calculate_score()}")
        print(f"Found: {len(state.found_words)} words")
        print(f"Remaining: {len(state.theme_words_remaining)} theme words")
    
    def display_message(self, message: str) -> None:
        """Display a message to the user."""
        print(f"\n{message}")
    
    def display_found_words(self, state: GameState) -> None:
        """Display found words grouped by type."""
        theme_words = [w for w in state.found_words if w.word_type == "theme"]
        spangrams = [w for w in state.found_words if w.word_type == "spangram"]
        other_words = [w for w in state.found_words if w.word_type == "valid"]
        
        if spangrams:
            print("\n** SPANGRAM **")
            for word in spangrams:
                print(f"  {word.text}")
        
        if theme_words:
            print("\nTheme Words:")
            for word in theme_words:
                print(f"  {word.text}")
        
        if other_words:
            print("\nOther Words:")
            for word in other_words:
                print(f"  {word.text}")


class CliInputHandler:
    """CLI input handler."""
    
    def get_user_input(self) -> str:
        """Get input from the user."""
        return input("Enter your selection or command: ")
    
    def parse_command(self, input_str: str) -> tuple[str, list[str]]:
        """Parse user input into command and arguments."""
        parts = input_str.strip().split()
        if not parts:
            return ("", [])
        return (parts[0].lower(), parts[1:])
