import sys
import random

from Tkinter import Tk, Canvas, Frame, BOTH

DEBUG = True
LEVELS = ['debug', 'n00b', 'l33t']
MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9


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


class SudokuUI(Frame):
    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent

        self.row, self.col = -1, -1

        self.initUI()

    def initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, expand=1)
        self.draw_grid()
        self.draw_puzzle()

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)

    def draw_grid(self):
        for i in xrange(10):
            self.canvas.create_line(
                MARGIN + i * SIDE, MARGIN,
                MARGIN + i * SIDE, HEIGHT - MARGIN,
                fill="blue" if i % 3 == 0 else "gray"
            )

            self.canvas.create_line(
                MARGIN, MARGIN + i * SIDE,
                WIDTH - MARGIN, MARGIN + i * SIDE,
                fill="blue" if i % 3 == 0 else "gray"
            )

    def draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in xrange(9):
            for j in xrange(9):
                answer = self.game.answer[i][j]
                original = self.game.puzzle[i][j]
                if answer != 0:
                    self.canvas.create_text(
                        MARGIN + j * SIDE + SIDE / 2,
                        MARGIN + i * SIDE + SIDE / 2,
                        text=answer, tags="numbers",
                        fill="black" if answer == original else "slate gray"
                    )

    def draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            self.canvas.create_rectangle(
                MARGIN + self.col * SIDE + 1,
                MARGIN + self.row * SIDE + 1,
                MARGIN + (self.col + 1) * SIDE - 1,
                MARGIN + (self.row + 1) * SIDE - 1,
                outline="red", tags="cursor"
            )

    def cell_clicked(self, event):
        x, y = event.x, event.y
        if (x > MARGIN and x < WIDTH - MARGIN and
            y > MARGIN and y < HEIGHT - MARGIN):
            self.canvas.focus_set()
            row, col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.puzzle[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.draw_cursor()

    def key_pressed(self, event):
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.answer[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.draw_puzzle()
            self.draw_cursor()
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

        self.puzzle = self.boards[random.randrange(len(self.boards))]
        self.answer = []
        for i in xrange(9):
            self.answer.append([])
            for j in xrange(9):
                self.answer[i].append(self.puzzle[i][j])

    def start(self, board_number):
        if board_number == -1:
            board_number = random.randrange(len(self.boards))
        elif board_number < 0 or board_number >= len(self.boards):
            raise SudokuError(
                "Can't find board number %d" % board_number
            )

        self.puzzle = self.boards[board_number]
        for i in xrange(9):
            self.answer[i] = []
            for j in xrange(9):
                self.answer[i].append(self.puzzle[i][j])


if __name__ == '__main__':
    try:
        level_name, board_number = parse_arguments(sys.argv)
    except SudokuError, e:
        print "Usage: python sudoku.py [level name] [board number]"
        if DEBUG:
            raise e
        else:
            sys.exit(1)

    try:
        with open('%s.sudoku' % level_name, 'r') as boards_file:
            game = SudokuGame(boards_file)
            game.start(board_number)

            root = Tk()
            ui = SudokuUI(root, game)
            root.geometry("%dx%d" % (WIDTH, HEIGHT))
            root.mainloop()
    except SudokuError, e:
        print "Puzzles file is invalid."
        if DEBUG:
            raise e
        else:
            sys.exit(1)
