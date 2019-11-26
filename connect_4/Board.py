class Board:
    def __init__(self):
        self.coin_types = ['X', 'O']
        self.matrix = [
            [] for i in range(7)
        ]

    def render(self):
        for i in range(0, 7):
            if not i:
                print(f"  1", end='')
            else:
                print(f'   {i + 1}', end='')
        print()

        for i in range(0, 13):
            for j in range(0, 15):
                is_horizontal = not i or not i % 2
                is_vertical = not j or not j % 2
                if is_horizontal and is_vertical:
                    print('╬', end='')
                elif is_horizontal:
                    print('═══', end='')
                elif is_vertical:
                    print('║', end='')
                else:
                    x = j - (j // 2) - 1
                    y = 5 - (i - (i // 2) - 1)
                    if self.has_coin(x, y):
                        print(f' {self.get_coin(x, y)} ', end='')
                    else:
                        print('   ', end='')
            print()

    def put_coin(self, x, player_num):
        self.matrix[x].append(player_num)

    def has_coin(self, x, y):
        return len(self.matrix[x]) - 1 >= y

    def get_coin(self, x, y):
        return self.coin_types[self.matrix[x][y]]

    def is_col_full(self, x):
        if x < 0 or x > len(self.matrix) - 1:
            return True
        return len(self.matrix[x]) == 6

    def is_full(self):
        for col in self.matrix:
            if len(col) < 6:
                return False
        return True
