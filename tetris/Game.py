from time import sleep
from random import random

# Installed dependencies
from pynput.keyboard import Listener, Key
import colorama

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

COMING_DOWN_NORMAL_FRAME_DELAY = .75
COMING_DOWN_SPEED_FRAME_DELAY = .05

RESOLVING_FRAME_DELAY = .05

GRAVITY_FRAME_DELAY = .1


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
        self.coming_down_frame_delay = COMING_DOWN_NORMAL_FRAME_DELAY
        self.coming_down_frame_counter = 1
        self.resolvable_rows = []
        self.resolved_rows = 0
        self.resolving_frame_delay = RESOLVING_FRAME_DELAY
        self.resolving_frame_counter = 1
        self.has_empty_rows = False
        self.gravity_frame_delay = GRAVITY_FRAME_DELAY
        self.gravity_frame_counter = 1
        self.should_rerender = True
        self.time = 0
        self.get_new_hand_shape(True)
        self.attach_keyboard_events()

    def deinit(self):
        self.detach_keyboard_events()
        flush_input()

    @property
    def frame_delay(self):
        return self.__frame_delay

    def get_new_hand_shape(self, init=False):
        random_shape_index = int(random() * len(SHAPE_LIST))
        new_shape = SHAPE_LIST[random_shape_index]()
        new_shape.xy[0] = int(self.board_width / 2 - new_shape.width / 2)
        new_shape.xy[1] = 1 if init else 0
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

            if self.should_animate_coming_down():
                if not self.hand_shape:
                    self.get_new_hand_shape()
                self.animate_coming_down()

            elif self.should_animate_resolving():
                self.animate_resolving()

            elif self.should_animate_gravity():
                self.animate_gravity()

            sleep(self.frame_delay)

            self.time += self.frame_delay
            if not self.time % 1:
                self.should_rerender = True
        self.deinit()

    def render_board(self):
        if not self.should_rerender:
            return
        clear_term()
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.is_wall(x, y):
                    self.draw_wall(x, y)

                elif self.hand_shape and self.hand_shape.is_shape(x, y):
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

        status = f'\nElapsed Time: {self.get_formated_time()}'
        status += f'\nResolved Rows: {self.resolved_rows}'
        print(status)
        self.should_rerender = False

    def get_formated_time(self):
        mins = int(self.time // 60)
        secs = int(self.time % 60)

        mins = f'0{mins}' if mins < 10 else mins
        secs = f'0{secs}' if secs < 10 else secs

        return f'{mins}:{secs}'

    def should_animate_coming_down(self):
        if self.resolvable_rows or self.has_empty_rows:
            return False
        if self.coming_down_frame_counter * self.frame_delay >= self.coming_down_frame_delay:
            self.coming_down_frame_counter = 1
            return True
        self.coming_down_frame_counter += 1
        return False

    def animate_coming_down(self):
        self.should_rerender = True
        if self.can_go_down():
            self.hand_shape.go_down()
        else:
            self.put_shape()
            self.get_resolvable_rows()

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
        self.hand_shape = None

    def should_animate_resolving(self):
        if not self.resolvable_rows:
            return False
        if self.resolving_frame_counter * self.frame_delay >= self.resolving_frame_delay:
            self.resolving_frame_counter = 1
            return True
        self.resolving_frame_counter += 1
        return False

    def animate_resolving(self):
        self.should_rerender = True
        min_y = self.resolvable_rows[0]
        if not self.has_board_row(min_y):
            self.resolvable_rows.clear()
            self.resolving_frame_counter = 1
            self.resolved_rows += 1
            self.check_middle_empty_rows()
            return
        min_x = min(self.board_blocks[min_y].keys())
        for y in self.resolvable_rows:
            self.del_board_block(min_x, y)

    def get_resolvable_rows(self):
        resolvable_rows = []
        for y in self.board_blocks.keys():
            if len(self.board_blocks[y]) == self.board_width - 2:
                resolvable_rows.append(y)
        self.resolvable_rows = resolvable_rows

    def check_middle_empty_rows(self):
        prev_y = None
        latest_y = None

        for y in self.board_blocks.keys():
            latest_y = y
            if prev_y == None:
                prev_y = y
                continue
            if y - prev_y > 1:
                self.has_empty_rows = True
                return

        if latest_y != None and not self.is_bottom_wall(latest_y + 1):
            self.has_empty_rows = True
            return

        self.has_empty_rows = False

    def should_animate_gravity(self):
        if not self.has_empty_rows:
            return False
        if self.gravity_frame_counter * self.frame_delay >= self.gravity_frame_delay:
            self.gravity_frame_counter = 1
            return True
        self.gravity_frame_counter += 1
        return False

    def animate_gravity(self):
        self.should_rerender = True
        animated_rows_count = 0
        for y in reversed(sorted(self.board_blocks.keys())):
            next_row_y = y + 1
            if not self.is_bottom_wall(next_row_y) and not self.has_board_row(next_row_y):
                self.board_blocks[next_row_y] = self.board_blocks[y].copy()
                del self.board_blocks[y]
                animated_rows_count += 1
        if not animated_rows_count:
            self.has_empty_rows = False

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
        if not self.has_board_row(y):
            return None
        return self.board_blocks[y].get(x, None)

    def set_board_block(self, x, y, color):
        if not self.has_board_row(y):
            self.board_blocks[y] = dict()
        self.board_blocks[y][x] = color

    def del_board_block(self, x, y):
        if not self.has_board_row(y):
            return
        if not self.has_board_block(x, y):
            return
        del self.board_blocks[y][x]

        if not len(self.board_blocks[y]):
            del self.board_blocks[y]

    def has_board_row(self, y):
        return self.board_blocks.get(y, None) != None

    def has_board_block(self, x, y):
        if not self.has_board_row(y):
            return False
        return self.board_blocks[y].get(x, None) != None

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
        if not self.hand_shape:
            return False
        result = True
        self.hand_shape.go_left()
        (shape_x, shape_y) = self.hand_shape.xy
        if self.has_overlapped_blocks(self.hand_shape) or \
                self.is_left_wall(shape_x):
            result = False
        self.hand_shape.go_right()
        return result

    def can_go_right(self):
        if not self.hand_shape:
            return False
        result = True
        self.hand_shape.go_right()
        (shape_x, shape_y) = self.hand_shape.xy
        if self.has_overlapped_blocks(self.hand_shape) or \
                self.is_right_wall(shape_x + self.hand_shape.width - 1):
            result = False
        self.hand_shape.go_left()
        return result

    def can_go_down(self):
        if not self.hand_shape:
            return False
        result = True
        self.hand_shape.go_down()
        (shape_x, shape_y) = self.hand_shape.xy
        if self.has_overlapped_blocks(self.hand_shape) or \
                self.is_bottom_wall(shape_y + self.hand_shape.height - 1):
            result = False
        self.hand_shape.go_up()
        return result

    def can_rotate_left(self):
        if not self.hand_shape:
            return False
        result = True
        self.hand_shape.rotate_left()
        (shape_x, shape_y) = self.hand_shape.xy
        shape_width = self.hand_shape.width
        shape_height = self.hand_shape.height
        if self.has_overlapped_blocks(self.hand_shape) or \
                shape_x + shape_width >= self.board_width or \
                shape_y + shape_height >= self.board_height:
            result = False
        self.hand_shape.rotate_right()
        return result

    def can_rotate_right(self):
        if not self.hand_shape:
            return False
        result = True
        self.hand_shape.rotate_right()
        (shape_x, shape_y) = self.hand_shape.xy
        shape_width = self.hand_shape.width
        shape_height = self.hand_shape.height
        if self.has_overlapped_blocks(self.hand_shape) or \
                shape_x + shape_width >= self.board_width or \
                shape_y + shape_height >= self.board_height:
            result = False
        self.hand_shape.rotate_left()
        return result

    def speed_up(self):
        self.coming_down_frame_delay = COMING_DOWN_SPEED_FRAME_DELAY

    def slow_down(self):
        self.coming_down_frame_delay = COMING_DOWN_NORMAL_FRAME_DELAY

    def end(self):
        self.should_exit = True


def on_press(game):
    def fn(key):
        try:
            key_char = key.char.lower()
            if key_char in 'wad':
                if key_char == 'w' and game.can_rotate_right():
                    game.hand_shape.rotate_right()
                elif key_char == 'a' and game.can_go_left():
                    game.hand_shape.go_left()
                elif key_char == 'd' and game.can_go_right():
                    game.hand_shape.go_right()
                game.should_rerender = True
            elif key_char == 's':
                game.speed_up()
        except AttributeError:
            if key in [Key.up, Key.left, Key.right]:
                if key == Key.up and game.can_rotate_right():
                    game.hand_shape.rotate_right()
                elif key == Key.left and game.can_go_left():
                    game.hand_shape.go_left()
                elif key == Key.right and game.can_go_right():
                    game.hand_shape.go_right()
                game.should_rerender = True
            elif key == Key.down:
                game.speed_up()
            elif key == Key.esc:
                game.end()

    return fn


def on_release(game):
    def fn(key):
        game.slow_down()
    return fn
