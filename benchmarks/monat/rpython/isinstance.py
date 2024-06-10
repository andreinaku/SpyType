def entry_point(argv):
    x = 2
    if isinstance(x, int):
        y = 4
    else:
        y = 'a'
    z = 3 + y
    return 0

def target(*args):
    return entry_point, None
