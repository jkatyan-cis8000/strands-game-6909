"""Main entry point for the Strands game."""

import sys
from src.config import THEME_WORDS_FILE
from src.types_mod import GameState, Word, Path, Position
from src.providers import GridGenerator, Logger
from src.providers.impl import SimpleGridGenerator, SimpleLogger
from src.repo import ThemeWordRepository, LexiconRepository
from src.repo.impl import ThemeWordRepositoryImpl, LexiconRepositoryImpl
from src.service import GameLogic
from src.service.game_logic import HintGenerator
from src.ui.cli import CliRenderer, CliInputHandler
from src.runtime import GameLoop, InputHandler, OutputHandler


def create_game() -> GameState:
    """Create a new game with default state."""
    logger = SimpleLogger()
    logger.info("Creating new game...")
    
    # Initialize repositories
    theme_repo = ThemeWordRepositoryImpl()
    
    # Get theme words (use default category if available)
    categories = theme_repo.get_all_categories()
    if categories:
        theme_words = theme_repo.get_theme_words(categories[0])
    else:
        theme_words = ["PYTHON", "JAVA", "RUBY", "GO", "SWIFT"]
    
    # Initialize game logic
    grid_gen = SimpleGridGenerator(logger)
    lexicon = LexiconRepositoryImpl()
    
    # Generate grid
    grid = grid_gen.generate_grid(theme_words)
    
    # Find spangram (longest word >= 8 letters)
    spangram = ""
    for word in theme_words:
        if len(word) >= 8:
            spangram = word
            break
    
    remaining = tuple(w for w in theme_words if w != spangram)
    
    state = GameState(
        grid=grid,
        theme_words_remaining=remaining,
        spangram=spangram
    )
    
    logger.info(f"Game created with {len(theme_words)} theme words")
    logger.info(f"Spangram: {spangram}")
    
    return state


def run_cli_game() -> None:
    """Run the game with CLI interface."""
    state = create_game()
    
    # Initialize components
    logger = SimpleLogger()
    renderer = CliRenderer()
    input_handler = CliInputHandler()
    
    game_logic = GameLogic(
        grid_generator=SimpleGridGenerator(logger),
        theme_repo=ThemeWordRepositoryImpl(),
        lexicon=LexiconRepositoryImpl()
    )
    
    hint_gen = HintGenerator(ThemeWordRepositoryImpl())
    game_loop = GameLoop(game_logic)
    output_handler = OutputHandler(renderer)
    
    # Bind actions
    ui_input = InputHandler(input_handler)
    
    def cmd_quit():
        game_loop.stop()
        return "Goodbye!"
    
    def cmd_hint():
        if hint_gen.check_hint_eligibility(state.non_theme_words_found):
            if state.theme_words_remaining:
                word = state.theme_words_remaining[0]
                return f"Hint: {hint_gen.get_hint_for_word(word)}"
            return "No hints available"
        return f"Need {3 - state.non_theme_words_found} more words for a hint"
    
    def cmd_status():
        score = game_logic.calculate_score(state)
        print(f"\nScore: {score}")
        print(f"Found: {len(state.found_words)} words")
        print(f"Remaining: {len(state.theme_words_remaining)} theme words")
        output_handler.display_found_words(state)
        return ""
    
    def cmd_grid():
        output_handler.display_grid(state)
        return ""
    
    ui_input.bind_action("quit", cmd_quit)
    ui_input.bind_action("q", cmd_quit)
    ui_input.bind_action("hint", cmd_hint)
    ui_input.bind_action("h", cmd_hint)
    ui_input.bind_action("status", cmd_status)
    ui_input.bind_action("s", cmd_status)
    ui_input.bind_action("grid", cmd_grid)
    ui_input.bind_action("g", cmd_grid)
    
    # Start game
    game_loop.start()
    output_handler.display_grid(state)
    output_handler.display_status(state)
    
    print("\nCommands: (h)int, (s)tatus, (g)rid, (q)uit")
    print("Select adjacent cells to form words (click or drag)")
    
    while game_loop.is_running():
        user_input = input("\n> ")
        
        if not user_input.strip():
            continue
        
        result = ui_input.process_input(user_input)
        if result:
            output_handler.display_message(result)
        
        if user_input.strip().lower() in ("quit", "q"):
            break


def main() -> None:
    """Main entry point."""
    try:
        run_cli_game()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
