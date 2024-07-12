import time


rand_cond = (time.time() % 1) >= 0.5


def if_1(x, y):
    if rand_cond:
        a = x
    else:
        a = y
    return a >> 2


def assign_1(c):
    a, b = c
    aux = a >> b
    return aux


def add_1(a):
    b = a + 3.5
    return b


def append_1(a):
    for i in range(0, a[0]):
        a.append('x')
    return len(a)


def append_2(a):
    while rand_cond:
        a.append(3)
    return None


def append_3():
    a = []
    while rand_cond:
        if rand_cond:
            a.append(3)
        else:
            a.append('3')
    return a[0]


def for_1(x, y):
    a = []
    for foo in range(x):
        bar = foo >> y
        a.append(bar)
    return a


def for_2(x, y):
    bar = x
    for foo in y:
        bar = bar + (foo >> 2)
    return bar
