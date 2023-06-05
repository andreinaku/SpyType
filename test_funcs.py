def f():
    a = 3


def g(a, b):
    c = a + b
    return c


def h(a, b):
    c = a + b
    a.append(3)


def i():
    if True:
        a = 3
    else:
        a = 3.5
    b = a + 10
    return b
