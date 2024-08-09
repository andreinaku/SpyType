def f(a, b):
    c = a >> b
    reveal_type(c)
    return c


def g(a:int, b:int):
    c = a >> b
    reveal_type(c)
    return c

reveal_type(f)
reveal_type(g)
