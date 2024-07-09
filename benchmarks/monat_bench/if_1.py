import random


def if_1(x, y):
    if random.randint(0, 10) < 5:
        a = x
    else:
        a = y
    return a >> 2


result = if_1(3, 4.5)
print(result)
