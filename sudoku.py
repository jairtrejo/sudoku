import sys

DEBUG = True
LEVELS = ['debug', 'n00b', 'l33t']


class SudokuError(Exception):
    pass


def parse_arguments(argv):
    if len(argv) == 2:
        level_name, board_number = argv[1], -1
    elif len(argv) == 3:
        try:
            level_name, board_number = argv[1], int(argv[2])
            assert board_number >= 0
        except (ValueError, AssertionError):
            raise SudokuError("Board number must be a positive integer.")
    else:
        raise SudokuError("Wrong number of arguments.")

    if level_name not in LEVELS:
        raise SudokuError(
            "Wrong level name. Valid choices are: " + ",".join(LEVELS)
        )

    return level_name, board_number


class SudokuGame(object):
    def __init__(self, boards_file):
        self.boards = [[]]
        for line in boards_file:
            line = line.strip()
            if len(line) != 9:
                self.boards = []
                raise SudokuError(
                    "Each line in the sudoku puzzle must be 9 chars long."
                )
            if len(self.boards[-1]) == 9:
                self.boards.append([])

            self.boards[-1].append([])

            for c in line.strip():
                if c not in "1234567890":
                    raise SudokuError(
                        "Valid characters for a sudoku puzzle must be in 0-9"
                    )
                self.boards[-1][-1].append(int(c))

        if len(self.boards[-1]) != 9:
            self.boards = []
            raise SudokuError(
                "Each sudoku puzzle must be 9 lines long"
            )

if __name__ == '__main__':
    try:
        level_name, board_number = parse_arguments(sys.argv)
    except SudokuError, e:
        print "Usage: python sudoku.py [level name] [board number]"
        if DEBUG:
            print e
