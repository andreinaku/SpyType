from ExpVisitor import *
from run_inference import *


COMP_SINTACTIC = 1
COMP_SEMANTIC = 2


class TestError(Exception):
    pass


def translate_test(arg, trans_func, expected):
    result = trans_func(arg)
    if hash(result) != hash(expected):
        # if not result.same_as(expected):
        raise TestError("ERROR\nExpected: ", expected, "\nGot: ", result)
    print(trans_func.__name__ + "(" + str(locals()["arg"]) + ")" + " OK!")


def op_test(*args, func, expected=None, raise_exc=None, compare_type=COMP_SINTACTIC):
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
            raise TestError("Unknown type to translate: {}".format(tip))

    arglist = []
    for arg in args:
        trans_func = get_transfunc(arg[1])
        arglist.append(trans_func(arg[0]))
    result = None
    try:
        result = func(*arglist)
    except Exception as e:
        if e is raise_exc:
            raise TestError("ERROR\nExpected Exception: ", raise_exc, "\nGot: ", type(e))
        if str(e) != str(raise_exc):
            raise TestError("ERROR\nExpected Exception text: ", str(raise_exc), "\nGot: ", str(e))
    if compare_type == COMP_SINTACTIC:
        diff_flag = (hash(result) != hash(expected))
    elif compare_type == COMP_SEMANTIC:
        diff_flag = (result != expected)
    else:
        raise TestError('Unknown compare type: {}'.format(compare_type))
    if diff_flag:
        raise TestError("ERROR\nExpected: ", expected, "\nGot: ", result)
    print("OK! " + func.__name__ + "(" + str(locals()["args"]) + ")")


def transfer_test(str_in_state: str, str_code: str, str_expected: str, compare_type=COMP_SINTACTIC, apply_simps=False):
    node_ast = ast.parse(str_code)
    input_state = Translator.translate_as(str_in_state)
    expected_state = Translator.translate_as(str_expected)
    ev = ExpVisit(input_state)
    ev.visit(node_ast)
    if not apply_simps:
        result = ev.current_as
    else:
        result = ev.current_as.intermediary_simplifications()
    if compare_type == COMP_SINTACTIC:
        diff_flag = (hash(result) != hash(expected_state))
    elif compare_type == COMP_SEMANTIC:
        diff_flag = (result != expected_state)
    else:
        raise TestError('Unknown compare type: {}'.format(compare_type))
    if diff_flag:
        raise TestError("ERROR\nExpected: ", expected_state, "\nGot: ", result)
    print("OK! " + "visit_test(" + str_in_state + ", " + str_code + ", " + str_expected + ")")


def inference_test(filepath: str, funcname: str, str_expected: str, compare_type=COMP_SINTACTIC):
    (_rounds, result_as) = run_infer(filepath, funcname)
    expected_as = Translator.translate_as(str_expected)
    if compare_type == COMP_SINTACTIC:
        diff_flag = (hash(result_as) != hash(expected_as))
    elif compare_type == COMP_SEMANTIC:
        diff_flag = (result_as != expected_as)
    else:
        raise TestError('Unknown compare type: {}'.format(compare_type))
    if diff_flag:
        raise TestError("ERROR\nExpected: ", expected_as, "\nGot: ", result_as)
    print("OK! " + "inference_test(" + filepath + ", " + funcname + ", " + str_expected + ")")


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

    expected_translation = \
        TypeExpression([
            PyType(dict, TypeExpression([PyType(int)]), TypeExpression([PyType(float)]))
        ])
    translate_test(r'dict<int, float>', Translator.translate_te, expected_translation)

    expected_translation = \
        TypeExpression([
            PyType(dict,
                   TypeExpression([PyType(dict,
                                          TypeExpression([PyType(int)]),
                                          TypeExpression([PyType(float), PyType(str)])
                                          )
                                   ]),
                   TypeExpression([PyType(list,
                                          TypeExpression([VarType('T_c')])
                                          )
                                   ])
                   )
        ])
    translate_test(r'dict<dict<int, float+str>, list<T_c>>', Translator.translate_te, expected_translation)

    op_test((r'int+float', TypeExpression), (r'int+float+str', TypeExpression), func=TypeExpression.comparable,
            expected=True)
    op_test((r'int+T_b', TypeExpression), (r'int+float+str+T_a', TypeExpression), func=TypeExpression.comparable,
            expected=False)
    op_test((r'T_a+T_b', TypeExpression), (r'T_c', TypeExpression), func=TypeExpression.comparable,
            expected=False)
    op_test((r'int+float', TypeExpression), (r'int+str', TypeExpression), func=TypeExpression.comparable,
            expected=False)

    op_test((r'list<T_1>+int', TypeExpression), (r'list<int+T_1>+int+float', TypeExpression), func=TypeExpression.__le__,
            expected=True)
    op_test((r'int+float', TypeExpression), (r'int+float+str', TypeExpression), func=TypeExpression.__le__,
            expected=True)
    op_test((r'int+T_b', TypeExpression), (r'int+float+str+T_a', TypeExpression), func=TypeExpression.__le__,
            expected=False)
    op_test((r'T_a+T_b', TypeExpression), (r'T_c', TypeExpression), func=TypeExpression.__le__,
            expected=False)
    op_test((r'int+float', TypeExpression), (r'int+str', TypeExpression), func=TypeExpression.__le__,
            expected=False)
    op_test((r'int+float', TypeExpression), (r'int+float', TypeExpression), func=TypeExpression.__eq__,
            expected=True)
    op_test((r'int+float', TypeExpression), (r'int+float+T_b', TypeExpression), func=TypeExpression.__eq__,
            expected=False)
    op_test((r'int+float+T_a', TypeExpression), (r'int+float+T_b+T_c', TypeExpression), func=TypeExpression.__eq__,
            expected=False)
    op_test(
        (r'int+float+T_a+list<list<T_a>+float>', TypeExpression),
        (r'T_a', TypeExpression),
        (r'complex+str', TypeExpression),
        func=TypeExpression.replace_in_te,
        expected=Translator.translate_te(r'int+float+complex+str+list<list<complex+str>+float>')
    )
    op_test(
        (r'int+float+complex+T_b+set<list<T_a+T_b>+complex>', TypeExpression),
        (r'float+T_b', TypeExpression),
        (r'T_any', TypeExpression),
        func=TypeExpression.replace_in_te,
        expected=Translator.translate_te(r'int+complex+T_any+set<list<T_a+T_b>+complex>')
    )
    op_test(
        (r'int+T_any', TypeExpression),
        (r'int+T_any', TypeExpression),
        func=TypeExpression.__le__,
        expected=True
    )
    op_test((r'list<T_1>', TypeExpression), (r'list<int+T_1>', TypeExpression), func=TypeExpression.__eq__,
            expected=False)


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
            expected=False)
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
    # r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int /\ T_a:float /\ T_b:int /\ T_c:int) \/
    #   (T_a:float /\ T_a:str /\ T_b:T_c /\ T_c:float)'
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
    op_test(
        (r'a:T_a /\ b:T_b ^ (T_a:int /\ T_b:int)', AbsState),
        (r'a:T_1 ^ (T_1:float)', AbsState),
        func=AbsState.lub,
        expected=Translator.translate_as(r'a:T_a /\ b:T_b ^ (T_a:int /\ T_b:int) \/ (T_a:float)'),
        compare_type=COMP_SEMANTIC
    )
    op_test(
        (r'a:T_a /\ b:T_b /\ c:T_c ^ '
         r'(T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_b:float /\ T_c:float)', AbsState),
        (r'a:T_1 /\ b:T_2 /\ c:T_3 ^ (T_1:int /\ T_2:int /\ T_3:int)', AbsState),
        func=AbsState.lub,
        expected=Translator.translate_as(
            r'a:T_a /\ b:T_b /\ c:T_c ^ (T_a:int /\ T_b:int /\ T_c:int) \/ (T_a:float /\ T_b:float /\ T_c:float)'
        ),
        compare_type=COMP_SEMANTIC
    )
    op_test(
        (r'a:T_a /\ b:T_b ^ (T_a:int /\ T_b:int) \/ (T_a:float /\ T_b:float)', AbsState),
        (r'a:T_a /\ b:T_b ^ (T_a:str /\ T_b:str)', AbsState),
        func=AbsState.glb,
        expected=Translator.translate_as(
            r'a:T_a /\ b:T_b ^ (T_a:int /\ T_a:str /\ T_b:int /\ T_b:str) \/ '
            r'(T_a:float /\ T_a:str /\ T_b:float /\ T_b:str)'
        ),
        compare_type=COMP_SEMANTIC
    )
    # op_test(
    #     (r'a:T_a /\ __out_a:T_o ^ (T_a:int /\ T_o:list<int>)', AbsState),
    #     func=AbsState.ingest_output_vars,
    #     expected=Translator.translate_as(r'__orig_a:T_a /\ a:T_o ^ (T_a:int /\ T_o:list<int>)'),
    #     compare_type=COMP_SINTACTIC
    # )
    op_test(
        (r'a:T_a /\ __out_a:T_o ^ (T_a:int /\ T_o:list<int>)', AbsState),
        func=AbsState.ingest_output_vars,
        expected=Translator.translate_as(r'a:T_o ^ (T_a:int /\ T_o:list<int>)'),
        compare_type=COMP_SINTACTIC
    )
    op_test(
        (r'__orig_a:T_1 /\ a:T_d4cbb29_1 /\ b:T_d4cbb29_0 ^ '
         r'(T_d4cbb29_1:list<T_d4cbb29_0>) \/ '
         r'(T_d4cbb29_1:list<int+T_r> /\ T_1:list<T_r> /\ T_d4cbb29_0:int+T_r)', AbsState),
        (r'__orig_a:T_1 /\ a:T_d4cbb29_1 /\ b:T_d4cbb29_0 ^ '
         r'(T_d4cbb29_1:list<T_d4cbb29_0>) \/ '
         r'(T_d4cbb29_1:list<T_3+int> /\ T_1:list<T_3> /\ T_d4cbb29_0:T_3+int)', AbsState),
        func=AbsState.__eq__,
        expected=True
    )
    op_test(
        (r'a:T_a /\ return:T_r ^ (T_a:list<int+T_1> /\ T_r:bool) \/ (T_a:list<T_1> /\ T_r:bool)', AbsState),
        func=AbsState.simplify_keep_maximals,
        expected=Translator.translate_as(r'a:T_a /\ return:T_r ^ (T_a:list<int+T_1> /\ T_r:bool)'),
        compare_type=COMP_SINTACTIC
    )


def transfer_tests():
    transfer_test(
        r'a:T_bot /\ b:T_bot',
        'a=3',
        r'a:T_a /\ b:T_bot /\ 3:T_a ^ (T_a:int)',
        compare_type=COMP_SEMANTIC
    )
    transfer_test(
        r'a:T_bot',
        'a=None',
        r'a:T_a /\ None:T_a ^ (T_a:NoneType)',
        compare_type=COMP_SEMANTIC
    )
    transfer_test(
        r'a:T_bot /\ b:T_bot',
        r'a+b',
        r'a:T_a /\ b:T_b /\ a + b:T_c ^ (T_a:int /\ T_b:int /\ T_c:int) \/ '
        r'(T_a:list<T_1> /\ T_b:list<T_2> /\ T_c:list<T_1+T_2>) \/ '
        r'(T_a:float /\ T_b:float /\ T_c:float) \/ '
        r'(T_a:int /\ T_b:float /\ T_c:float) \/ '
        r'(T_a:float /\ T_b:int /\ T_c:float)',
        compare_type=COMP_SEMANTIC
    )
    transfer_test(
        r'a:T_a /\ b:T_b ^ (T_a:float /\ T_b:float)',
        r'a+b',
        r'a:T_a /\ b:T_b ^ (T_a:float /\ T_b:float)',
        compare_type=COMP_SEMANTIC,
        apply_simps=True
    )
    # interesting cases on account of the semantic equivalence of the types of __out_a
    transfer_test(
        r'a:T_a',
        r'a.append(3)',
        r'a:T_a /\ 3:T_c /\ __out_a:T_o ^ (T_a:list<T_1> /\ T_c:int /\ T_o:list<T_1+T_c>)',
        compare_type=COMP_SEMANTIC
    )
    transfer_test(
        r'a:T_a',
        r'a.append(3)',
        r'a:T_a /\ 3:T_c /\ __out_a:T_o ^ (T_a:list<T_1> /\ T_c:int /\ T_o:list<T_1+int>)',
        compare_type=COMP_SEMANTIC
    )
    #
    # transfer_test(
    #     str_in_state=r'b:T_b /\ a:T_a ^ (T_a:int /\ T_b:int /\ T_r:int) \/ '
    #                  r'(T_a:list<T_3> /\ T_b:list<T_4> /\ T_r:list<T_4+T_3>)',
    #     str_code=r'a.append(3)',
    #     str_expected=r'__orig_a:T_a /\ b:T_b /\ a:T_o ^ '
    #                  r'(T_a:list<T_3> /\ T_b:list<T_4> /\ T_c:int /\ T_o:list<T_3+int>)',
    #     compare_type=COMP_SEMANTIC,
    #     apply_simps=True
    # )
    transfer_test(
        str_in_state=r'b:T_b /\ a:T_a ^ (T_a:int /\ T_b:int /\ T_r:int) \/ '
                     r'(T_a:list<T_3> /\ T_b:list<T_4> /\ T_r:list<T_4+T_3>)',
        str_code=r'a.append(3)',
        str_expected=r'b:T_b /\ a:T_o ^ '
                     r'(T_b:list<T_4> /\ T_c:int /\ T_o:list<T_3+int>)',
        compare_type=COMP_SEMANTIC,
        apply_simps=True
    )
    # transfer_test(
    #     r'a:T_a /\ b:T_bot',
    #     r'a.append(3)',
    #     r'__orig_a:T_a /\ a:T_o /\ b:T_bot ^ (T_a:list<T_1> /\ T_o:list<T_1+int>)',
    #     compare_type=COMP_SEMANTIC,
    #     apply_simps=True
    # )
    transfer_test(
        r'a:T_a /\ b:T_bot',
        r'a.append(3)',
        r'a:T_o /\ b:T_bot ^ (T_o:list<T_1+int>)',
        compare_type=COMP_SEMANTIC,
        apply_simps=True
    )


def inference_tests():
    inference_test(
        'test_funcs.py',
        'f',
        str_expected=r'a:T_c ^ (T_c:int)',
        compare_type=COMP_SEMANTIC
    )
    # inference_test(
    #     'test_funcs.py',
    #     'h',
    #     str_expected=r'__orig_a:T_a /\ b:T_b /\ c:T_c /\ a:T_o ^ '
    #                  r'(T_a:list<T_1> /\ T_b:list<T_2> /\ T_c:list<T_1+T_2> /\ T_o:list<T_1+int>)',
    #     compare_type=COMP_SEMANTIC
    # )
    inference_test(
        'test_funcs.py',
        'h',
        str_expected=r'b:T_b /\ c:T_c /\ a:T_o ^ '
                     r'(T_b:list<T_2> /\ T_c:list<T_1+T_2> /\ T_o:list<T_1+int>)',
        compare_type=COMP_SEMANTIC
    )
    inference_test(
        'test_funcs.py',
        'g',
        str_expected=r'a:T_a /\ b:T_b /\ c:T_c /\ return:T_c ^ '
                     r'(T_a:int /\ T_b:int /\ T_c:int) \/ '
                     r'(T_a:int /\ T_b:float /\ T_c:float) \/ '
                     r'(T_a:float /\ T_b:int /\ T_c:float) \/ '
                     r'(T_a:float /\ T_b:float /\ T_c:float) \/ '
                     r'(T_a:list<T_1> /\ T_b:list<T_2> /\ T_c:list<T_1+T_2>)',
        compare_type=COMP_SEMANTIC
    )
    inference_test(
        'test_funcs.py',
        'i',
        str_expected=r'a:T_a /\ b:T_b /\ return:T_b ^ '
                     r'(T_a:int /\ T_b:int) \/ '
                     r'(T_a:float /\ T_b:float)',
        compare_type=COMP_SEMANTIC
    )
    # inference_test(
    #     'test_funcs.py',
    #     'j',
    #     str_expected=r'__orig_a:T_a /\ b:T_o /\ return:T_o /\ a:T_o ^ (T_a:list<T_1> /\ T_o:list<T_1+int>)',
    #     compare_type=COMP_SEMANTIC
    # )
    inference_test(
        'test_funcs.py',
        'j',
        str_expected=r'b:T_o /\ return:T_o /\ a:T_o ^ (T_o:list<T_1+int>)',
        compare_type=COMP_SEMANTIC
    )
    # inference_test(
    #     filepath='test_funcs.py',
    #     funcname='k',
    #     str_expected=r'__orig_a:T_o /\ a:T_a /\ return:T_r ^ '
    #                  r'(T_a:list<T_1> /\ T_r:bool) \/ '
    #                  r'(T_o:list<T_1> /\ T_a:list<T_1+int> /\ T_r:bool)',
    #     compare_type=COMP_SEMANTIC
    # )
    inference_test(
        filepath='test_funcs.py',
        funcname='k',
        str_expected=r'a:T_a /\ return:T_r ^ '
                     r'(T_a:list<T_1> /\ T_r:bool) \/ '
                     r'(T_a:list<T_1+int> /\ T_r:bool)',
        compare_type=COMP_SEMANTIC
    )
    # inference_test(
    #     filepath='test_funcs.py',
    #     funcname='l',
    #     str_expected=r'__orig_a:T_a /\ b:T_b /\ a:T_o /\ return:T_r ^ '
    #                  r'(T_o:list<T_1> /\ T_r:bool) \/ '
    #                  r'(T_a:list<T_1> /\ T_o:list<T_1+int> /\ T_b:T_1+int /\ T_r:bool)',
    #     compare_type=COMP_SEMANTIC
    # )
    inference_test(
        filepath='test_funcs.py',
        funcname='l',
        str_expected=r'b:T_b /\ a:T_o /\ return:T_r ^ '
                     r'(T_o:list<T_1> /\ T_r:bool) \/ '
                     r'(T_o:list<T_1+int> /\ T_b:T_1+int /\ T_r:bool)',
        compare_type=COMP_SEMANTIC
    )


def aux_tests():
    pass


if __name__ == "__main__":
    # te_tests()
    # print('\n----------------\n')
    # va_tests()
    # print('\n----------------\n')
    # ctx_tests()
    # print('\n----------------\n')
    # tc_tests()
    # print('\n----------------\n')
    # as_tests()
    # print('\n----------------\n')
    # transfer_tests()
    # print('\n----------------\n')
    # inference_tests()
    # print('\n----------------\n')
    aux_tests()
