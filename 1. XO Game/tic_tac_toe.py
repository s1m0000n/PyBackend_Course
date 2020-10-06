"""This module is a Tic Tac Toe terminal game for 2 players, nothing really special.
 To use it, simply import XOGame, use default constructor
 to initialize it with an int n or nothing, the default is the classic 3*3 board.
 Then use .start() to start playing! Example:
 from tic_tac_toe import XOGame
 XOGame(5).start()"""
from itertools import chain
from re import split


class XOGame:
    """Class for the game Tic Tac Toe on any n*n field"""

    def __init__(self, dim=3):
        assert dim > 0, 'Невозможно создать поле отрицательной или ' \
                        'нулевой размерности(в нашем мире)'
        self.dim = dim
        self.board = [['_' for _ in range(dim)] for _ in range(dim)]

    # Game Logic
    def start(self):
        """Game cycle controller"""
        print('Крестики-Нолики Remastered Gold Edition\n'
              'В любой момент игры вы можете ввести комманды:\n'
              '   help - посмотреть правила игры\n'
              '   valid x y - возможно ли сделать такой ход\n'
              'Выберите начинающего игрока (Игрок X) и поехали!\n')
        input('Нажмите Enter...')
        while True:
            if self.play('X') is not None:
                return
            if self.play('O') is not None:
                return

    def play(self, player_name):
        """Game logic for each one user turn
        Args:
            player_name -- name of current player
        Returns:
            Winner's name or None"""
        print(f'Ход игрока {player_name}\nТекущее состояние доски:')
        self.show_board()
        coords = self.is_valid(self.input())
        self.board[coords[0]][coords[1]] = player_name
        if (winner := self.is_winner()) is not None:
            print(f'Player {winner} is the winner!' if winner != 'Tie' else winner)
            self.show_board()
            return winner
        return None

    # IO
    def input(self):
        """Reads and parses user input
        Returns:
            coordinates tuple (x, y)"""
        inp = input('>> ').lower()
        if inp == 'help':
            self.show_help()
            return self.input()
        elif inp == 'quit':
            quit()
        else:
            # parsing input
            try:
                parsed = self.parse(inp)
            except ValueError:
                print('Попробуйте снова, введите 2 числа или комманды help или quit')
                return self.input()
            else:
                if len(parsed) != 2:
                    print('Попробуйте снова, введите РОВНО 2 числа или комманды help или quit')
                    return self.input()
                return parsed

    def show_board(self, board=None):
        """Prints boards & coordinate indices using ASCII
        Args:
            board -- self.board by default, expects [[]]
        Returns:
            nothing"""
        if board is None:
            board = self.board

        l_pad = ' ' * 3
        space_inside = lambda c, lr='': lr + c * (self.dim * 5 - (self.dim - 1)) + lr
        row = lambda r: '░  ' + '   '.join(r) + '  ░'

        print('\n' + l_pad * 2, end='')
        for i in range(self.dim):
            print(f'{i}', end=' ' * 3)
        print('\n' + l_pad + space_inside('░', '░') + '\n' + l_pad + space_inside(' ', '░'))
        for i in range(self.dim):
            print(f' {i} {row(board[i])}\n' + l_pad + space_inside(' ', '░'))
        print(l_pad + space_inside('░', '░'))

    def show_help(self):
        """Prints rules of the game and expected input format
        Returns:
            nothing"""
        print('Правила игры:\n'
              'Игроки по очереди ставят на свободные клетки поля n*n знаки '
              '(один всегда крестики, другой всегда нолики).\n'
              'Первый, выстроивший в ряд 3 своих фигуры по вертикали, горизонтали или диагонали, '
              'выигрывает.\nПервый ход делает игрок, ставящий крестики.\n'
              'Как отметить клетку:\n'
              f'x - горизонтальная ось от 0 до {self.dim - 1}\n'
              f'y - вертикальная ось от 0 до {self.dim - 1}\n'
              'Возможные варианты записи ответа:\n'
              '     x y\n'
              '     x, y\n'
              '     x,y\n'
              'Вместо , можно использовать символы разделения из набора [;,./:] или просто пробелы')

    # Validation&Parsing
    @staticmethod
    def parse(raw_text):
        """Parses raw input
        Returns:
            (int,)"""
        return tuple(map(lambda x: int(x),
                         filter(lambda x: x != '',
                                split(r'[;,./:\s]', raw_text.strip()))))

    def is_winner(self):
        """Returns:
            winner name: 'X', 'O' or None"""
        if '_' not in list(chain(*self.board)):
            return 'Tie'
        for sequence in [self.board,  # lines
                         [[line[i] for line in self.board] for i in range(self.dim)],  # rows
                         [[row[i] for i, row in enumerate(self.board)],
                          [row[-i - 1] for i, row in enumerate(self.board)]]]:  # diagonals
            for line in sequence:
                if ''.join(line) == line[0] * self.dim and line[0] != '_':
                    return line[0]
        return None

    def is_valid(self, coords, recursive=True):
        """Checking whether given coordinates are valid and free.
        Recursively calls self.is_valid(self.input()),
         if the coords aren't valid, prints the reason.
         Args:
             coords -- tuple of 2 (x,y) int coordinates
         Returns:
              x,y -- unpacked coordinates"""
        if coords[0] < 0 or coords[1] < 0:
            print('Данной клетки не существует, попробуйте снова')
            return self.is_valid(self.input()) if recursive else False
        try:
            if self.board[coords[0]][coords[1]] == '_':
                return coords[0], coords[1] if recursive else True
            else:
                print('Эта клетка уже занята, попробуйте снова')
                return self.is_valid(self.input()) if recursive else False
        except IndexError:
            print('Данной клетки не существует, попробуйте снова')
            return self.is_valid(self.input()) if recursive else False
