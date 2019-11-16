import math

# Installed dependencies
import colorama


class Snake:
    def __init__(self, board_width, board_height):
        self.head_xy = [
            math.ceil(board_width / 2),
            math.ceil(board_height / 2)
        ]
        self.body_xy = [
            [
                self.head_xy[0] - 1,
                self.head_xy[1]
            ]
        ]
        self.head_char = 'O'
        self.body_char = 'o'
        self.move_dir = 'right'
        self.color = colorama.Fore.GREEN + colorama.Style.BRIGHT
