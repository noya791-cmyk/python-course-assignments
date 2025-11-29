#!/usr/bin/env python3
"""Test script for the simple Rock-Paper-Scissors game."""

from Game import determine_winner


def test_tie():
    try:
        assert determine_winner("rock", "rock") == "tie"
        assert determine_winner("paper", "paper") == "tie"
        assert determine_winner("scissors", "scissors") == "tie"
        print("✓ PASS: tie outcomes")
        return True
    except AssertionError as e:
        print(f"✗ FAIL: tie outcomes - {e}")
        return False


def test_win():
    try:
        assert determine_winner("rock", "scissors") == "win"
        assert determine_winner("paper", "rock") == "win"
        assert determine_winner("scissors", "paper") == "win"
        print("✓ PASS: win outcomes")
        return True
    except AssertionError as e:
        print(f"✗ FAIL: win outcomes - {e}")
        return False


def test_lose():
    try:
        assert determine_winner("rock", "paper") == "lose"
        assert determine_winner("paper", "scissors") == "lose"
        assert determine_winner("scissors", "rock") == "lose"
        print("✓ PASS: lose outcomes")
        return True
    except AssertionError as e:
        print(f"✗ FAIL: lose outcomes - {e}")
        return False


def main():
    print("=" * 60)
    print("Game tests for day05: Rock-Paper-Scissors")
    print("=" * 60)
    print()

    tests = [
        ("Tie outcomes", test_tie),
        ("Win outcomes", test_win),
        ("Lose outcomes", test_lose),
    ]

    results = []
    for name, fn in tests:
        print(f"\n{name}:")
        print("-" * 60)
        results.append(fn())

    print()
    print("=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    return all(results)


if __name__ == "__main__":
    import sys

    sys.exit(0 if main() else 1)

