from re import split
from itertools import chain


class XOGame:
    def __init__(self, dim=3):
        assert dim > 0, 'Невозможно создать поле отрицательной размерности(в нашем мире)'
        self.dim = dim
        self.board = [['_' for _ in range(dim)] for _ in range(dim)]

    def start(self):
        print('Крестики-Нолики Remastered Gold Edition')
        print('В любой момент игры вы можете ввести комманды:')
        print(' help - посмотреть правила игры')
        print(' valid x y - возможно ли сделать такой ход')
        print('Выберите начинающего игрока (Игрок X) и поехали!')
        input('Нажмите Enter...')
        while True:
            self.user_play('X')
            if (w := self.is_winner()) is not None:
                print(f'Player {w} is the winner!' if w != 'Tie' else w)
                self.show_board()
                return w

            self.user_play('O')
            if (w := self.is_winner()) is not None:
                print(f'Player {w} is the winner!' if w != 'Tie' else w)
                self.show_board()
                return w

    def show_board(self, board=None):
        if board is None:
            board = self.board
        l_pad = ' ' * 3
        space_inside = lambda c, lr='': lr + c * (self.dim * 5 - (self.dim-1)) + lr
        row = lambda r: '░  ' + '   '.join(r) + '  ░'
        print()
        print(l_pad * 2, end='')
        for i in range(self.dim):
            print(f'{i}', end=' ' * 3)
        print()
        print(l_pad + space_inside('░', '░'))
        print(l_pad + space_inside(' ', '░'))
        for i in range(self.dim):
            print(f' {i} ', end='')
            print(row(board[i]))
            print(l_pad + space_inside(' ', '░'))
        print(l_pad + space_inside('░', '░'))

    def user_play(self, name):
        print(f'Ход игрока {name}')
        print('Текущее состояние доски:')
        self.show_board()
        x, y = self.is_valid_analyze(self.input())
        self.board[x][y] = name

    def is_winner(self):
        # TODO: Убрать повторения
        # check who is the winner
        # returns winner name(X, O) or None
        if '_' not in list(chain(*self.board)):
            return 'Tie'
        for line in self.board:
            if ''.join(line) == line[0] * self.dim and line[0] != '_':
                return line[0]
        for row_i in range(self.dim):
            row = [line[row_i] for line in self.board]
            if ''.join(row) == row[0] * self.dim and row[0] != '_':
                return row[0]
        leading_diagonal = [row[i] for i, row in enumerate(self.board)]
        if ''.join(leading_diagonal) == leading_diagonal[0] * self.dim and leading_diagonal[0] != '_':
            return leading_diagonal[0]
        opposing_diagonal = [row[-i - 1] for i, row in enumerate(self.board)]
        if ''.join(opposing_diagonal) == opposing_diagonal[0] * self.dim and opposing_diagonal[0] != '_':
            return opposing_diagonal[0]
        return None

    def input(self):
        inp = input('>> ').lower()
        cmds = {
            'help': self.show_help,
            'valid': self.is_valid_user_req
        }
        if inp in cmds.keys():
            cmds[inp]()
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
                    print('Попробуйте снова, введите РОВНО 2 числа')
                    return self.input()
                return inp

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

    def is_valid(self, x, y):
        try:
            return self.board[x][y] == '_'
        except IndexError:
            return None

    def is_valid_analyze(self, t):
        x, y = t
        iv = self.is_valid(x, y)
        if iv:
            return x, y
        elif not iv:
            print('Эта клетка уже занята, попробуйте снова')
        else:
            print('Данной клетки не существует, попробуйте снова')
        return self.is_valid_analyze(self.input())

    def is_valid_user_req(self, x, y):
        iv = self.is_valid(x, y)
        if iv:
            print('Такой ход возможен')
        elif not iv:
            print('Эта клетка уже занята')
        else:
            print('Данной клетки не существует')


if __name__ == '__main__':
    game1 = XOGame(6)
    game1.start()
