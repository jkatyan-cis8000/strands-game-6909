"""Runtime layer - application lifecycle and orchestration."""

from src.types_mod import GameState
from src.service import GameLogic, HintGenerator
from src.repo import ThemeWordRepository, LexiconRepository
from src.ui.cli import CliRenderer, CliInputHandler
from typing import Protocol


class GameLoop:
    """Game loop implementation."""
    
    def __init__(self, game_logic: GameLogic):
        self._game_logic = game_logic
        self._running = False
    
    def start(self) -> None:
        """Start the game loop."""
        self._running = True
    
    def stop(self) -> None:
        """Stop the game loop."""
        self._running = False
    
    def is_running(self) -> bool:
        """Check if the game is running."""
        return self._running


class InputHandler:
    """Input handler implementation."""
    
    def __init__(self, cli_input: CliInputHandler):
        self._cli_input = cli_input
        self._handlers = {}
    
    def process_input(self, input_data: str) -> str:
        """Process user input and return command/result."""
        command, args = self._cli_input.parse_command(input_data)
        handler = self._handlers.get(command)
        if handler:
            return handler(*args)
        return f"Unknown command: {command}"
    
    def bind_action(self, action: str, handler) -> None:
        """Bind an action to a handler function."""
        self._handlers[action] = handler


class OutputHandler:
    """Output handler implementation."""
    
    def __init__(self, cli_renderer: CliRenderer):
        self._cli_renderer = cli_renderer
    
    def display_grid(self, state: GameState) -> None:
        """Display the game grid."""
        self._cli_renderer.display_grid(state)
    
    def display_status(self, state: GameState) -> None:
        """Display game status."""
        self._cli_renderer.display_status(state)
    
    def display_message(self, message: str) -> None:
        """Display a message to the user."""
        self._cli_renderer.display_message(message)
