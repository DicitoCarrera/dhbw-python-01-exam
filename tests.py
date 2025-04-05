"""
Unit tests for the Abandoned Space Station game.
"""

import unittest
from typing import List, Set, cast

from src.Domain import (
    EMPTY,
    HIDDEN,
    TRAP,
    CellContent,
    GameBoard,
    HiddenBoard,
    Position,
)
from src.GameState import GameState
from src.initialize_game import (
    count_adjacent_dangers,
    create_empty_board,
    initialize_game,
)
from src.io_game import render_board
from src.scan_position import is_win_condition, scan_position


class TestGameFunctions(unittest.TestCase):
    """Test cases for game functions"""

    def test_create_empty_board(self) -> None:
        """Test creating an empty board"""
        width, height = 5, 5
        cell = HIDDEN
        board = create_empty_board(width, height, cell)

        self.assertEqual(len(board), height)
        self.assertEqual(len(board[0]), width)
        for row in board:
            for cell_content in row:
                self.assertEqual(cell_content, cell)

    def test_initialize_game(self) -> None:
        """Test game initialization"""
        width, height = 5, 5
        state = initialize_game(width, height)

        # Check board dimensions
        self.assertEqual(len(state.hidden_board), height)
        self.assertEqual(len(state.hidden_board[0]), width)
        self.assertEqual(len(state.visible_board), height)
        self.assertEqual(len(state.visible_board[0]), width)

        # Check trap count
        self.assertEqual(len(state.danger_positions), state.trap_count)

        # Check that all visible cells are hidden
        for row in state.visible_board:
            for cell in row:
                self.assertEqual(cell, HIDDEN)

        # Check that dangers are correctly placed
        danger_count = 0
        for y in range(height):
            for x in range(width):
                if state.hidden_board[y][x] == TRAP:
                    danger_count += 1
                    self.assertIn(Position((x, y)), state.danger_positions)

        self.assertEqual(danger_count, state.trap_count)

    def test_count_adjacent_dangers(self) -> None:
        """Test counting adjacent dangers"""
        # Create a test board with known danger positions
        board: List[List[CellContent]] = [
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, TRAP, EMPTY, TRAP, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, TRAP, EMPTY, EMPTY, TRAP],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        ]
        hidden_board = cast(HiddenBoard, board)

        # Test various positions
        test_cases = [
            ((0, 0), 1),  # Corner with 1 adjacent
            ((1, 1), 0),  # On danger - should return 0
            ((2, 2), 3),  # Center with 3 adjacent (not 4)
            ((4, 4), 1),  # Corner with 1 adjacent
            ((2, 1), 2),  # Edge case
        ]

        for pos, expected in test_cases:
            x, y = pos
            if board[y][x] != TRAP:  # Skip danger positions
                count = count_adjacent_dangers(hidden_board, 5, 5, x, y)
                self.assertEqual(
                    count,
                    expected,
                    f"Position {pos} should have {expected} adjacent dangers",
                )

    def test_scan_position_safe(self) -> None:
        """Test scanning a safe position"""
        # Create a controlled game state
        width, height = 5, 5
        hidden_board = cast(HiddenBoard, create_empty_board(width, height, EMPTY))
        visible_board = cast(GameBoard, create_empty_board(width, height, HIDDEN))
        danger_positions: Set[Position] = {Position((1, 1)), Position((3, 3))}

        # Place dangers
        for pos in danger_positions:
            x, y = pos
            hidden_board[y][x] = TRAP

        # Update adjacent numbers
        for y in range(height):
            for x in range(width):
                pos = Position((x, y))
                if pos not in danger_positions:
                    adjacent_count = count_adjacent_dangers(
                        hidden_board, width, height, x, y
                    )
                    if adjacent_count > 0:
                        hidden_board[y][x] = CellContent(str(adjacent_count))

        state = GameState(
            width=width,
            height=height,
            trap_count=len(danger_positions),
            hidden_board=hidden_board,
            visible_board=visible_board,
            danger_positions=danger_positions,
        )

        # Scan a safe position
        new_state = scan_position(state, Position((0, 0)))

        # Check that position was revealed
        self.assertNotEqual(new_state.visible_board[0][0], HIDDEN)
        # Game should not be over
        self.assertFalse(new_state.game_over)

    def test_scan_position_danger(self) -> None:
        """Test scanning a danger position"""
        # Create a controlled game state
        width, height = 5, 5
        hidden_board = cast(HiddenBoard, create_empty_board(width, height, EMPTY))
        visible_board = cast(GameBoard, create_empty_board(width, height, HIDDEN))
        danger_positions: Set[Position] = {Position((1, 1)), Position((3, 3))}

        # Place dangers
        for pos in danger_positions:
            x, y = pos
            hidden_board[y][x] = TRAP

        state = GameState(
            width=width,
            height=height,
            trap_count=len(danger_positions),
            hidden_board=hidden_board,
            visible_board=visible_board,
            danger_positions=danger_positions,
        )

        # Scan a danger position
        new_state = scan_position(state, Position((1, 1)))

        # Check that position was revealed as a trap
        self.assertEqual(new_state.visible_board[1][1], TRAP)
        # Game should be over
        self.assertTrue(new_state.game_over)

    def test_auto_expand(self) -> None:
        """Test auto-expansion of empty cells"""
        # Create a controlled game state with a cluster of empty cells
        width, height = 5, 5
        hidden_board = cast(HiddenBoard, create_empty_board(width, height, EMPTY))
        visible_board = cast(GameBoard, create_empty_board(width, height, HIDDEN))
        danger_positions: Set[Position] = {Position((4, 4))}

        # Place dangers
        for pos in danger_positions:
            x, y = pos
            hidden_board[y][x] = TRAP

        # Update adjacent numbers
        for y in range(height):
            for x in range(width):
                pos = Position((x, y))
                if pos not in danger_positions:
                    adjacent_count = count_adjacent_dangers(
                        hidden_board, width, height, x, y
                    )
                    if adjacent_count > 0:
                        hidden_board[y][x] = CellContent(str(adjacent_count))

        state = GameState(
            width=width,
            height=height,
            trap_count=len(danger_positions),
            hidden_board=hidden_board,
            visible_board=visible_board,
            danger_positions=danger_positions,
        )

        # Scan a position in the middle of empty cells
        new_state = scan_position(state, Position((0, 0)))

        # Check that multiple cells were revealed by auto-expansion
        revealed_count = sum(
            1 for row in new_state.visible_board for cell in row if cell != HIDDEN
        )
        self.assertGreater(revealed_count, 1)

    def test_is_win_condition(self) -> None:
        """Test win condition detection"""
        width, height = 3, 3
        hidden_board = cast(HiddenBoard, create_empty_board(width, height, EMPTY))
        visible_board = cast(GameBoard, create_empty_board(width, height, HIDDEN))
        danger_positions: Set[Position] = {Position((1, 1))}

        # Place dangers
        for pos in danger_positions:
            x, y = pos
            hidden_board[y][x] = TRAP

        state = GameState(
            width=width,
            height=height,
            trap_count=len(danger_positions),
            hidden_board=hidden_board,
            visible_board=visible_board,
            danger_positions=danger_positions,
        )

        # Not winning yet - all cells hidden
        self.assertFalse(is_win_condition(state))

        # Reveal all safe cells
        new_visible = [row[:] for row in visible_board]
        for y in range(height):
            for x in range(width):
                if Position((x, y)) not in danger_positions:
                    new_visible[y][x] = hidden_board[y][x]

        new_state = state.with_updates(visible_board=cast(GameBoard, new_visible))

        # Now should be winning
        self.assertTrue(is_win_condition(new_state))

    def test_render_board(self) -> None:
        """Test board rendering"""
        width, height = 3, 3
        hidden_board = cast(HiddenBoard, create_empty_board(width, height, EMPTY))
        visible_board = cast(GameBoard, create_empty_board(width, height, HIDDEN))
        danger_positions: Set[Position] = {Position((1, 1))}

        state = GameState(
            width=width,
            height=height,
            trap_count=len(danger_positions),
            hidden_board=hidden_board,
            visible_board=visible_board,
            danger_positions=danger_positions,
        )

        rendered = render_board(state)
        # Basic check for rendering format
        self.assertIn("0 | # # # |", rendered)
        self.assertIn("1 | # # # |", rendered)
        self.assertIn("2 | # # # |", rendered)

        # Test game over rendering
        game_over_state = state.with_updates(game_over=True)
        rendered = render_board(game_over_state)
        self.assertIn("GAME OVER", rendered)

        # Test win rendering
        win_state = state.with_updates(win=True)
        rendered = render_board(win_state)
        self.assertIn("CONGRATULATIONS", rendered)


if __name__ == "__main__":
    unittest.main()
