from random import random
from utils import get_item_by_index, is_numeric, clear_term


def rps_game():
    elements = {
        'rock': 'scissor',
        'paper': 'rock',
        'scissor': 'paper'
    }
    while True:
        clear_term()
        pc_choice = get_item_by_index(elements, int(random() * 3))
        print("""Which one?
1. rock
2. paper
3. scissor
(sth else = quit)""")
        your_choice = input('Enter the number of your choice: ')

        if not is_numeric(your_choice):
            break

        your_choice = get_item_by_index(elements, int(your_choice) - 1)

        if your_choice[0] == 'quit':
            break

        if your_choice[0] == pc_choice[0]:
            print(f'Equal choices: {your_choice[0]}')
        elif your_choice[1] == pc_choice[0]:
            print(f'You won!!! -> {your_choice[0]} vs {pc_choice[0]}')
        elif pc_choice[1] == your_choice[0]:
            print(f'You lost... -> {your_choice[0]} vs {pc_choice[0]}')

        ans = input('Play again? (type "yes", otherwise anything else...): ')
        if not ans.lower() == 'yes':
            break
