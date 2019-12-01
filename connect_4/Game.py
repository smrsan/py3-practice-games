# Misc
from connect_4.Board import Board
from connect_4.Player import Player
from connect_4.AiPlayer import AiPlayer
from utils import clear_term


class Game:
    def __init__(self):
        self.turn = 0
        self.players = []
        Player.reset_counter()
        AiPlayer.reset_counter()

        has_two_players = input(
            "Do you wanna play with your friend? ['yes'/...]: "
        ).lower() == 'yes'

        if has_two_players:
            self.players.append(
                Player(coin_char='X', turn_num=len(self.players)))
            self.players.append(
                Player(coin_char='O', turn_num=len(self.players)))
        else:
            self.players.append(
                Player(coin_char='X', turn_num=len(self.players)))
            self.players.append(
                AiPlayer(coin_char='O', turn_num=len(self.players), game=self))

        self.board = Board(game=self)

    def run(self):
        while True:
            clear_term()

            self.board.render()

            winner = self.board.get_winner()
            if winner != -1:
                print(f'{self.players[winner].name} has WON the Game!!!')
                return

            if self.board.is_full():
                print("It's a Tie!")
                return

            coin_x = self.players[self.turn].get_col_num()

            if coin_x == 'q':
                return

            if not self.board.is_col_full(coin_x):
                self.board.put_coin(coin_x, self.turn)
                self.next_turn()

    def next_turn(self):
        new_val = self.turn + 1
        self.turn = new_val if new_val < len(self.players) else 0
