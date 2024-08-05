import time


rand_cond = (time.time() % 1) >= 0.5


def anytest():
    c = [3]
    while rand_cond:
        c = [c]
    return c
