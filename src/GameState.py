from typing import Set

from .Domain import GameBoard, HiddenBoard, Position


class GameState:
    """Immutable representation of the game state"""

    def __init__(
        self,
        width: int,
        height: int,
        trap_count: int,
        hidden_board: HiddenBoard,
        visible_board: GameBoard,
        danger_positions: Set[Position],
    ) -> None:
        self.width = width
        self.height = height
        self.trap_count = trap_count
        self.hidden_board = hidden_board
        self.visible_board = visible_board
        self.danger_positions = danger_positions
        self.game_over = False
        self.win = False

    def with_updates(self, **kwargs: object) -> "GameState":
        """Creates a new game state with updated values"""
        new_state = GameState(
            width=self.width,
            height=self.height,
            trap_count=self.trap_count,
            hidden_board=self.hidden_board,
            visible_board=self.visible_board,
            danger_positions=self.danger_positions,
        )

        # Apply all updates
        for key, value in kwargs.items():
            setattr(new_state, key, value)

        return new_state
