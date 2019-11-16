# Installed dependencies
import colorama


class Food:
    def __init__(self, xy):
        self.xy = xy[:]
        self.color = colorama.Fore.RED + colorama.Style.BRIGHT
        self.char = 'X'
