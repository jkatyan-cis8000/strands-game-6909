"""In-memory and file-based repository implementations."""

import json
import os
from typing import Optional
from src.types_mod import GameState, Word
from src.repo import ThemeWordRepository, GameRepository, LexiconRepository
from src.config import THEME_WORDS_FILE, LEXICON_FILE


class ThemeWordRepositoryImpl(ThemeWordRepository):
    """Theme word repository implementation."""
    
    def __init__(self, data_dir: str = "data"):
        self._data_dir = data_dir
        self._categories = self._load_categories()
    
    def _load_categories(self) -> dict[str, list[str]]:
        """Load theme words from JSON file."""
        filepath = os.path.join(self._data_dir, "theme_words.json")
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def get_theme_words(self, category: str) -> list[str]:
        """Get theme words for a category."""
        return self._categories.get(category, [])
    
    def get_all_categories(self) -> list[str]:
        """Get all available theme categories."""
        return list(self._categories.keys())


class LexiconRepositoryImpl(LexiconRepository):
    """Lexicon repository implementation."""
    
    def __init__(self, filepath: str = None):
        self._words: set[str] = set()
        filepath = filepath or LEXICON_FILE
        self._load_lexicon(filepath)
    
    def _load_lexicon(self, filepath: str) -> None:
        """Load words from lexicon file."""
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                for line in f:
                    word = line.strip().upper()
                    if word:
                        self._words.add(word)
    
    def is_valid_word(self, word: str) -> bool:
        """Check if a word is in the lexicon."""
        return word.upper() in self._words
    
    def get_words_of_length(self, length: int) -> list[str]:
        """Get all words of a given length."""
        return [w for w in self._words if len(w) == length]
    
    def get_words_starting_with(self, prefix: str) -> list[str]:
        """Get all words starting with a prefix."""
        prefix = prefix.upper()
        return [w for w in self._words if w.startswith(prefix)]


class GameRepositoryImpl(GameRepository):
    """Game state repository implementation."""
    
    def __init__(self, save_dir: str = "saves"):
        self._save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
    
    def save_game(self, game_state: GameState) -> None:
        """Save current game state."""
        # This is a simplified implementation
        # In a real app, we'd serialize to JSON
        pass
    
    def load_game(self, game_id: str) -> Optional[GameState]:
        """Load a saved game state."""
        # This is a simplified implementation
        return None
    
    def delete_game(self, game_id: str) -> None:
        """Delete a saved game."""
        # This is a simplified implementation
        pass
