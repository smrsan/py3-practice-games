# Installed dependencies
import colorama

# Misc
from tetris.shapes.Shape import Shape


class IShape(Shape):
    def __init__(self):
        super().__init__()
        self.set_matrix(
            [
                [1],
                [1],
                [1],
                [1]
            ]
        )
        self.color = colorama.Fore.RED + colorama.Style.BRIGHT


class JShape(Shape):
    def __init__(self):
        super().__init__()
        self.set_matrix(
            [
                [0, 1],
                [0, 1],
                [1, 1]
            ]
        )
        self.color = colorama.Fore.GREEN + colorama.Style.BRIGHT


class LShape(Shape):
    def __init__(self):
        super().__init__()
        self.set_matrix(
            [
                [1, 0],
                [1, 0],
                [1, 1]
            ]
        )
        self.color = colorama.Fore.CYAN + colorama.Style.BRIGHT


class OShape(Shape):
    def __init__(self):
        super().__init__()
        self.set_matrix(
            [
                [1, 1],
                [1, 1]
            ]
        )
        self.color = colorama.Fore.YELLOW + colorama.Style.BRIGHT


class SShape(Shape):
    def __init__(self):
        super().__init__()
        self.set_matrix(
            [
                [0, 1, 1],
                [1, 1, 0]
            ]
        )
        self.color = colorama.Fore.MAGENTA + colorama.Style.BRIGHT


class TShape(Shape):
    def __init__(self):
        super().__init__()
        self.set_matrix(
            [
                [1, 1, 1],
                [0, 1, 0]
            ]
        )
        self.color = colorama.Fore.MAGENTA


class ZShape(Shape):
    def __init__(self):
        super().__init__()
        self.set_matrix(
            [
                [1, 1, 0],
                [0, 1, 1]
            ]
        )
        self.color = colorama.Fore.BLUE + colorama.Style.BRIGHT
