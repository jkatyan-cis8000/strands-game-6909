"""Repository module for data access."""

from src.types_mod import Position, Word, GameState
from typing import Protocol


class ThemeWordRepository(Protocol):
    """Interface for theme word storage."""

    def get_theme_words(self, category: str) -> list[str]:
        """Get theme words for a category."""
        ...

    def get_all_categories(self) -> list[str]:
        """Get all available theme categories."""
        ...


class GameRepository(Protocol):
    """Interface for game state persistence."""

    def save_game(self, game_state: GameState) -> None:
        """Save current game state."""
        ...

    def load_game(self, game_id: str) -> GameState | None:
        """Load a saved game state."""
        ...

    def delete_game(self, game_id: str) -> None:
        """Delete a saved game."""
        ...


class LexiconRepository(Protocol):
    """Interface for word validation."""

    def is_valid_word(self, word: str) -> bool:
        """Check if a word is in the lexicon."""
        ...

    def get_words_of_length(self, length: int) -> list[str]:
        """Get all words of a given length."""
        ...

    def get_words_starting_with(self, prefix: str) -> list[str]:
        """Get all words starting with a prefix."""
        ...
