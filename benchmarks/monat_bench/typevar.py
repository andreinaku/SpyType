from typing import TypeVar, Generic


t = TypeVar('T')


def f(x: T):
    a = x + 2
    return a


print(f(4))

