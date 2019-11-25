# Installed dependencies
import colorama

# Misc
from mastermind import mastermind_game
from rocks_papers_scissors import rps_game
from snake import snake_game
from tetris import tetris_game
from connect_4 import connect_4_game
from utils import clear_term

colorama.init()

while True:
    clear_term()
    print(
        """< Game List >
1. MasterMind
2. Rocks, Papers, & Scissors
3. Snake
4. Tetris
5. Connect 4

(sth else = quit)"""
    )
    selected_game = input('Enter a game number: ')
    if selected_game == '1':
        mastermind_game()
    elif selected_game == '2':
        rps_game()
    elif selected_game == '3':
        snake_game()
    elif selected_game == '4':
        tetris_game()
    elif selected_game == '5':
        connect_4_game()
    else:
        print('Good Bye...')
        break

colorama.deinit()
