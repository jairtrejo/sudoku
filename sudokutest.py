import sudoku
import unittest


class TestParseArguments(unittest.TestCase):
    def test_it_parses_arguments(self):
        level_name, board_number = sudoku.parse_arguments(
            ['sudoku.py', 'l33t', '5']
        )
        self.assertEqual(level_name, 'l33t')
        self.assertEqual(board_number, 5)


if __name__ == '__main__':
    unittest.main()
