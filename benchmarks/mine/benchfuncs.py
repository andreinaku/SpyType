import random


def if_1(x, y):
    if random.randint(0, 10) < 5:
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
    while True:
        a.append(3)
    return None


def append_3():
    a = []
    while random.randint(0, 10) < 5:
        if random.randint(0, 10) < 5:
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


# if __name__ == '__main__':
x1 = if_1(2, 3.5)
# x2 = assign_1([2, 3])
# x3 = add_1(4.5)
# x4 = append_1([5])
# # x5 = append_2(['5'])
# x6 = append_3()
# x7 = for_1(2, 3)
# x8 = for_2(2, [3, 4])
print('done')
