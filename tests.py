from Translator import *


class TestErrror(Exception):
    pass


def translate_test(arg, trans_func, expected):
    result = trans_func(arg)
    if hash(result) != hash(expected):
        # if not result.same_as(expected):
        raise TestErrror("ERROR\nExpected: ", expected, "\nGot: ", result)
    print(trans_func.__name__ + "(" + str(locals()["arg"]) + ")" + " OK!")


# def op_test(*args, func, trans_func, expected=None, raise_exc=None):
#     te_list = []
#     for arg in args:
#         aux = trans_func(arg)
#         te_list.append(aux)
#     result = None
#     try:
#         result = func(*te_list)
#     except Exception as e:
#         if e is raise_exc:
#             raise TestErrror("ERROR\nExpected Exception: ", raise_exc, "\nGot: ", type(e))
#         if str(e) != str(raise_exc):
#             raise TestErrror("ERROR\nExpected Exception text: ", str(raise_exc), "\nGot: ", str(e))
#     if result != expected:
#         raise TestErrror("ERROR\nExpected: ", expected, "\nGot: ", result)
#     print(func.__name__ + "(" + str(locals()["args"]) + ")" + " OK!")


def op_test(*args, func, expected=None, raise_exc=None):
    def get_transfunc(tip):
        if tip == TypeExpression:
            return Translator.translate_te
        elif tip == VarAssign:
            return Translator.translate_va
        elif tip == Context:
            return Translator.translate_ctx
        elif tip == TypeConstraint:
            return Translator.translate_tc
        elif tip == AbsState:
            return Translator.translate_as
        elif tip == VarType:
            return Translator.translate_type
        elif tip == PyType:
            return Translator.translate_type
        else:
            raise TestErrror("Unknown type to translate: {}".format(tip))

    arglist = []
    for arg in args:
        trans_func = get_transfunc(arg[1])
        arglist.append(trans_func(arg[0]))
    result = None
    try:
        result = func(*arglist)
    except Exception as e:
        if e is raise_exc:
            raise TestErrror("ERROR\nExpected Exception: ", raise_exc, "\nGot: ", type(e))
        if str(e) != str(raise_exc):
            raise TestErrror("ERROR\nExpected Exception text: ", str(raise_exc), "\nGot: ", str(e))
    if hash(result) != hash(expected):
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

    op_test((r'int+float', TypeExpression), (r'int+float+str', TypeExpression), func=TypeExpression.comparable,
            expected=True)
    op_test((r'int+T_b', TypeExpression), (r'int+float+str+T_a', TypeExpression), func=TypeExpression.comparable,
            expected=True)
    op_test((r'T_a+T_b', TypeExpression), (r'T_c', TypeExpression), func=TypeExpression.comparable,
            expected=True)
    op_test((r'int+float', TypeExpression), (r'int+str', TypeExpression), func=TypeExpression.comparable,
            expected=False)

    op_test((r'int+float', TypeExpression), (r'int+float+str', TypeExpression), func=TypeExpression.__le__,
            expected=True)
    op_test((r'int+T_b', TypeExpression), (r'int+float+str+T_a', TypeExpression), func=TypeExpression.__le__,
            expected=False)
    op_test((r'T_a+T_b', TypeExpression), (r'T_c', TypeExpression), func=TypeExpression.__le__,
            expected=True)
    op_test((r'int+float', TypeExpression), (r'int+str', TypeExpression), func=TypeExpression.__le__,
            expected=False)
    op_test((r'int+float', TypeExpression), (r'int+float', TypeExpression), func=TypeExpression.__eq__,
            expected=True)
    op_test((r'int+float', TypeExpression), (r'int+float+T_b', TypeExpression), func=TypeExpression.__eq__,
            expected=False)
    op_test((r'int+float+T_a', TypeExpression), (r'int+float+T_b+T_c', TypeExpression), func=TypeExpression.__eq__,
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

    op_test((r'T_a:list<T_b> /\ T_b:set<int+str>', Context),
            (r'T_a:list<set<int+str>> /\ T_b:set<int+str>', Context),
            func=Context.__eq__,
            expected=True)
    op_test((r'T_a:list<T_b>', Context),
            (r'T_a:list<T_c>', Context),
            func=Context.__eq__,
            expected=True)
    op_test((r'T_a:int /\ T_b:int /\ T_c:int', Context),
            (r'T_a:int /\ T_b:int /\ T_c:T_d /\ T_d:int', Context),
            func=Context.__eq__,
            expected=False)
    op_test(
        (r'T_a:int /\ T_b:int /\ T_c:int', Context),
        (r'T_a:int+float /\ T_b:int+float /\ T_c:int+float', Context),
        func=Context.__le__,
        expected=True
    )
    op_test(
        (r'T_a:int+float+T_b /\ T_b:T_a+str', Context),
        (r'T_a', VarType),
        (r'T_a', VarType),
        (r'int+float+T_b', TypeExpression),
        func=Context.squash_te,
        expected=hset({Translator.translate_te(r'int+float+str+T_a')})
    )
    op_test(
        (r'T_a:int+float+T_b /\ T_b:T_c+str /\ T_c:complex+T_a', Context),
        (r'T_a', VarType),
        (r'T_a', VarType),
        (r'int+float+T_b', TypeExpression),
        func=Context.squash_te,
        expected=hset({Translator.translate_te(r'int+float+str+complex+T_a')})
    )
    op_test(
        (r'T_a:list<T_b>+str+float /\ T_b:int /\ T_b:float+str', Context),
        (r'T_a', VarType),
        func=Context.squash_vt,
        expected=hset({Translator.translate_te(r'str+float+list<int>'),
                       Translator.translate_te(r'str+float+list<float+str>')})
    )
    op_test(
        (r'T_a:int+T_b /\ T_b:str+T_a', Context),
        (r'T_a', VarType),
        func=Context.squash_vt,
        expected=hset({Translator.translate_te(r'int+str+T_a')})
    )
    op_test(
        (r'T_a:int+T_b /\ T_b:str+T_a', Context),
        (r'T_b', VarType),
        func=Context.squash_vt,
        expected=hset({Translator.translate_te(r'int+str+T_b')})
    )
    op_test(
        (r'T_a:list<T_b>+int /\ T_b:set<T_c> /\ T_c:int /\ T_c:str+T_a', Context),
        (r'T_a', VarType),
        func=Context.squash_vt,
        expected=hset({Translator.translate_te(r'int+list<set<int>>'),
                       Translator.translate_te(r'int+list<set<str+T_a>>')})
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
        (r'(T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:T_b /\ T_b:int /\ T_c:int)', TypeConstraint),
        (r'T_a:int /\ T_b:int /\ T_c:int', TypeConstraint),
        func=TypeConstraint.__eq__,
        expected=True
    )
    op_test(
        (r'(T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:T_b /\ T_b:int /\ T_c:int)', TypeConstraint),
        (r'T_a:int /\ T_b:int /\ T_c:int', TypeConstraint),
        func=TypeConstraint.__le__,
        expected=True
    )
    op_test(
        (r'(T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:T_b /\ T_b:int /\ T_c:int)', TypeConstraint),
        (r'T_a:int+float /\ T_b:int+float /\ T_c:int+float', TypeConstraint),
        func=TypeConstraint.__le__,
        expected=True
    )


def as_tests():
    # r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int /\ T_a:float /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_a:str /\ T_b:T_c /\ T_c:float)'
    va = VarAssign([
        ('a', VarType('T_a')),
        ('b', VarType('T_b')),
        ('c', VarType('T_c'))
    ])
    ctx1 = Context([
        ('T_a', hset({TypeExpression([PyType(int)]), TypeExpression([PyType(float)])})),
        ('T_b', hset({TypeExpression([PyType(int)])})),
        ('T_c', hset({TypeExpression([PyType(int)])}))
    ])
    ctx2 = Context([
        ('T_a', hset({TypeExpression([PyType(float)]), TypeExpression([PyType(str)])})),
        ('T_b', hset({TypeExpression([VarType('T_c')])})),
        ('T_c', hset({TypeExpression([PyType(float)])}))
    ])
    tc = TypeConstraint({ctx1, ctx2})
    expected_translation = AbsState(va, tc)
    translate_test(r'a:T_a /\ b:T_b /\ c:T_c ^ '
                   r'(T_a:int /\ T_a:float /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_a:str /\ T_b:T_c /\ T_c:float)',
                   Translator.translate_as, expected_translation)

    op_test(
        (r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_b:T_c /\ T_c:float)', AbsState),
        (r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_b:T_c /\ T_c:float)', AbsState),
        func=AbsState.__eq__,
        expected=True
    )
    op_test(
        (r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_b:T_c /\ T_c:float)', AbsState),
        (r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int+float /\ T_b:int+float /\ T_c:int+float)', AbsState),
        func=AbsState.__eq__,
        expected=False
    )
    op_test(
        (r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_b:T_c /\ T_c:float)', AbsState),
        (r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int+float /\ T_b:int+float /\ T_c:int+float)', AbsState),
        func=AbsState.__le__,
        expected=True
    )


def aux_tests():
    pass


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
    print('\n----------------\n')
    aux_tests()
