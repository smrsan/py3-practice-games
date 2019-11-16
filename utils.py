import os
import sys


def get_item_by_index(obj, key_index, default_val='quit'):
    keys_list = list(obj.keys())
    result_key = keys_list[key_index] if 0 <= key_index < len(
        keys_list) else default_val
    result_val = obj.get(result_key, default_val)
    return result_key, result_val


def is_numeric(some_str):
    try:
        int(some_str)
        return True
    except ValueError:
        return False


def clear_term():
    # sys.stderr.write("\x1b[2J\x1b[H")
    # print(chr(27) + "[2J")
    # print("\x1b[2J\x1b[H")
    os.system('cls' if os.name == 'nt' else 'clear')


def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys
        import termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
