import sys


class SudokuError(Exception):
    pass


def parse_arguments(argv):
    if len(argv) == 2:
        return argv[1], -1
    else:
        return argv[1], int(argv[2])


if __name__ == '__main__':
    try:
        level_name, board_number = parse_arguments(sys.argv)
    except SudokuError:
        print "Usage: python sudoku.py [level name] [board number]"
