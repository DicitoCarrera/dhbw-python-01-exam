from typing import List, NewType, Tuple

# Domain types for strong typing
Position = NewType("Position", Tuple[int, int])
CellContent = NewType("CellContent", str)
GameBoard = NewType("GameBoard", List[List[CellContent]])
HiddenBoard = NewType("HiddenBoard", List[List[CellContent]])

# Constants
TRAP = CellContent("X")  # Represents a trap/danger
HIDDEN = CellContent("#")  # Represents a hidden cell
EMPTY = CellContent(" ")  # Represents an empty revealed cell
