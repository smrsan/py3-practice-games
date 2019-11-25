from connect_4.Game import Game


def connect_4_game():
    resume = True
    while resume:
        game = Game()
        game.run()
        user_inpt = input('\nDo u wanna play again? [type "yes"/...]: ')
        resume = user_inpt.lower() == 'yes'
