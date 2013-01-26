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


if __name__ == '__main__':
    unittest.main()
