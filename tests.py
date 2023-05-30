from Translator import *


class TestErrror(Exception):
    pass


def translate_test(arg, trans_func, expected):
    result = trans_func(arg)
    if hash(result) != hash(expected):
        # if not result.same_as(expected):
        raise TestErrror("ERROR\nExpected: ", expected, "\nGot: ", result)
    print(trans_func.__name__ + "(" + str(locals()["arg"]) + ")" + " OK!")


def op_test(*args, func, trans_func, expected=None, raise_exc=None):
    te_list = []
    for arg in args:
        aux = trans_func(arg)
        te_list.append(aux)
    result = None
    try:
        result = func(*te_list)
    except Exception as e:
        if e is raise_exc:
            raise TestErrror("ERROR\nExpected Exception: ", raise_exc, "\nGot: ", type(e))
        if str(e) != str(raise_exc):
            raise TestErrror("ERROR\nExpected Exception text: ", str(raise_exc), "\nGot: ", str(e))
    if result != expected:
        raise TestErrror("ERROR\nExpected: ", expected, "\nGot: ", result)
    print(func.__name__ + "(" + str(locals()["args"]) + ")" + " OK!")


def te_tests():
    # r'int+float+str+list<set<str+float+T_a>+T_b>+T_c'
    expected_translation = \
        TypeExpression([
            PyType(int),
            PyType(float),
            PyType(str),
            PyType(list, TypeExpression([PyType(set, TypeExpression([PyType(str),
                                                                     PyType(float),
                                                                     VarType('T_a')])),
                                        VarType('T_b')])),
            VarType('T_c')])
    translate_test(r'int+float+str+list<set<str+float+T_a>+T_b>+T_c', Translator.translate_te, expected_translation)

    op_test(r'int+float', r'int+float+str', trans_func=Translator.translate_te, func=TypeExpression.comparable,
            expected=True)
    op_test(r'int+T_b', r'int+float+str+T_a', trans_func=Translator.translate_te, func=TypeExpression.comparable,
            expected=True)
    op_test(r'T_a+T_b', r'T_c', trans_func=Translator.translate_te, func=TypeExpression.comparable,
            expected=True)
    op_test(r'int+float', r'int+str', trans_func=Translator.translate_te, func=TypeExpression.comparable,
            expected=False)

    op_test(r'int+float', r'int+float+str', trans_func=Translator.translate_te, func=TypeExpression.__le__,
            expected=True)
    op_test(r'int+T_b', r'int+float+str+T_a', trans_func=Translator.translate_te, func=TypeExpression.__le__,
            expected=False)
    op_test(r'T_a+T_b', r'T_c', trans_func=Translator.translate_te, func=TypeExpression.__le__,
            expected=True)
    op_test(r'int+float', r'int+str', trans_func=Translator.translate_te, func=TypeExpression.__le__,
            expected=False)
    op_test(r'int+float', r'int+float', trans_func=Translator.translate_te, func=TypeExpression.__eq__,
            expected=True)
    op_test(r'int+float', r'int+float+T_b', trans_func=Translator.translate_te, func=TypeExpression.__eq__,
            expected=False)
    op_test(r'int+float+T_a', r'int+float+T_b+T_c', trans_func=Translator.translate_te, func=TypeExpression.__eq__,
            expected=True)


def va_tests():
    # r'a:T_a /\ b:T_b /\ c:T_c'
    expected_translation = VarAssign([
        ('a', VarType('T_a')),
        ('b', VarType('T_b')),
        ('c', VarType('T_c'))
    ])
    translate_test(r'a:T_a /\ b:T_b /\ c:T_c', Translator.translate_va, expected_translation)


def ctx_tests():
    # r'T_a:int+float /\ T_b:list<set<str>> /\ T_c:float+str'
    expected_translation = Context([
        ('T_a', hset({TypeExpression([PyType(int), PyType(float)])})),
        ('T_b', hset({TypeExpression([PyType(list, TypeExpression([PyType(set, TypeExpression([PyType(str)]))]))])})),
        ('T_c', hset({TypeExpression([PyType(float), PyType(str)])}))
    ])
    translate_test(r'T_a:int+float /\ T_b:list<set<str>> /\ T_c:float+str', Translator.translate_ctx,
                   expected_translation)

    # r'T_a:T_b'
    expected_translation = Context([
        ('T_a', hset({TypeExpression([VarType('T_b')])}))
    ])
    translate_test(r'T_a:T_b', Translator.translate_ctx, expected_translation)

    # r'T_a:int+float /\ T_b:T_c /\ T_c:float+str'
    expected_translation = Context([
        ('T_a', hset({TypeExpression([PyType(int), PyType(float)])})),
        ('T_b', hset({TypeExpression([VarType('T_c')])})),
        ('T_c', hset({TypeExpression([PyType(float), PyType(str)])}))
    ])
    translate_test(r'T_a:int+float /\ T_b:T_c /\ T_c:float+str', Translator.translate_ctx,
                   expected_translation)

    op_test(r'T_a:list<T_b> /\ T_b:set<int+str>',
            r'T_a:list<set<int+str>> /\ T_b:set<int+str>',
            func=Context.__eq__,
            trans_func=Translator.translate_ctx,
            expected=True)
    op_test(r'T_a:list<T_b>',
            r'T_a:list<T_c>',
            func=Context.__eq__,
            trans_func=Translator.translate_ctx,
            expected=True)
    op_test(r'T_a:int /\ T_b:int /\ T_c:int',
            r'T_a:int /\ T_b:int /\ T_c:T_d /\ T_d:int',
            func=Context.__eq__,
            trans_func=Translator.translate_ctx,
            expected=False)
    op_test(
        r'T_a:int /\ T_b:int /\ T_c:int',
        r'T_a:int+float /\ T_b:int+float /\ T_c:int+float',
        func=Context.__le__,
        trans_func=Translator.translate_ctx,
        expected=True
    )


def tc_tests():
    # r'(T_a:int+float /\ T_b:list<set<str>> /\ T_c:float+str) \/ (T_a:int /\ T_b:int /\ T_c:int)'
    ctx1 = Context([
        ('T_a', hset({TypeExpression([PyType(int), PyType(float)])})),
        ('T_b', hset({TypeExpression([PyType(list, TypeExpression([PyType(set, TypeExpression([PyType(str)]))]))])})),
        ('T_c', hset({TypeExpression([PyType(float), PyType(str)])}))
    ])
    ctx2 = Context([
        ('T_a', hset({TypeExpression([PyType(int)])})),
        ('T_b', hset({TypeExpression([PyType(int)])})),
        ('T_c', hset({TypeExpression([PyType(int)])}))
    ])
    expected_translation = TypeConstraint()
    expected_translation.add(ctx1)
    expected_translation.add(ctx2)
    translate_test(r'(T_a:int+float /\ T_b:list<set<str>> /\ T_c:float+str) \/ (T_a:int /\ T_b:int /\ T_c:int)',
                   Translator.translate_tc, expected_translation)

    op_test(
        r'(T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:T_b /\ T_b:int /\ T_c:int)',
        r'T_a:int /\ T_b:int /\ T_c:int',
        func=TypeConstraint.__eq__,
        trans_func=Translator.translate_tc,
        expected=True
    )
    op_test(
        r'(T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:T_b /\ T_b:int /\ T_c:int)',
        r'T_a:int /\ T_b:int /\ T_c:int',
        func=TypeConstraint.__le__,
        trans_func=Translator.translate_tc,
        expected=True
    )
    op_test(
        r'(T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:T_b /\ T_b:int /\ T_c:int)',
        r'T_a:int+float /\ T_b:int+float /\ T_c:int+float',
        func=TypeConstraint.__le__,
        trans_func=Translator.translate_tc,
        expected=True
    )


def as_tests():
    # r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_b:T_c /\ T_c:float)'
    va = VarAssign([
        ('a', VarType('T_a')),
        ('b', VarType('T_b')),
        ('c', VarType('T_c'))
    ])
    ctx1 = Context([
        ('T_a', hset({TypeExpression([PyType(int)])})),
        ('T_b', hset({TypeExpression([PyType(int)])})),
        ('T_c', hset({TypeExpression([PyType(int)])}))
    ])
    ctx2 = Context([
        ('T_a', hset({TypeExpression([PyType(float)])})),
        ('T_b', hset({TypeExpression([VarType('T_c')])})),
        ('T_c', hset({TypeExpression([PyType(float)])}))
    ])
    tc = TypeConstraint({ctx1, ctx2})
    expected_translation = AbsState(va, tc)
    translate_test(r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_b:T_c /\ T_c:float)',
                   Translator.translate_as, expected_translation)

    op_test(
        r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_b:T_c /\ T_c:float)',
        r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_b:T_c /\ T_c:float)',
        func=AbsState.__eq__,
        trans_func=Translator.translate_as,
        expected=True
    )
    op_test(
        r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_b:T_c /\ T_c:float)',
        r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int+float /\ T_b:int+float /\ T_c:int+float)',
        func=AbsState.__eq__,
        trans_func=Translator.translate_as,
        expected=False
    )
    op_test(
        r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_b:T_c /\ T_c:float)',
        r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int+float /\ T_b:int+float /\ T_c:int+float)',
        func=AbsState.__le__,
        trans_func=Translator.translate_as,
        expected=True
    )


if __name__ == "__main__":
    te_tests()
    print('\n----------------\n')
    va_tests()
    print('\n----------------\n')
    ctx_tests()
    print('\n----------------\n')
    tc_tests()
    print('\n----------------\n')
    as_tests()
