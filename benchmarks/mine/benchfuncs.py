import random


def if_1(x, y):
    if random.randint(0, 10) < 5:
        a = x
    else:
        a = y
    return a >> 2


def assign_1():
    a, b = [3, 3.5]
    return a, b


def assign_1_prim(c):
    a, b = c
    aux = a >> b
    return aux


def add_1(a):
    b = a + 3.5
    return b


def life_add_1(board, pos):
    row, column = pos
    return \
        board[row-1, column-1] + board[row-1, column]


def append_1(a):
    a = [3.5]
    a.append(3)


def append_2_prim(a):
    while True:
        a.append(3)


def append_4():
    a = []
    a.append(3)


def append_4_prim(a):
    a.append(3)


def append_5():
    a = []
    while random.randint(0, 10) < 5:
        if random.randint(0, 10) < 5:
            a.append(3)
        else:
            a.append('3')
    return a[0]

def append_5_prim(a):
    while random.randint(0, 10) < 5:
        if random.randint(0, 10) < 5:
            a.append(3)
        else:
            a.append('3')
    return a[0]
