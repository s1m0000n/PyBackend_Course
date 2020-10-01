from re import split
from copy import copy


class XOGame:
    def __init__(self, dim=3):
        assert dim > 0, 'Невозможно создать поле отрицательной размерности(в нашем мире)'
        self.dim = dim
        self.board = [['_' for _ in range(dim)] for _ in range(dim)]

    @staticmethod
    def choose(options):
        for i, v in enumerate(options):
            print(f'{i + 1}. {v}')
        answer = input('Введите ваш ответ: ')
        try:
            answer = int(answer)
        except ValueError:
            print('Невозможно выбрать такой ответ, введите число. Попробуйте снова.')
            return XOGame.choose(options)
        else:
            if answer > len(options) or answer <= 0:
                print('Невозможно выбрать такой ответ, попробуйте снова')
                return XOGame.choose(options)
            return answer

    def start(self):
        print('Крестики-Нолики Remastered Gold Edition')
        print('В любой момент игры вы можете ввести комманды:')
        print(' help - посмотреть правила игры')
        print(' valid x y - возможно ли сделать такой ход')
        print('Выберите режим игры:')
        if self.choose(('С компьютером(он сегодня злой)', 'Вдвоём')) == 1:
            self.with_computer()
        else:
            self.two_players()

    def with_computer(self):
        pass

    def show_board(self, board = None):
        if board is None:
            board = self.board
        l_pad = ' ' * 3
        space_inside = lambda c, lr='': lr + c * (self.dim * 5 - 2) + lr
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
        temp = copy(self.board)
        temp[x][y] = name
        print('Состояние доски после вашего хода')
        self.show_board(temp)

        if self.choose(('Подтвердить ход', 'Изменить ход')) == 2:
            # TODO: fix this!
            # Troubles with changing choice
            temp = self.board
            self.user_play(name)
        else:
            self.board = temp

    def two_players(self):
        print('Выберите начинающего игрока (Игрок X) и поехали!')
        input('Нажмите Enter...')
        # checking for winners
        while True:
            self.user_play('X')
            self.is_winner()
            self.user_play('O')
            self.is_winner()

    def is_winner(self):
        # check who is the winner
        pass
        # return winner name(X, O) or None


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
        x,y = t
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
    game1 = XOGame(3)
    game1.start()
