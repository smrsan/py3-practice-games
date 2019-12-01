class Board:
    def __init__(self, game, width=7, height=6, win_condition_num=4):
        self.__game = game
        self.__width = width
        self.__height = height
        self.__win_condition_num = win_condition_num
        self.matrix = [
            [] for i in range(self.width)
        ]

    @property
    def game(self):
        return self.__game

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def win_condition_num(self):
        return self.__win_condition_num

    def render(self):
        for i in range(0, self.width):
            if not i:
                print(f"  1", end='')
            else:
                print(f'   {i + 1}', end='')
        print()

        for i in range(0, self.height * 2 + 1):
            for j in range(0, self.width * 2 + 1):
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
                    y = (self.height - 1) - (i - (i // 2) - 1)
                    if self.has_coin(x, y):
                        print(f' {self.get_coin(x, y)} ', end='')
                    else:
                        print('   ', end='')
            print()

    def put_coin(self, x, player_num):
        self.matrix[x].append(player_num)

    def rm_coin(self, x):
        return self.matrix[x].pop()

    def has_coin(self, x, y):
        return y < len(self.matrix[x])

    def get_coin(self, x, y):
        return self.game.players[self.matrix[x][y]].coin_char

    def is_col_full(self, x):
        if x < 0 or x >= self.width:
            return True
        return len(self.matrix[x]) == self.height

    def is_full(self):
        for col in self.matrix:
            if len(col) < self.height:
                return False
        return True

    def get_winner(self):
        # Check Vertical Winners
        for col in self.matrix:
            x_counter = 0
            o_counter = 0
            for cell in col:
                if cell == 0:
                    x_counter += 1
                    o_counter = 0
                    if x_counter == self.win_condition_num:
                        return 0
                else:
                    x_counter = 0
                    o_counter += 1
                    if o_counter == self.win_condition_num:
                        return 1

        # Check Horizontal Winners
        for y in range(self.height):
            x_counter = 0
            o_counter = 0
            for x in range(self.width):
                cell = self.matrix[x][y] if self.has_coin(x, y) else None
                if cell == 0:
                    x_counter += 1
                    o_counter = 0
                    if x_counter == self.win_condition_num:
                        return 0
                elif cell == 1:
                    x_counter = 0
                    o_counter += 1
                    if o_counter == self.win_condition_num:
                        return 1
                else:
                    x_counter = o_counter = 0

        # Check Diagonal Winners
        for z in range(
            max(
                [
                    self.width - self.win_condition_num,
                    self.height - self.win_condition_num
                ]
            )
        ):
            # because of 4 diagonal directions
            x_counter = [0 for i in range(4)]
            o_counter = [0 for i in range(4)]

            x = []
            y = []

            x.append([i for i in range((self.width-1)-z)])
            y.append([i for i in reversed(range(self.height-z))])

            x.append([i for i in range(z+1, self.width)])
            y.append([i for i in range(self.height-1, z-1, -1)])

            x.append([i for i in range(self.width-1, z, -1)])
            y.append(y[0])

            x.append(y[0])
            y.append(y[1])

            for i in range(self.height - z):  # for each calculated x,y
                for j in range(4):  # for each diagonal direction
                    # d = diagonal
                    dx, dy = x[j][i], y[j][i]
                    cell = None

                    if self.has_coin(dx, dy):
                        cell = self.matrix[dx][dy]

                    if cell == 0:
                        x_counter[j] += 1
                        o_counter[j] = 0
                        if x_counter[j] == self.win_condition_num:
                            return 0
                    elif cell == 1:
                        x_counter[j] = 0
                        o_counter[j] += 1
                        if o_counter[j] == self.win_condition_num:
                            return 1
                    else:
                        x_counter[j] = o_counter[j] = 0

        # No one has won the game...
        return -1
