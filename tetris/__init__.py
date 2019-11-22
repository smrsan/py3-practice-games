from tetris.Game import Game


def tetris_game():
    resume = True
    while resume:
        game = Game()
        game.run()
        if game.is_lost:
            user_inpt = input('\nDo u wanna play again? [type "yes"/...]: ')
            resume = user_inpt.lower() == 'yes'
        else:
            # Surely the ESC key is pressed
            break
