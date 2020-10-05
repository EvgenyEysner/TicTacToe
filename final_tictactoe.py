# Крестики-нолики
import random

# Вывожу на экран  иснтрукцию для игрока
def playInstruct():
    print(
        '''
    Добро пожаловать в игру Крестики-нолики!
    С Вами  будет сражаться компьютер.
    Что бы сделать свой ход, введите цифру от 1 до 9.
    Числа соответсвуют клавишам на клавиатуре:
    7 | 8 | 9
    ---------
    4 | 5 | 6
    ---------
    1 | 2 | 3
    Приготовьтесь к эпическому сражению с ИИ!\n
        ''')


def playboard(board):
# Эта функция выводит на экран игровое поле, клетки которого будут заполняться.
# "board" — это список из 10 строк, для прорисовки игрового поля (индекс 0 игнорируется).
    print(board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('-' * 10)
    print(board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('-' * 10)
    print(board[1] + ' | ' + board[2] + ' | ' + board[3])


def play_token():   # Разрешение игроку ввести букву, которую он выбирает.
    token = ''
    while not (token == 'Х' or token == 'О'):
        print('Вы выбираете Х или О?')
        token = input().upper()
        # Возвращает список, в котором буква игрока — первый элемент, а буква компьютера — второй.
        if token == 'Х':
            return ['Х', 'О']
        else:
            return ['О', 'Х']


def who_is_first():     # Случайный выбор игрока, который ходит первым.
    if random.randint(0, 1) == 0:
        return 'Компьютер'
    else:
        return 'Человек'


def make_move(board, token, move):  # Размещение меток на игровом поле, где token это X или O
    board[move] = token


def check_the_winner(board, token):  # Учитывая заполнение игрового поля и буквы игрока, выводим победителя
    # выиграшные варианты которые перебираю по 3 клетки
    win_options = ((7, 8, 9), (4, 5, 6), (1, 2, 3), (7, 4, 1), (8, 5, 2), (9, 6, 3), (7, 5, 3), (9, 5, 1))
    for i in win_options:
        if board[i[0]] == board[i[1]] == board[i[2]] == token:
            winner = board[i[0]]    # если какие-то 3 клетки совпадают выводим победителя
            return winner
        if ' ' not in board:
            return 'Ничья'  # если свободных клеток нет
    return None


def new_playboard(board):   # Создает копию игрового поля и возвращает его, нужна для логики ИИ
    new_board = []
    for i in board:
        new_board.append(i)
    return new_board


def check_free_space(board, move):  # Возвращает True, если сделан ход в свободную клетку.
    return board[move] == ' '


def player_move(board):  # Разрешение игроку сделать ход.
    move = None
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not check_free_space(board, int(move)):
        print('Ваш следующий ход? (1-9)')
        move = input()
    return int(move)


# Возвращает допустимый ход, учитывая список сделанных ходов и список заполненных клеток.
def random_move(board, list_):
    moves = []
    for i in list_:
        if check_free_space(board, i):
            moves.append(i)

    if len(moves) != 0:
        return random.choice(moves)
    else:
        return None     # Возвращает значение None, если больше нет допустимых ходов.


# Учитывая заполнение игрового поля и букву компьютера, определяет допустимый ход и возвращает его.
def python_move(board, computer_token):
    if computer_token == 'Х':
        player_token = 'О'
    else:
        player_token = 'Х'

# алгоритм для ИИ
# Сначала проверяем — победим ли мы, сделав следующий ход.
    for i in range(1, 10):
        new_board = new_playboard(board)
        if check_free_space(new_board, i):
            make_move(new_board, computer_token, i)
            if check_the_winner(new_board, computer_token):
                return i

# Проверяем — победит ли игрок, сделав следующий ход, и блокируем его.
    for i in range(1, 10):
        new_board = new_playboard(board)
        if check_free_space(new_board, i):
            make_move(new_board, player_token, i)
            if check_the_winner(new_board, player_token):
                return i
# Пробуем занять один из углов, если есть свободные.
    move = random_move(board, [1, 3, 7, 9])
    if move is not None:
        return move

# Пробуем занять центр, если он свободен.
    if check_free_space(board, 5):
        return 5

# Делаем ход по одной стороне.
    return random_move(board, [2, 4, 6, 8])


# Проверка — заполнено ли поле
def playboard_full(board):
# Возвращает True, если клетка на игровом поле занята. В противном случае, возвращает False.
    for i in range(1, 10):
        if check_free_space(board, i):
            return False
    return True


print('Игра "Крестики-нолики"')

while True:
    playInstruct()
# Перезагрузка игрового поля
    board = [' ']*10
    player_token, computer_token = play_token()
    turn = who_is_first()
    print('' + turn + ' ходит первым.')
    play_game = True
    while play_game:
        if turn == 'Человек':
# Ход игрока.
            playboard(board)
            move = player_move(board)
            make_move(board, player_token, move)

            if check_the_winner(board, player_token):
                playboard(board)
                print('Ура! Вы выиграли!')
                play_game = False
            else:
                if playboard_full(board):
                    playboard(board)
                    print('Ничья!')
                    break
                else:
                    turn = 'Компьютер'
        else:
# Ход компьютера.
            move = python_move(board, computer_token)
            make_move(board, computer_token, move)

            if check_the_winner(board, computer_token):
                playboard(board)
                print('Компьютер победил! Вы проиграли.')
                play_game = False
            else:
                if playboard_full(board):
                    playboard(board)
                    print('Ничья!')
                    break
                else:
                    turn = 'Человек'

    print('Сыграем еще раз? (Y или N)')
    if not input().lower().startswith('y'):
        break