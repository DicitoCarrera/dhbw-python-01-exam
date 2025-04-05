# Abandoned Space Station Game

A Minesweeper-like console game set in an abandoned space station where players must scan areas to find safe zones while avoiding hidden dangers.

## Game Overview

In this game, you explore an abandoned space station by scanning different areas. Some areas contain hidden dangers (traps). The objective is to scan all safe areas without triggering any traps.

- When you scan a safe area, you'll see a number indicating how many adjacent areas contain traps
- If you scan an area with a trap, the game ends immediately
- Your goal is to identify all safe areas without triggering any traps

## How to Play

1. Run the game:

   ```
   python src/main.py [width] [height]
   ```

   Where `[width]` and `[height]` are optional parameters to specify the board size (minimum 5x5).

2. When prompted, enter coordinates to scan in the format `x y` (e.g., `3 4`).

3. Continue scanning areas until you've revealed all safe areas or triggered a trap.

4. Enter `q` at any time to quit the game.

## Project Structure

```
dhbw-python-01-exam
├─ .python-version
├─ docs
│  └─ docs.md
├─ LICENSE
├─ main.py
├─ pyproject.toml
├─ README.md
├─ src
│  ├─ Domain.py
│  ├─ GameState.py
│  ├─ initialize_game.py
│  ├─ io_game.py
│  ├─ scan_position.py
│  └─ __init__.py
├─ test
│  ├─ tests.py
│  └─ __init__.py
├─ uv.lock
└─ __init__.py
```

## Development

This project adheres to:

- Functional programming paradigm
- Strong typing with mypy
- Domain-Driven Design principles
- Comprehensive unit testing (75%+ coverage)
- Pylint code quality standards

## Running Tests

To run tests with coverage:

```

cd tests
coverage run -m unittest discover
coverage report -m

```

To run pylint:

```

pylint src/main.py

```

To run mypy type checking:

```

mypy src/main.py

```
