from random import random


class AiPlayer:
    count = 0

    @staticmethod
    def get_player_num():
        AiPlayer.count += 1
        return AiPlayer.count

    @staticmethod
    def reset_counter():
        AiPlayer.count = 0

    def __init__(self, coin_char, turn_num, game, name=None):
        self.__name = name or f"AiPlayer{AiPlayer.get_player_num()}"
        self.__coin_char = coin_char
        self.__game = game
        self.__turn_num = turn_num

    @property
    def name(self):
        return self.__name

    @property
    def coin_char(self):
        return self.__coin_char

    @property
    def game(self):
        return self.__game

    @property
    def turn_num(self):
        return self.__turn_num

    def get_col_num(self):
        board = self.game.board
        players = self.game.players

        for x in range(board.width):
            # Check if winning is possible
            board.put_coin(x, self.turn_num)
            if board.get_winner() == self.turn_num:
                board.rm_coin(x)
                return x
            board.rm_coin(x)
            # Check if other players would be winner
            for player in players:
                board.put_coin(x, player.turn_num)
                if board.get_winner() == player.turn_num:
                    board.rm_coin(x)
                    return x
                board.rm_coin(x)

        return int(random() * board.width)
