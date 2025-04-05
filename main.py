"""
Abandoned Space Station Game - A Minesweeper-like game set in a deserted space station
where players must safely scan areas while avoiding hidden dangers.
"""

import sys

from src.initialize_game import initialize_game
from src.io_game import clear_screen, get_player_input, render_board
from src.scan_position import scan_position


def main() -> None:
    """Main game loop"""
    # Get board size from command line arguments or use defaults
    width = 8
    height = 8

    if len(sys.argv) > 2:
        try:
            width = max(5, int(sys.argv[1]))
            height = max(5, int(sys.argv[2]))
        except ValueError:
            print("Invalid arguments. Using default size.")

    # Initialize game
    state = initialize_game(width, height)

    # Game loop
    quit_game = False
    while not state.game_over and not state.win and not quit_game:
        clear_screen()
        print("=== ABANDONED SPACE STATION ===")
        print("Find all safe areas without triggering traps.")
        print(f"Board size: {state.width}x{state.height}, Traps: {state.trap_count}")
        print(render_board(state))

        position, quit_game = get_player_input()
        if position is not None:
            state = scan_position(state, position)

    # Final board state
    clear_screen()
    print("=== ABANDONED SPACE STATION ===")
    print(render_board(state))

    # Reveal all traps if game is over
    if state.game_over:
        print("\nTrap locations:")
        for pos in state.danger_positions:
            x, y = pos
            print(f"  - Position ({x}, {y})")

    print("Thanks for playing!")


if __name__ == "__main__":
    main()
