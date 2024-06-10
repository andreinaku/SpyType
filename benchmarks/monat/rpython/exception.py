def entry_point(argv):
    x = 2
    y = 'a'
    try:
        z = x + y
    except TypeError:
        z = 3.14
        a = z + 1
    return 0

def target(*args):
    return entry_point, None
