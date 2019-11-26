# Misc
from connect_4.Board import Board
from utils import clear_term


class Game:
    def __init__(self):
        self.__frame_delay = .05
        self.is_lost = False
        self.board = Board()
        self.turn = 0

    def run(self):
        while True:
            clear_term()

            self.board.render()
            if self.board.is_full():
                print("It's a Tie!")
                return

            user_n = self.turn + 1
            coin_x = input(f'[User{user_n}] Enter col num or ("q" to exit): ')
            coin_x = coin_x.strip()

            if coin_x == 'q':
                return

            coin_x = int(coin_x) - 1
            if not self.board.is_col_full(coin_x):
                self.board.put_coin(coin_x, self.turn)
                self.next_turn()

    def next_turn(self):
        self.turn = 0 if self.turn else 1
