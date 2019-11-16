# Installed dependencies
import colorama

# Misc
from mastermind import mastermind_game
from rocks_papers_scissors import rps_game
from snake import snake_game
from utils import clear_term, flush_input

colorama.init()

while True:
    clear_term()
    print(
        """< Game List >
1. MasterMind
2. Rocks, Papers, & Scissors
3. Snake

(sth else = quit)"""
    )
    flush_input()
    selected_game = input('Enter a game number: ')
    if selected_game == '1':
        mastermind_game()
    elif selected_game == '2':
        rps_game()
    elif selected_game == '3':
        snake_game()
    else:
        print('Good Bye...')
        break

colorama.deinit()
