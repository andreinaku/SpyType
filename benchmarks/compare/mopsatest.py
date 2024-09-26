def if_2(x, y):
    if (x >> 2) >= (y << 2):
        return y << x
    return y


aux = if_2(3, 4)
print(aux)
