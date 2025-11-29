# Day 05 — Rock, Paper, Scissors

This is a tiny Rock-Paper-Scissors console game implemented as `Game.py`.

## Dependencies

- No external dependencies — only Python's standard library is used (`random`).
- Requires Python 3.6+ (type hints used are compatible with Python 3.6+).

## How to run the game

From the repository root, run:

```powershell
& 'C:/Users/noya7/AppData/Local/Programs/Python/Python313/python.exe' day05\Game.py
```

Or, if `python` is on your PATH:

```powershell
python day05\Game.py
```

The game will prompt you for `rock`, `paper`, or `scissors` and will ask whether you want to play again.

## How to run tests

The repository contains a small test script `test_game.py` that checks the decision logic of the game.

Run the tests with:

```powershell
python day05\test_game.py
```

The script runs a few simple assertions and prints the test results in a compact format.

If you'd like a pytest-style test suite, I can add `pytest`-based tests and a `requirements.txt` entry.
