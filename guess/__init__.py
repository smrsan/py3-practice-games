from random import random

# Misc
from utils import clear_term


def guess_game():
    resume = True
    while resume:
        clear_term()
        hidden_num = int(random() * 100) - 1
        while True:
            guess_num = input('Guess the hidden num [0-99]: ').strip()
            if not guess_num.isnumeric():
                continue
            guess_num = int(guess_num)
            if guess_num < 0 or guess_num > 99:
                continue

            if guess_num > hidden_num:
                print("It's greater than the hidden num...")
            elif guess_num < hidden_num:
                print("It's less than the hidden num...")
            else:
                print("You WON..!")
                user_inpt = input("Do u wanna play again? ['Yes'/...]: ")
                resume = user_inpt.lower() == 'yes'
                break

        if not resume:
            break
