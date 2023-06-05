from ast import *


def compute_opspecs():
    opspecs = {
        BinOp: {
            Add: r'__in_p1:T?1 /\ __in_p2:T?2 /\ return:T?r ^ '
                 r'(T?1:int /\ T?2:int /\ T?r:int) \/ '
                 r'(T?1:float /\ T?2:float /\ T?r:float) \/ '
                 r'(T?1:int /\ T?2:float /\ T?r:float) \/ '
                 r'(T?1:float /\ T?2:int /\ T?r:float) \/ '
                 r'(T?1:list<T?3> /\ T?2:list<T?4> /\ T?r:list<T?3+T?4>)',
            LShift: r'__in_p1:T?1 /\ __in_p2:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int)',
            Mult: r'__in_p1:T?1 /\ __in_p2:T?2 /\ return:T?r ^ '
                  r'(T?1:int /\ T?2:int /\ T?r:int) \/ '
                  r'(T?1:float /\ T?2:float /\ T?r:float) \/ '
                  r'(T?1:int /\ T?2:float /\ T?r:float) \/ '
                  r'(T?1:float /\ T?2:int /\ T?r:float)'
        }
    }
    return opspecs


def compute_funcspecs():
    funcspecs = {
        '_test1': r'__in_p1:T?1 /\ __in_p2:T?2 /\ __out_p1:T?o ^ (T?1:list<T?`1> /\ T?o:list<T?`1+T?2>)',
        '_test2': r'__in_p1:T?1 /\ __in_p2:T?2 /\ return:T?r ^ (T?1:int /\ T?2:int /\ T?r:int) \/ '
                  r'(T?1:float /\ T?2:float /\ T?r:float)',
        '_test3': r'__in_p1:T?1 ^ (T?1:int+float)',
        '_test4': r'__in_p1:T?1 ^ (T?1:float)',
        '_test5': r'__in_p1:T?1 /\ __in_p2:T?2 ^ (T?1:list<T?2>)',
        '_test6': r'__in_p1:T?1 ^ (T?1:int)',
        'append': r'__in_p1:T?1 /\ __in_p2:T?2 /\ __out_p1:T?o ^ (T?1:list<T?3> /\ T?o:list<T?3+T?2>)',
        # 'append': r'__in_p1:T?1 /\ __in_p2:T?2 /\ __out_p1:T?o ^ (T?1:list<T?`1> /\ T?o:list<T?`2> /\ T?`2:T?`1+T?2)',
        'reverse': r'__in_p1:T?1 ^ (T?1:list<T?2>)',
        # 'pop': r'__in_p1:T?1 /\ return:T?r ^ (T?1:list<T?2> /\ T?r:T?2)',
        'pop': r'__in_p1:T?1 /\ return:T?r ^ (T?1:list<T?r>)',
        'len': r'__in_p1:T?1 /\ return:T?r ^ (T?1:str /\ T?r:int) \/ (T?1:list<T?2> /\ T?r:int)'
    }
    return funcspecs
