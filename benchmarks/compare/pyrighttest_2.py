def if_2(x: int, y: int):
    if (x >> 2) >= (y << 2):
        return y << x
    return y
