from mastermind import mastermind_game
from rocks_papers_scissors import rps_game
from snake import snake_game
from utils import clear_term

while True:
    clear_term()
    print(
        """< Game List >
1. MasterMind
2. Rocks, Papers, & Scissors
3. Snake

(sth else = quit)"""
    )
    selected_game = input('Enter a game number: ')
    if selected_game == '1':
        mastermind_game()
    elif selected_game == '2':
        rps_game()
    elif selected_game == '3':
        snake_game()
    else:
        break

print('Good Bye...')