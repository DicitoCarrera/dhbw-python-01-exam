# Abandoned Space Station Game Documentation

## Project Overview

The Abandoned Space Station Game is a console-based game inspired by Minesweeper. Players must navigate through an abandoned space station, scanning areas to find all safe locations while avoiding dangerous traps.

## Architecture

The game is implemented using a functional programming paradigm with immutable data structures and pure functions wherever possible. The architecture follows Domain-Driven Design principles and employs Algebraic Data Types (ADTs) for strong typing.

### Domain Model

The core domain model consists of:

1. **GameState**: An immutable class representing the complete state of the game
2. **Position**: A type representing a position on the game board (x, y)
3. **CellContent**: A type representing the content of a cell on the board
4. **GameBoard**: The visible board shown to the player
5. **HiddenBoard**: The complete board with all cell contents

### Key Functions

1. **initialize_game()**: Creates a new game state with randomly placed traps
2. **scan_position()**: Core game mechanic for scanning board positions
3. **auto_expand()**: Reveals connected empty cells when an empty cell is scanned
4. **is_win_condition()**: Checks if all safe cells have been revealed
5. **render_board()**: Converts game state to string representation for console display

## Typing System

The project uses Python's typing system extensively to ensure type safety:

- NewType for domain-specific types (Position, CellContent, etc.)
- Function annotations for parameters and return types
- Immutable data structures with explicit state transitions
- Type checking with mypy (strict settings)

## User Interface

The game provides a simple console-based user interface:

1. The board is displayed as a grid of characters
2. Players enter coordinates to scan (e.g., "3 4")
3. Cells are displayed as:
   - "#" for hidden cells
   - "X" for traps (when revealed)
   - Numbers for cells adjacent to traps
   - " " (space) for empty cells with no adjacent traps

## Program Flow

1. Game initialization:
   - Create board of specified size
   - Randomly place traps (dangers)
   - Calculate adjacent trap counts for each cell

2. Game loop:
   - Display current board state
   - Get player input
   - Scan selected position
   - Check win/lose condition
   - Repeat until game ends

3. Game end:
   - Display final board state
   - Show trap locations (if game is lost)
   - Show congratulations (if game is won)

## Dependencies

### Unit Tests

All unit tests pass successfully, covering:

- Board initialization
- Trap placement
- Cell scanning mechanics
- Auto-expansion logic
- Win condition detection
- Game rendering
