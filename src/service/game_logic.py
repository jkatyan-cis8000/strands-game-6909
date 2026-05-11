"""Game logic - board generation, scoring, and hint generation."""

from src.types_mod import GameState, Word, Selection, Path
from src.providers import GridGenerator
from src.repo import LexiconRepository, ThemeWordRepository
from src.utils import is_valid_path, get_adjacent_positions
from src.config import MIN_WORDS_FOR_HINT, SPANGRAM_LENGTH_MIN, SPANGRAM_LENGTH_MAX
from typing import Optional


class GameLogic:
    """Core game logic implementation."""
    
    def __init__(
        self,
        grid_generator: GridGenerator,
        theme_repo: ThemeWordRepository,
        lexicon: LexiconRepository
    ):
        self._grid_generator = grid_generator
        self._theme_repo = theme_repo
        self._lexicon = lexicon
    
    def validate_selection(
        self,
        selection: Selection,
        state: GameState
    ) -> Optional[Word]:
        """Validate a player's selection of cells."""
        path = selection.path
        
        # Check if path is contiguous
        if not path.is_valid_path():
            return None
        
        # Get letters from path
        letters = path.get_letters(state.grid)
        
        # Check if word is in lexicon
        if not self._lexicon.is_valid_word(letters):
            return None
        
        # Determine word type
        word_type = "valid"
        if letters == state.spangram:
            word_type = "spangram"
        elif letters in state.theme_words_remaining:
            word_type = "theme"
        
        return Word(text=letters, path=path, word_type=word_type)
    
    def apply_selection(self, state: GameState, word: Word) -> GameState:
        """Update game state after a valid word is found."""
        # Update found words
        new_words = tuple(list(state.found_words) + [word])
        
        # Update remaining theme words if it's a theme word
        new_remaining = state.theme_words_remaining
        if word.word_type == "theme":
            new_remaining = tuple(w for w in state.theme_words_remaining if w != word.text)
        
        # Check spangram status
        new_spangram_found = state.found_spangram or word.word_type == "spangram"
        
        # Update non-theme word count
        new_non_theme = state.non_theme_words_found
        if word.word_type != "theme":
            new_non_theme += 1
        
        return GameState(
            grid=state.grid,
            found_words=new_words,
            found_spangram=new_spangram_found,
            non_theme_words_found=new_non_theme,
            theme_words_remaining=new_remaining,
            spangram=state.spangram
        )
    
    def check_spangram(self, path: Path, grid) -> bool:
        """Check if a path forms a spangram (touches opposite sides)."""
        positions = path.positions
        first_pos = positions[0]
        last_pos = positions[-1]
        
        # Check horizontal (left to right or right to left)
        horizontal = (
            (first_pos.col == 0 and last_pos.col == 7) or
            (first_pos.col == 7 and last_pos.col == 0)
        )
        
        # Check vertical (top to bottom or bottom to top)
        vertical = (
            (first_pos.row == 0 and last_pos.row == 5) or
            (first_pos.row == 5 and last_pos.row == 0)
        )
        
        return horizontal or vertical
    
    def is_game_complete(self, state: GameState) -> bool:
        """Check if the game is complete."""
        # Game is complete if all theme words are found
        return len(state.theme_words_remaining) == 0
    
    def calculate_score(self, state: GameState) -> int:
        """Calculate the current score."""
        score = 0
        for word in state.found_words:
            # Base score
            word_score = max(1, len(word.text) - 2) * 10
            
            # Spangram bonus
            if word.word_type == "spangram":
                word_score += 100
            
            score += word_score
        
        return score


class HintGenerator:
    """Hint generation implementation."""
    
    def __init__(self, theme_repo: ThemeWordRepository):
        self._theme_repo = theme_repo
    
    def get_hint_for_word(self, word: str) -> Optional[str]:
        """Get a hint for a specific word."""
        # For now, return a simple hint based on word length
        if len(word) >= 7:
            return f"_starts_with_{word[0]}_and_ends_with_{word[-1]}"
        return f"_{len(word)}_letters"
    
    def check_hint_eligibility(self, non_theme_count: int) -> bool:
        """Check if player is eligible for a new hint."""
        return non_theme_count >= MIN_WORDS_FOR_HINT
