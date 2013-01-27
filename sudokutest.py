import sudoku
import unittest


class TestParseArguments(unittest.TestCase):
    def test_it_parses_arguments(self):
        level_name, board_number = sudoku.parse_arguments(
            ['sudoku.py', 'l33t', '5']
        )
        self.assertEqual(level_name, 'l33t')
        self.assertEqual(board_number, 5)

    def test_it_works_when_missing_board_number(self):
        level_name, board_number = sudoku.parse_arguments(
            ['sudoku.py', 'l33t']
        )
        self.assertEqual(level_name, 'l33t')
        self.assertEqual(board_number, -1)

    def test_it_doesnt_work_when_missing_level_name(self):
        self.assertRaises(
            sudoku.SudokuError,
            sudoku.parse_arguments, ['sudoku.py']
        )


class TestSudokuGameInit(unittest.TestCase):
    def test_it_creates_board_from_file(self):
        boards_file = ("123456789\n" * 9).strip().split('\n')
        game = sudoku.SudokuGame(boards_file)
        self.assertEqual(game.boards, [[range(1, 10)] * 9])

    def test_it_creates_multiple_boards_from_file(self):
        boards_file = ("012345678\n" * 18).strip().split('\n')
        game = sudoku.SudokuGame(boards_file)
        self.assertEqual(game.boards, [[range(0, 9)] * 9] * 2)

    def test_it_doesnt_work_with_wrong_number_of_chars_per_line(self):
        boards_file = ("1234567890\n" * 18).strip().split('\n')
        self.assertRaises(sudoku.SudokuError, sudoku.SudokuGame, boards_file)

    def test_it_doesnt_work_with_wrong_number_of_lines_per_file(self):
        boards_file = ("123456789\n" * 19).strip().split('\n')
        self.assertRaises(sudoku.SudokuError, sudoku.SudokuGame, boards_file)

    def test_it_doesnt_work_with_invalid_chars(self):
        boards_file = ("12345678x\n" * 9).strip().split('\n')
        self.assertRaises(sudoku.SudokuError, sudoku.SudokuGame, boards_file)

if __name__ == '__main__':
    unittest.main()
