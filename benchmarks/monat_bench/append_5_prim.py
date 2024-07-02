import random


def append_5_prim(a):
    while random.randint(0, 10) < 5:
        if random.randint(0, 10) < 5:
            a.append(3)
        else:
            a.append('3')
    return a[0]
