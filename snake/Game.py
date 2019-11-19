from time import sleep
from random import uniform

# Installed dependencies
from pynput.keyboard import Listener, Key
import colorama

# Misc
from snake.Snake import Snake
from snake.Food import Food
from utils import clear_term


class Game:
    def __init__(self):
        self.board_width = 35
        self.board_height = 25
        self.frame_delay = .25
        self.should_exit = False
        self.key_listener = None
        self.snake = Snake(
            board_width=self.board_width,
            board_height=self.board_height
        )
        self.drop_food()
        self.attach_keyboard_events()

    def deinit(self):
        self.dettach_keyboard_events()

    def attach_keyboard_events(self):
        self.key_listener = Listener(
            on_press=on_press(self),
            on_release=on_release(self)
        )
        self.key_listener.start()

    def dettach_keyboard_events(self):
        self.key_listener.stop()

    def run(self):
        while not self.should_exit:
            self.render_board()
            sleep(self.frame_delay)
            self.move_snake()
        self.should_exit = False
        self.deinit()

    def render_board(self):
        clear_term()
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.is_wall(x, y):
                    print('#', end='')
                elif self.is_snake_head(x, y):
                    print(self.snake.color + self.snake.head_char,
                          end=colorama.Style.RESET_ALL)
                elif self.is_snake_body(x, y):
                    print(self.snake.color + self.snake.body_char,
                          end=colorama.Style.RESET_ALL)
                elif self.is_food(x, y):
                    print(self.food.color + self.food.char,
                          end=colorama.Style.RESET_ALL)
                else:
                    print(' ', end='')
                print(' ', end='')
            print()
        print(f"🃟 <Snake Len: {len(self.snake.body_xy) + 1}> - ", end='')
        print(
            f"<Head XY: {{{self.snake.head_xy[0]}, {self.snake.head_xy[1]}}}> - ",
            end=''
        )
        print(f"<Food XY: {{{self.food.xy[0]}, {self.food.xy[1]}}}> 🃟")

    def is_top_wall(self, y):
        return not y

    def is_left_wall(self, x):
        return not x

    def is_bottom_wall(self, y):
        return y == self.board_height - 1

    def is_right_wall(self, x):
        return x == self.board_width - 1

    def is_wall(self, x, y):
        return self.is_top_wall(y) or \
            self.is_left_wall(x) or \
            self.is_bottom_wall(y) or \
            self.is_right_wall(x)

    def is_snake_head(self, x, y):
        return x == self.snake.head_xy[0] and \
            y == self.snake.head_xy[1]

    def is_snake_body(self, x, y):
        for part in self.snake.body_xy:
            if x == part[0] and y == part[1]:
                return True
        return False

    def is_food(self, x, y):
        return x == self.food.xy[0] and \
            y == self.food.xy[1]

    def move_snake(self):
        last_part_xy = self.snake.head_xy[:]

        if self.snake.move_dir == 'up':
            self.snake.head_xy[1] -= 1
        elif self.snake.move_dir == 'down':
            self.snake.head_xy[1] += 1
        elif self.snake.move_dir == 'left':
            self.snake.head_xy[0] -= 1
        elif self.snake.move_dir == 'right':
            self.snake.head_xy[0] += 1

        if self.is_top_wall(self.snake.head_xy[1]):
            self.snake.head_xy[1] = self.board_height - 2
        elif self.is_left_wall(self.snake.head_xy[0]):
            self.snake.head_xy[0] = self.board_width - 2
        elif self.is_bottom_wall(self.snake.head_xy[1]):
            self.snake.head_xy[1] = 1
        elif self.is_right_wall(self.snake.head_xy[0]):
            self.snake.head_xy[0] = 1

        self.snake.body_xy.append(last_part_xy)
        last_part_xy = self.snake.body_xy[0]

        if self.is_food(self.snake.head_xy[0], self.snake.head_xy[1]):
            self.drop_food()
        else:
            self.snake.body_xy.remove(last_part_xy)

    def drop_food(self):
        food_xy = [None, None]
        while True:
            food_xy[0] = int(uniform(1, self.board_width - 2))
            food_xy[1] = int(uniform(1, self.board_height - 2))
            if not self.is_snake_head(food_xy[0], food_xy[1]) and \
                    not self.is_snake_body(food_xy[0], food_xy[1]):
                break
        self.food = Food(food_xy)


def on_press(game):
    def fn(key):
        try:
            key_char = key.char.lower()
            if key_char == 'w':
                game.snake.move_dir = 'up'
            elif key_char == 's':
                game.snake.move_dir = 'down'
            elif key_char == 'a':
                game.snake.move_dir = 'left'
            elif key_char == 'd':
                game.snake.move_dir = 'right'
        except AttributeError:
            if key == Key.up:
                game.snake.move_dir = 'up'
            elif key == Key.down:
                game.snake.move_dir = 'down'
            elif key == Key.left:
                game.snake.move_dir = 'left'
            elif key == Key.right:
                game.snake.move_dir = 'right'
            elif key == Key.esc:
                game.should_exit = True
    return fn


def on_release(game):
    def fn(key):
        pass
    return fn
