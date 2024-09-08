import time


rand_cond = (time.time() % 1) >= 0.5


def if_1(x, y):
    '''
    Tests inference over branches given by if-else statement.
    '''
    if rand_cond:
        a = x
    else:
        a = y
    return a >> 2


def if_2(x, y):
    '''
    Tests inference over different branches and constraint gathering from conditional statements that contain binary operators.
    '''
    if (x >> 2) >= (y << 2):
        return y << x
    return y


def try_1(x):
    '''
    Tests inference over branches given by try-except statement and constraints given by subscription operator.
    '''
    try:
        aux = x[0]
    except:
        aux = 0
    return aux


def while_1(x):
    '''
    Tests inference over branches given by while statement and constraints given by binary operators.
    '''
    L = []
    y = x
    while y:
        L.append(y % 2)
        y = y >> 1
    return L


def assign_1(c):
    '''
    Tests inference with constraints added by assignment with list target and binary operators.
    '''
    a, b = c
    aux = a >> b
    return aux


def add_1(a):
    '''
    Tests inference with constraints added by a simple binary operator.
    '''
    b = a + 3.5
    return b


def append_1(a):
    '''
    Tests inference with constraints added from for-statements, range function, subscription operator and append calls.
    '''
    for i in range(0, a[0]):
        a.append('x')
    return len(a)


def append_2(a):
    '''
    Tests inference with constraints added from append calls.
    '''
    if rand_cond:
        a.append(3)
    return None


def append_3():
    '''
    Tests inference with constraints added by append calls over different program branches.
    '''
    a = []
    while rand_cond:
        if rand_cond:
            a.append(3)
        else:
            a.append('3')
    return a[0]


def for_1(x, y):
    '''
    Tests inference with constraints added by for-statements, range calls, append calls, and binary operators.
    '''
    a = []
    for foo in range(x):
        bar = foo >> y
        a.append(bar)
    return a


def for_2(x, y):
    '''
    Tests inference with constraints added by for-statements and binary operators.
    '''
    bar = x
    for foo in y:
        bar = bar + (foo >> 2)
    return bar


def assign_multiple_1(x, y, z):
    '''
    Tests correct assignment of type variables in sequence assignments (verbose)
    '''
    a, b, c = x, y, z
