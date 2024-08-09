def add_1(a):
    '''
    Tests inference with constraints added by a simple binary operator.
    '''
    b = a + 3.5
    return b

def add_1_annotated(a:float):
    '''
    Tests inference with constraints added by a simple binary operator.
    '''
    b = a + 3.5
    return b

reveal_type(add_1)
reveal_type(add_1_annotated)
