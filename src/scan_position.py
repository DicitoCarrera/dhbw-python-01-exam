from typing import Set, cast

from .Domain import EMPTY, HIDDEN, TRAP, GameBoard, Position
from .GameState import GameState


def auto_expand(state: GameState, x: int, y: int) -> GameState:
    """Auto-expand when an empty cell is revealed"""
    # Create a working copy of the visible board
    new_visible = [row[:] for row in state.visible_board]

    # Use a set to track cells to expand to avoid duplicates
    to_expand: Set[Position] = {Position((x, y))}
    expanded: Set[Position] = set()

    while to_expand:
        current = to_expand.pop()
        cx, cy = current

        if current in expanded:
            continue

        expanded.add(current)

        # Reveal current cell
        new_visible[cy][cx] = state.hidden_board[cy][cx]

        # If current cell is empty, add adjacent cells to expansion list
        if state.hidden_board[cy][cx] == EMPTY:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = cx + dx, cy + dy
                    if (
                        0 <= nx < state.width
                        and 0 <= ny < state.height
                        and state.visible_board[ny][nx] == HIDDEN
                    ):
                        to_expand.add(Position((nx, ny)))

    return state.with_updates(visible_board=cast(GameBoard, new_visible))


def is_win_condition(state: GameState) -> bool:
    """Check if the win condition is met"""
    # Win if all non-danger cells are revealed
    hidden_count = sum(row.count(HIDDEN) for row in state.visible_board)
    return hidden_count == len(state.danger_positions)


def scan_position(state: GameState, pos: Position) -> GameState:
    """Scan a position on the game board"""
    x, y = pos

    # Check if position is valid
    if not (0 <= x < state.width and 0 <= y < state.height):
        return state  # Invalid position, return unchanged state

    # Check if already revealed
    if state.visible_board[y][x] != HIDDEN:
        return state  # Already revealed, return unchanged state

    # Check if hit a trap
    if pos in state.danger_positions:
        # Create new visible board showing all dangers
        new_visible = [row[:] for row in state.visible_board]
        new_visible[y][x] = TRAP

        return state.with_updates(
            visible_board=cast(GameBoard, new_visible), game_over=True
        )

    # Reveal the cell
    new_visible = [row[:] for row in state.visible_board]
    new_visible[y][x] = state.hidden_board[y][x]

    new_state = state.with_updates(visible_board=cast(GameBoard, new_visible))

    # Check if auto-expand (empty cell with no adjacent dangers)
    if state.hidden_board[y][x] == EMPTY:
        new_state = auto_expand(new_state, x, y)

    # Check win condition
    if is_win_condition(new_state):
        new_state = new_state.with_updates(win=True)

    return new_state
