class Player:
    count = 0

    @staticmethod
    def get_player_num():
        Player.count += 1
        return Player.count

    @staticmethod
    def reset_counter():
        Player.count = 0

    def __init__(self, coin_char, turn_num, name=None):
        self.__name = name or f"Player{Player.get_player_num()}"
        self.__coin_char = coin_char
        self.__turn_num = turn_num

    @property
    def name(self):
        return self.__name

    @property
    def coin_char(self):
        return self.__coin_char

    @property
    def turn_num(self):
        return self.__turn_num

    def get_col_num(self):
        coin_x = input(f"[{self.name}] Enter col num ('q' to exit): ")
        coin_x = coin_x.strip()

        if not coin_x.isnumeric():
            if coin_x.lower() == 'q':
                return 'q'
            else:
                return self.get_col_num()

        coin_x = int(coin_x) - 1
        return coin_x
