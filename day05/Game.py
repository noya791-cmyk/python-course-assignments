import random
#Rock-Paper-Scissors Game
 options = ["rock", "paper", "scissors"]
 computer_choice = random.choice(options)
 pltayer_choice = input("Enter rock, paper, or scissors: ").lower()
    if player_choice == computer_choice:
        print(f"Both chose {player_choice}. It's a tie!")  
    elif (player_choice == "rock" and computer_choice == "scissors") or \
         (player_choice == "paper" and computer_choice == "rock") or \
         (player_choice == "scissors" and computer_choice == "paper"):
        print(f"You chose {player_choice}, computer chose {computer_choice}. You win!")
    else:
        print(f"You chose {player_choice}, computer chose {computer_choice}. You lose!")        






