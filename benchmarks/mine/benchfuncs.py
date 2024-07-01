def assign_1(c):
    a, b = c
    return a, b


def add_1(a):
    b = a + 3.5
    return b


def life_add_1(board, pos):
    row, column = pos
    return \
        board[row-1, column-1]


def append_1(a):
    a = [3.5]
    a.append(3)


def append_2(a):
    while True:
        a.append(3)
