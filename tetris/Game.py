from time import sleep
from random import random
import colorama

# Installed dependencies
from pynput.keyboard import Listener, Key

# Misc
from utils import flush_input, clear_term
from tetris import shapes

SHAPE_LIST = (
    shapes.IShape,
    shapes.JShape,
    shapes.LShape,
    shapes.OShape,
    shapes.SShape,
    shapes.TShape,
    shapes.ZShape
)

GRAVITY_NORMAL_FRAME_DELAY = .75
GRAVITY_SPEED_FRAME_DELAY = .05


class Game:
    def __init__(self):
        self.board_blocks = dict()
        self.board_width = 15
        self.board_height = 20
        self.__frame_delay = .05
        self.should_exit = False
        self.is_lost = False
        self.key_listener = None
        self.hand_shape = None
        self.gravity_frame_delay = GRAVITY_NORMAL_FRAME_DELAY
        self.gravity_frame_counter = 1
        self.get_new_hand_shape()
        self.attach_keyboard_events()

    def deinit(self):
        self.detach_keyboard_events()
        flush_input()

    @property
    def frame_delay(self):
        return self.__frame_delay

    def get_new_hand_shape(self):
        random_shape_index = int(random() * len(SHAPE_LIST))
        new_shape = SHAPE_LIST[random_shape_index]()
        new_shape.xy[0] = int(self.board_width / 2 - new_shape.width / 2)
        new_shape.xy[1] = 1
        self.hand_shape = new_shape

    def attach_keyboard_events(self):
        self.key_listener = Listener(
            on_press=on_press(self),
            on_release=on_release(self)
        )
        self.key_listener.start()

    def detach_keyboard_events(self):
        self.key_listener.stop()

    def run(self):
        while not self.should_exit:
            self.render_board()
            if self.should_animate_gravity():
                if not self.can_go_down():
                    self.put_shape()
                else:
                    self.hand_shape.go_down()
            sleep(self.frame_delay)
        self.deinit()

    def render_board(self):
        clear_term()
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.is_wall(x, y):
                    self.draw_wall(x, y)

                elif self.hand_shape.is_shape(x, y):
                    print(
                        self.hand_shape.color + '▓▓',
                        end=colorama.Style.RESET_ALL
                    )

                elif not self.is_empty_board_block(x, y):
                    print(
                        self.get_board_block(x, y) + '▓▓',
                        end=colorama.Style.RESET_ALL
                    )

                else:
                    print('  ', end='')
            print()

    def put_shape(self):
        (shape_x, shape_y) = self.hand_shape.xy

        for y in range(self.hand_shape.height):
            for x in range(self.hand_shape.width):
                if self.hand_shape.is_colored_block(x, y):
                    self.set_board_block(
                        x + shape_x,
                        y + shape_y,
                        self.hand_shape.color
                    )
        self.get_new_hand_shape()

    def is_empty_board_block(self, x, y):
        return self.get_board_block(x, y) == None

    def has_overlapped_blocks(self, shape):
        (shape_x, shape_y) = self.hand_shape.xy

        for y in range(self.hand_shape.height):
            for x in range(self.hand_shape.width):
                if self.hand_shape.is_colored_block(x, y) and \
                        self.get_board_block(x + shape_x, y + shape_y):
                    return True

        return False

    def get_board_block(self, x, y):
        return self.board_blocks.get(f'{x}:{y}', None)

    def set_board_block(self, x, y, color):
        self.board_blocks[f'{x}:{y}'] = color

    def draw_wall(self, x, y):
        if self.is_top_wall(y):
            if self.is_left_wall(x):
                print('╔', end='')
            elif self.is_right_wall(x):
                print('╗', end='')
            else:
                print('══', end='')
        elif self.is_bottom_wall(y):
            if self.is_left_wall(x):
                print('╚', end='')
            elif self.is_right_wall(x):
                print('╝', end='')
            else:
                print('══', end='')
        elif self.is_left_wall(x) or self.is_right_wall(x):
            print('║', end='')

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

    def can_go_left(self):
        result = True
        self.hand_shape.go_left()
        (shape_x, shape_y) = self.hand_shape.xy
        if self.has_overlapped_blocks(self.hand_shape) or \
                self.is_left_wall(shape_x):
            result = False
        self.hand_shape.go_right()
        return result

    def can_go_right(self):
        result = True
        self.hand_shape.go_right()
        (shape_x, shape_y) = self.hand_shape.xy
        if self.has_overlapped_blocks(self.hand_shape) or \
                self.is_right_wall(shape_x + self.hand_shape.width - 1):
            result = False
        self.hand_shape.go_left()
        return result

    def can_go_down(self):
        result = True
        self.hand_shape.go_down()
        (shape_x, shape_y) = self.hand_shape.xy
        if self.has_overlapped_blocks(self.hand_shape) or \
                self.is_bottom_wall(shape_y + self.hand_shape.height - 1):
            result = False
        self.hand_shape.go_up()
        return result

    def should_animate_gravity(self):
        if self.gravity_frame_counter * self.frame_delay >= self.gravity_frame_delay:
            self.gravity_frame_counter = 1
            return True
        self.gravity_frame_counter += 1
        return False

    def can_rotate_left(self):
        result = True
        self.hand_shape.rotate_left()
        (shape_x, shape_y) = self.hand_shape.xy
        shape_width = self.hand_shape.width
        shape_height = self.hand_shape.height
        if self.has_overlapped_blocks(self.hand_shape) or \
                self.is_wall(shape_x + shape_width - 1, shape_y + shape_height - 1):
            result = False
        self.hand_shape.rotate_right()
        return result

    def can_rotate_right(self):
        result = True
        self.hand_shape.rotate_right()
        (shape_x, shape_y) = self.hand_shape.xy
        shape_width = self.hand_shape.width
        shape_height = self.hand_shape.height
        if self.has_overlapped_blocks(self.hand_shape) or \
                self.is_wall(shape_x + shape_width - 1, shape_y + shape_height - 1):
            result = False
        self.hand_shape.rotate_left()
        return result

    def speed_up(self):
        self.gravity_frame_delay = GRAVITY_SPEED_FRAME_DELAY

    def slow_down(self):
        self.gravity_frame_delay = GRAVITY_NORMAL_FRAME_DELAY

    def end(self):
        self.should_exit = True


def on_press(game):
    def fn(key):
        try:
            key_char = key.char.lower()
            if key_char == 'w' and game.can_rotate_right():
                game.hand_shape.rotate_right()
            elif key_char == 'a' and game.can_go_left():
                game.hand_shape.go_left()
            elif key_char == 'd' and game.can_go_right():
                game.hand_shape.go_right()
            elif key_char == 's':
                game.speed_up()
        except AttributeError:
            if key == Key.up and game.can_rotate_right():
                game.hand_shape.rotate_right()
            elif key == Key.left and game.can_go_left():
                game.hand_shape.go_left()
            elif key == Key.right and game.can_go_right():
                game.hand_shape.go_right()
            elif key == Key.down:
                game.speed_up()
            elif key == Key.esc:
                game.end()

    return fn


def on_release(game):
    def fn(key):
        game.slow_down()
    return fn
