"""Service layer - business logic for the Strands game."""

from src.types_mod import GameState, Word, Selection, Hint
from src.repo import ThemeWordRepository, LexiconRepository
from typing import Protocol


class GameLogic(Protocol):
    """Interface for game logic operations."""

    def validate_selection(self, selection: Selection, state: GameState) -> Word | None:
        """Validate a player's selection of cells."""
        ...

    def apply_selection(self, state: GameState, word: Word) -> GameState:
        """Update game state after a valid word is found."""
        ...

    def check_spangram(self, path, grid) -> bool:
        """Check if a path forms a spangram (touches opposite sides)."""
        ...

    def is_game_complete(self, state: GameState) -> bool:
        """Check if the game is complete."""
        ...

    def calculate_score(self, state: GameState) -> int:
        """Calculate the current score."""
        ...


class HintGenerator(Protocol):
    """Interface for hint generation."""

    def get_hint_for_word(self, word: str) -> Hint | None:
        """Get a hint for a specific word."""
        ...

    def check_hint_eligibility(self, non_theme_count: int) -> bool:
        """Check if player is eligible for a new hint."""
        ...
