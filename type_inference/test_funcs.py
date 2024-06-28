def d(a):
    c = len(a)
    return c


def e(a, b):
    c = a >> b
    return c


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


def issue_64(source):
    first = []
    source.reverse()
    while source:
        tok = source.pop()
        first.append(tok)
        aux = len(tok)
    return True


def issue_64_infinite():
    a = []
    while True:
        a.append(3)
    return True


def issue_64_infinite_2():
    a = []
    while True:
        b = a.pop()
        a.append(3)
    return True


def issue_64_2(source):
    first = []
    source.reverse()
    tok = source.pop()
    first.append(tok)
    aux = len(tok)
    return first


def issue_64_1(source, pos, maxline):
    first = []
    source.reverse()
    while source:
        tok = source.pop()
        first.append(tok)
        pos += len(tok)
        if source:
            tok = source[-1]
            # allowed = (maxline + 1) if tok.endswith(' ') else (maxline - 4)
            # allowed = 3  # for first test
            # if pos + len(tok) > allowed:
            #     break

    source.reverse()
    return first, source


def test_if(b):
    if True:
        a = 3
    else:
        a = 3.5
    b = a >> 10
    return b


def test_if_2(b):
    if True:
        a = 3
    else:
        a = 3.5
    b = a + 10
    return b


def test_while_1(b):
    while True:
        a = b + 3
    return a


def test_while_2(b):
    while True:
        a = b >> 3
    return a


def test_add(a, b, c):
    return a + b + c


def f1(x, y):
    a, b = x
    return y[a + 1, b - 1]
