import random
from typing import List, cast

from .Domain import EMPTY, HIDDEN, TRAP, CellContent, GameBoard, HiddenBoard, Position
from .GameState import GameState


def create_empty_board(
    width: int, height: int, cell: CellContent
) -> List[List[CellContent]]:
    """Create an empty board filled with the given cell content"""
    return [[cell for _ in range(width)] for _ in range(height)]


def count_adjacent_dangers(
    board: HiddenBoard, width: int, height: int, x: int, y: int
) -> int:
    """Count adjacent dangers around a given position"""
    count = 0
    # Check all 8 adjacent cells
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Skip the center cell

            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and board[ny][nx] == TRAP:
                count += 1

    return count


def initialize_game(
    width: int = 8, height: int = 8, trap_percentage: float = 0.15
) -> GameState:
    """Initialize a new game with the given parameters"""
    if width < 5 or height < 5:
        # Ensure minimum board size requirement is met
        width = max(width, 5)
        height = max(height, 5)

    # Calculate number of traps based on percentage
    trap_count = int(width * height * trap_percentage)
    trap_count = max(
        1, min(trap_count, width * height - 1)
    )  # Ensure at least 1 trap, but not all

    # Create empty boards
    hidden_board = cast(HiddenBoard, create_empty_board(width, height, EMPTY))
    visible_board = cast(GameBoard, create_empty_board(width, height, HIDDEN))

    # Generate danger positions
    all_positions = [(x, y) for x in range(width) for y in range(height)]
    danger_positions = set(
        cast(List[Position], random.sample(all_positions, trap_count))
    )

    # Place dangers on hidden board
    for pos in danger_positions:
        x, y = pos
        hidden_board[y][x] = TRAP

    # Calculate adjacent danger counts and update the hidden board
    for y in range(height):
        for x in range(width):
            pos = Position((x, y))
            if pos not in danger_positions:
                adjacent_count = count_adjacent_dangers(
                    hidden_board, width, height, x, y
                )
                if adjacent_count > 0:
                    hidden_board[y][x] = CellContent(str(adjacent_count))

    return GameState(
        width=width,
        height=height,
        trap_count=trap_count,
        hidden_board=hidden_board,
        visible_board=visible_board,
        danger_positions=danger_positions,
    )
