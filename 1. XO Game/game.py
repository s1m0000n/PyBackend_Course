from re import split
from itertools import chain


class XOGame:
    def __init__(self, dim=3):
        assert dim > 0, 'Невозможно создать поле отрицательной размерности(в нашем мире)'
        self.dim = dim
        self.board = [['_' for _ in range(dim)] for _ in range(dim)]

    # Game Logic
    def start(self):
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

    def play(self, name):
        print(f'Ход игрока {name}\nТекущее состояние доски:')
        self.show_board()
        x, y = self.is_valid(self.input())
        self.board[x][y] = name
        if (w := self.is_winner()) is not None:
            print(f'Player {w} is the winner!' if w != 'Tie' else w)
            self.show_board()
            return w

    # IO
    def input(self):
        # returns (x,y)
        inp = input('>> ').lower()
        if inp == 'help':
            self.show_help()
            return self.input()
        else:
            # parsing input
            try:
                inp = tuple(map(lambda x: int(x), filter(lambda x: x != '', split(r'[;,./:\s]', inp.strip()))))
            except ValueError:
                print('Попробуйте снова, введите 2 числа или комманды help, valid')
                return self.input()
            else:
                if len(inp) != 2:
                    print('Попробуйте снова, введите РОВНО 2 числа или комманды help, valid')
                    return self.input()
                return inp

    def show_board(self, board=None):
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
        print('Правила игры:')
        print('Игроки по очереди ставят на свободные клетки поля n*n знаки (один всегда крестики, другой всегда '
              'нолики).\nПервый, выстроивший в ряд 3 своих фигуры по вертикали, горизонтали или диагонали, '
              'выигрывает.\nПервый ход делает игрок, ставящий крестики.\n')
        print('Как отметить клетку:')
        print(f'x - горизонтальная ось от 0 до {self.dim - 1}')
        print(f'y - вертикальная ось от 0 до {self.dim - 1}')
        print('Возможные варианты записи ответа:\n'
              'x y\n'
              'x, y\n'
              'x,y\n'
              'Вместо , можно использовать символы разделения из набора [;,./:] или просто пробелы')

    # Validation
    def is_winner(self):
        # returns winner literal or None
        if '_' not in list(chain(*self.board)):
            return 'Tie'
        for sequence in [self.board,  # lines
                         [[line[row_i] for line in self.board] for row_i in range(self.dim)],  # rows
                         [[row[i] for i, row in enumerate(self.board)],
                          [row[-i - 1] for i, row in enumerate(self.board)]]]:  # diagonals
            for line in sequence:
                if ''.join(line) == line[0] * self.dim and line[0] != '_':
                    return line[0]
        return None

    def is_valid(self, t):
        try:
            if self.board[t[0]][t[1]] == '_':
                return t[0], t[1]
            else:
                print('Эта клетка уже занята, попробуйте снова')
                return self.is_valid(self.input())
        except IndexError:
            print('Данной клетки не существует, попробуйте снова')
            return self.is_valid(self.input())
