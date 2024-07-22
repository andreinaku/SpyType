from random import randint


rand_cond = randint(0, 10) <= 5


def while_1(x):
    L = []
    y = x
    while y:
        L.append(y % 2)
        y = y >> 1
    return L   


def append_2(a):
    if rand_cond:
        a.append(3)
    return None


res = while_1(2)
append_2(['2'])
