import sys


class SudokuError(Exception):
    pass


def parse_arguments(argv):
    if len(argv) == 2:
        return argv[1], -1
    elif len(argv) == 3:
        return argv[1], int(argv[2])
    else:
        raise SudokuError("Wrong number of arguments.")


if __name__ == '__main__':
    try:
        level_name, board_number = parse_arguments(sys.argv)
    except SudokuError:
        print "Usage: python sudoku.py [level name] [board number]"
