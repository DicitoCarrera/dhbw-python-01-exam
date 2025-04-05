import os
from typing import Optional, Tuple

from .Domain import Position
from .GameState import GameState


def render_board(state: GameState) -> str:
    """Render the game board as a string"""
    # Column headers
    result = "    " + " ".join(str(i) for i in range(state.width)) + "\n"
    result += "   " + "-" * (state.width * 2 - 1) + "\n"

    # Rows with row headers
    for y in range(state.height):
        result += f"{y} | "
        for x in range(state.width):
            cell = state.visible_board[y][x]
            result += cell + " "
        result += "|\n"

    result += "   " + "-" * (state.width * 2 - 1) + "\n"

    # Game status
    if state.game_over:
        result += "\nGAME OVER! You triggered a trap!\n"
    elif state.win:
        result += "\nCONGRATULATIONS! You've successfully scanned all safe areas!\n"

    return result


def clear_screen() -> None:
    """Clear the console screen"""
    os.system("cls" if os.name == "nt" else "clear")


def get_player_input() -> Tuple[Optional[Position], bool]:
    """Get player input for the next move"""
    try:
        user_input = input("Enter coordinates to scan (x y) or 'q' to quit: ")

        if user_input.lower() == "q":
            return None, True

        parts = user_input.split()
        if len(parts) != 2:
            print("Invalid input. Please enter coordinates as 'x y'.")
            return None, False

        try:
            x, y = int(parts[0]), int(parts[1])
            return Position((x, y)), False
        except ValueError:
            print("Invalid coordinates. Please enter numbers only.")
            return None, False

    except KeyboardInterrupt:
        return None, True
