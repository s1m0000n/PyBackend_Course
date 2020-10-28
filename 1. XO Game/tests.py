import unittest
from tic_tac_toe import XOGame


class Init(unittest.TestCase):
    def test_zero_neg_dim_init(self):
        for i in range(0, -2, -1):
            self.assertRaises(AssertionError, XOGame, i)


class IsValid(unittest.TestCase):
    game = XOGame(2)

    def test_check_whether_coords_free(self):
        self.game.board[0][0] = 'X'
        self.assertFalse(self.game.is_valid((0, 0), False))
        self.assertTrue(self.game.is_valid((1, 1), False))

    def test_check_coords_existence(self):
        for pair in ((-10, -10), (-1, -1), (3, 3), (2, 2), (-10, 1), (1, -10), (1, 3), (3, 1)):
            self.assertFalse(self.game.is_valid(pair, False))

    def test_valid_coords(self):
        game = XOGame(2)
        for pair in ((1, 1), (0, 1), (1, 0), (0, 0)):
            self.assertTrue(game.is_valid(pair, True))


class Parsing(unittest.TestCase):
    def test_parsable(self):
        cases = {'1 2': (1, 2), '2, 2': (2, 2), '     0    0      ': (0, 0), '1....1  .': (1, 1), '1/1': (1, 1),
                 '01, 002': (1, 2)}
        for key in cases:
            self.assertEqual(XOGame.parse(key), cases[key])

    def test_one_parsable(self):
        cases = {'12': (12,), '01002': (1002,)}
        for key in cases:
            self.assertEqual(XOGame.parse(key), cases[key])

    # В интерпретаторе всё работает как и планировалось, поднимается ValueError, unittest не отлавливает???
    def test_ValueError(self):
        cases = ('abc', 'a b', 'a, b', '0 a 1', '1_1')
        for s in cases:
            self.assertRaises(ValueError, XOGame.parse, s)


class IsWinner(unittest.TestCase):
    def test_lines_winner(self):
        game = XOGame(3)
        game.board = [['X', 'X', 'X'],
                      ['X', 'X', 'O'],
                      ['_', 'O', 'O']]
        self.assertEqual(game.is_winner(), 'X')
        game.board = [['_', '_', 'O'],
                      ['O', 'O', '_'],
                      ['X', 'X', 'X']]
        self.assertEqual(game.is_winner(), 'X')

    def test_rows_winner(self):
        game = XOGame(3)
        game.board = [['X', 'O', 'X'],
                      ['X', 'O', '_'],
                      ['_', 'O', 'X']]
        self.assertEqual(game.is_winner(), 'O')
        game.board = [['O', 'X', 'X'],
                      ['O', 'X', '_'],
                      ['O', '_', 'X']]
        self.assertEqual(game.is_winner(), 'O')

    def test_diags_winner(self):
        game = XOGame(3)
        game.board = [['X', 'X', 'O'],
                      ['O', 'X', 'O'],
                      ['_', 'O', 'X']]
        self.assertEqual(game.is_winner(), 'X')
        game.board = [['X', 'X', 'O'],
                      ['X', 'O', '_'],
                      ['O', '_', 'X']]
        self.assertEqual(game.is_winner(), 'O')

    def test_None_winner(self):
        game = XOGame(3)
        game.board = [['X', 'X', 'O'],
                      ['O', 'X', 'O'],
                      ['_', '_', '_']]
        self.assertIsNone(game.is_winner())
        game.board = [['X', 'O', 'O'],
                      ['X', 'X', 'O'],
                      ['O', '_', '_']]
        self.assertIsNone(game.is_winner())

    def test_Tie(self):
        game = XOGame(3)
        game.board = [['O', 'X', 'O'],
                      ['X', 'X', 'O'],
                      ['X', 'O', 'X']]
        self.assertEqual(game.is_winner(), 'Tie')


if __name__ == '__main__':
    unittest.main()
