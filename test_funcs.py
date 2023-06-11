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


def j(a):
    while True:
        a.append(3)
        b = a
    return b


def k():
    a = []
    while True:
        a.append(3)
    return True


def l():
    a = []
    while True:
        b = a.pop()
        a.append(3)
    return True
