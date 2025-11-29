import random


# Rock-Paper-Scissors Game
options = ["rock", "paper", "scissors"]


def determine_winner(player_choice: str, computer_choice: str) -> str:
    """Return the outcome from the player's perspective: 'tie', 'win' or 'lose'.

    This helper makes the decision logic easy to test.
    """
    player_choice = player_choice.lower()
    computer_choice = computer_choice.lower()

    if player_choice == computer_choice:
        return "tie"
    elif (
        (player_choice == "rock" and computer_choice == "scissors")
        or (player_choice == "paper" and computer_choice == "rock")
        or (player_choice == "scissors" and computer_choice == "paper")
    ):
        return "win"
    else:
        return "lose"


def main() -> None:
    """Interactive play loop for Rock-Paper-Scissors."""
    while True:
        computer_choice = random.choice(options)
        player_choice = input("Enter rock, paper, or scissors: ").lower()

        outcome = determine_winner(player_choice, computer_choice)
        if outcome == "tie":
            print(f"Both chose {player_choice}. It's a tie!")
        elif outcome == "win":
            print(f"You chose {player_choice}, computer chose {computer_choice}. You win!")
        else:
            print(f"You chose {player_choice}, computer chose {computer_choice}. You lose!")

        # Ask to play again
        again = input("Do you want to play again? (yes/no): ").lower()
        if again != "yes":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
