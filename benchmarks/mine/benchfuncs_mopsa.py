from random import randint


rand_cond = randint(0, 10) <= 5


def while_1(x):
    L = []
    while x >> 2:
        L.append(x % 2)
    return L     


def append_2(a):
    while rand_cond:
        a.append(3)
    return None


def append_2_if(a):
    if rand_cond:
        a.append(3)
    return None


x1 = while_1(2)
x2 = append_2(['2'])
x3 = append_2_if(['2'])
print('done')
