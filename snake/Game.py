from time import sleep
from random import uniform

# Installed dependencies
from pynput.keyboard import Listener, Key
import colorama

# Misc
from snake.Snake import Snake
from snake.Food import Food
from utils import clear_term, flush_input


NORMAL_FRAME_DELAY = .25
SPEED_FRAME_DELAY = .05


class Game:
    def __init__(self):
        self.board_width = 35
        self.board_height = 25
        self.frame_delay = NORMAL_FRAME_DELAY
        self.should_exit = False
        self.is_lost = False
        self.key_listener = None
        self.snake = Snake(
            board_width=self.board_width,
            board_height=self.board_height
        )
        self.food = Food(self.snake.head_xy)
        self.drop_food()
        self.attach_keyboard_events()

    def deinit(self):
        self.detach_keyboard_events()

    def attach_keyboard_events(self):
        self.key_listener = Listener(
            on_press=on_press(self),
            on_release=on_release(self)
        )
        self.key_listener.start()

    def detach_keyboard_events(self):
        self.key_listener.stop()
        flush_input()

    def run(self):
        while not self.should_exit:
            self.render_board()
            if self.is_snake_body(self.snake.head_xy[0], self.snake.head_xy[1]):
                self.should_exit = self.is_lost = True
            else:
                sleep(self.frame_delay)
                self.move_snake()
        self.deinit()

    def render_board(self):
        clear_term()
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.is_wall(x, y):
                    self.draw_wall(x, y)
                    continue

                if self.is_snake_head(x, y):
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

    def draw_wall(self, x, y):
        if self.is_top_wall(y):
            if self.is_left_wall(x):
                print(' ', end='╔')
            elif self.is_right_wall(x):
                print('╗', end=' ')
            else:
                print('═', end='═')
        elif self.is_bottom_wall(y):
            if self.is_left_wall(x):
                print(' ', end='╚')
            elif self.is_right_wall(x):
                print('╝', end=' ')
            else:
                print('═', end='═')
        elif self.is_left_wall(x):
            print(' ', end='║')
        elif self.is_right_wall(x):
            print('║', end=' ')

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
        return [x, y] == self.snake.head_xy

    def is_snake_body(self, x, y):
        return [x, y] in self.snake.body_xy

    def is_food(self, x, y):
        return [x, y] == self.food.xy

    def move_snake(self):
        last_head_xy = self.snake.head_xy[:]

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

        self.snake.body_xy.append(last_head_xy)

        if self.is_food(self.snake.head_xy[0], self.snake.head_xy[1]):
            self.drop_food()
        else:
            self.snake.body_xy.remove(self.snake.body_xy[0])

    def drop_food(self):
        food_xy = self.food.xy
        while self.is_snake_head(food_xy[0], food_xy[1]) or \
                self.is_snake_body(food_xy[0], food_xy[1]):
            food_xy[0] = int(uniform(1, self.board_width - 2))
            food_xy[1] = int(uniform(1, self.board_height - 2))
        self.food = Food(food_xy)

    def speed_up(self):
        self.frame_delay = SPEED_FRAME_DELAY

    def slow_down(self):
        self.frame_delay = NORMAL_FRAME_DELAY


def on_press(game):
    def fn(key):
        current_dir = game.snake.move_dir
        new_dir = None
        try:
            key_char = key.char.lower()
            if key_char == 'w' and current_dir != 'down':
                new_dir = 'up'
            elif key_char == 's' and current_dir != 'up':
                new_dir = 'down'
            elif key_char == 'a' and current_dir != 'right':
                new_dir = 'left'
            elif key_char == 'd' and current_dir != 'left':
                new_dir = 'right'
        except AttributeError:
            if key == Key.up and current_dir != 'down':
                new_dir = 'up'
            elif key == Key.down and current_dir != 'up':
                new_dir = 'down'
            elif key == Key.left and current_dir != 'right':
                new_dir = 'left'
            elif key == Key.right and current_dir != 'left':
                new_dir = 'right'
            elif key == Key.esc:
                game.should_exit = True

        if current_dir == new_dir:
            game.speed_up()
        elif new_dir != None:
            game.snake.move_dir = new_dir

    return fn


def on_release(game):
    def fn(key):
        game.slow_down()
    return fn
