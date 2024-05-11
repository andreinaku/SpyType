from testbase import *
from statev2.transfer import *
from pyiparser_2 import VARTYPE_REPLACE, builtin_types
from typing import *
from statev2.function_instance import FunctionInstance


class SpecTestCases(unittest.TestCase):
    def test_apply_spec_1(self):
        state = Translator.translate_state(r'((a:int+float /\ b:int+float))')
        spec = Translator.translate_state(r'(a:float /\ b:int)')
        expected_result = Translator.translate_state(
            r'((a:Ta` /\ b:Tb`) ^ '
            r'((Ta` <= int+float) /\ (Ta` <= float) /\ (Tb` <= int+float) /\ (Tb` <= int))'
            r')'
        )
        result = state_apply_spec(state, spec, testmode=True)
        self.assertEqual(result, expected_result)

    def test_apply_spec_set_1(self):
        stateset = Translator.translate_state_set(
            r'((a:Ta /\ b:Tb))'
        )
        specset = Translator.translate_state_set(
            r'((a:int /\ b:int)) \/ ((a:float /\ b:float))'
        )
        expected_result = Translator.translate_state_set(
            r'((a:Ta` /\ b:Tb`) ^ (Ta` <= Ta /\ Ta` <= int /\ Tb` <= Tb /\ Tb` <= int)) \/ '
            r'((a:Ta` /\ b:Tb`) ^ (Ta` <= Ta /\ Ta` <= float /\ Tb` <= Tb /\ Tb` <= float))'
        )
        result = set_apply_spec(stateset, specset, testmode=True)
        self.assertEqual(result, expected_result)

    def test_apply_spec_set_2(self):
        stateset = Translator.translate_state_set(
            r'((a:Ta /\ b:Tb) ^ (Ta <= int+float /\ Tb <= str))'
        )
        specset = Translator.translate_state_set(
            r'((a:int /\ b:int)) \/ ((a:float /\ b:float))'
        )
        expected_result = Translator.translate_state_set(
            r'((a:Ta` /\ b:Tb`) ^ '
            r'(Ta` <= Ta /\ Ta` <= int /\ Tb` <= Tb /\ Tb` <= int /\ Ta <= int+float /\ Tb <= str)) \/ '
            r'((a:Ta` /\ b:Tb`) ^ '
            r'(Ta <= int+float /\ Tb <= str /\ Ta` <= Ta /\ Ta` <= float /\ Tb` <= Tb /\ Tb` <= float))'
        )
        result = set_apply_spec(stateset, specset, testmode=True)
        self.assertEqual(result, expected_result)

    def test_spec_to_state_1(self):
        spec = Translator.translate_func_spec(r'((a:int /\ b:int) -> ((a+b):int))')
        result = spec_to_state(spec)
        expected_result = Translator.translate_state(r'(a:int /\ b:int /\ (a+b):int)')
        self.assertEqual(result, expected_result)

    def test_find_specs_1(self):
        expr = 'a + b'
        binop_node = ast.parse(expr).body[0].value
        result = find_spec(binop_node)
        expected_result = unitedspecs['__add__']
        self.assertEqual(result, expected_result)

    def test_get_specset_from_binop_1(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        result = get_specset(binop_node)
        expected_result = hset(
            {
                Translator.translate_func_spec(r'((self:complex /\ __value:complex) -> (return:complex))'),
                Translator.translate_func_spec(r'((self:float /\ __value:float) -> (return:float))'),
                Translator.translate_func_spec(r'((self:int /\ __value:int) -> (return:float))')
            }
        )
        self.assertEqual(result, expected_result)

    def test_substitute_binop_state_arguments_1(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state = Translator.translate_state(r'(a:int+float /\ b:int+float)')
        result = substitute_state_arguments(state, binop_node)
        expected_result = hset(
            {
                Translator.translate_func_spec(r'((a:complex /\ b:complex) -> ((a / b):complex))'),
                Translator.translate_func_spec(r'((a:float /\ b:float) -> ((a / b):float))'),
                Translator.translate_func_spec(r'((a:int /\ b:int) -> ((a / b):float))')
            }
        )
        self.assertEqual(result, expected_result)

    def test_set_apply_binop_spec_1(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state_set = Translator.translate_state_set(r'(a:Ta /\ b:Tb)')
        # result = set_apply_binop_spec(state_set, binop_node, testmode=True)
        result = set_apply_specset(state_set, binop_node, testmode=True)
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):complex) ^ '
                    r'(Ta` <= Ta /\ Ta` <= complex /\ Tb` <= Tb /\ Tb` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= Ta /\ Ta` <= float /\ Tb` <= Tb /\ Tb` <= float))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= Ta /\ Ta` <= int /\ Tb` <= Tb /\ Tb` <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_set_apply_binop_spec_2(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state_set = Translator.translate_state_set(
            r'((a:Ta /\ b:Tb) ^ (Ta <= int+float /\ Tb <= int+float)) \/ '
            r'(a:str /\ b:str)'
        )
        result = set_apply_specset(state_set, binop_node, testmode=True)
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):complex) ^ '
                    r'(Ta <= int+float /\ Tb <= int+float /\ Ta` <= Ta /\ Ta` <= complex /\ Tb` <= Tb /\ Tb` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta <= int+float /\ Tb <= int+float /\ Ta` <= Ta /\ Ta` <= float /\ Tb` <= Tb /\ Tb` <= float))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta <= int+float /\ Tb <= int+float /\ Ta` <= Ta /\ Ta` <= int /\ Tb` <= Tb /\ Tb` <= int))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):complex) ^ '
                    r'(Ta` <= str /\ Ta` <= complex /\ Tb` <= str /\ Tb` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= float /\ Tb` <= str /\ Tb` <= float))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= int /\ Tb` <= str /\ Tb` <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_set_apply_binop_spec_3(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state_set = Translator.translate_state_set(
            r'(a:str /\ b:str)'
        )
        result = set_apply_specset(state_set, binop_node, testmode=True)
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):complex) ^ '
                    r'(Ta` <= str /\ Ta` <= complex /\ Tb` <= str /\ Tb` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= float /\ Tb` <= str /\ Tb` <= float))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= int /\ Tb` <= str /\ Tb` <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_1(self):
        expr = 'a / b'
        state_set = Translator.translate_state_set(
            r'(a:str /\ b:str)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):complex) ^ '
                    r'(Ta` <= str /\ Ta` <= complex /\ Tb` <= str /\ Tb` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= float /\ Tb` <= str /\ Tb` <= float))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= int /\ Tb` <= str /\ Tb` <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_2(self):
        expr = '(a >> b) / c'
        state_set = Translator.translate_state_set(
            r'(a:Ta /\ b:Tb /\ c:Tc)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'((a:T1 /\ b:T2 /\ c:T4 /\ (a >> b):T3 /\ ((a >> b) / c):float) ^ '
                    r'(T1 <= Ta /\ T1 <= int /\ T2 <= Tb /\ T2 <= int /\ T4 <= int /\ T3 <= int /\ T4 <= Tc))'
                ),
                Translator.translate_state(
                    r'((a:T1 /\ b:T2 /\ c:T4 /\ (a >> b):T3 /\ ((a >> b) / c):float) ^ '
                    r'(T1 <= Ta /\ T1 <= int /\ T2 <= Tb /\ T2 <= int /\ T4 <= float /\ T3 <= int /\ T3 <= float /\ T4 <= Tc))'
                ),
                Translator.translate_state(
                    r'((a:T1 /\ b:T2 /\ c:T4 /\ (a >> b):T3 /\ ((a >> b) / c):complex) ^ '
                    r'(T1 <= Ta /\ T1 <= int /\ T2 <= Tb /\ T2 <= int /\ T4 <= complex /\ T3 <= int /\ T3 <= complex /\ T4 <= Tc))'
                ),
            }
        )
        self.assertEqual(result, expected_result)

    def test_visit_Constant_1(self):
        expr = '3'
        state_set = Translator.translate_state_set(
            r'(a:Ta /\ b:Tb) \/ (a:int /\ b:int)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = Translator.translate_state_set(
            r'(a:Ta /\ b:Tb /\ 3:int) \/ (a:int /\ b:int /\ 3:int)'
        )
        self.assertEqual(result, expected_result)

    def test_basetype_replace_vartype_1(self):
        bt = Translator.translate_basetype('list< T_1 > + dict< T_K, T_V >')
        result = bt.replace_vartype('T_1', 'T?0')
        result = result.replace_vartype('T_K', 'T?K')
        result = result.replace_vartype('T_V', 'T?V')
        expected_result = Translator.translate_basetype('list< T?0 > + dict< T?K, T?V >')
        self.assertEqual(result, expected_result)

    def test_basetype_replace_vartype_2(self):
        bt = Basetype({
            PyType(list, Basetype({VarType('_T')})),
            PyType(dict, Basetype({VarType('_KT')}), Basetype({VarType('_VT')}))
        })
        for entry, replacement in VARTYPE_REPLACE.items():
            bt = bt.replace_vartype(entry, replacement)
        result = bt
        expected_result = Translator.translate_basetype('list< T?0 > + dict< T?1, T?2 >')
        self.assertEqual(result, expected_result)

    def test_basetype_filter_pytypes_1(self):
        bt = Translator.translate_basetype('int + float + list< set < T1 > > + list< reversed< T2 > + complex >')
        result = bt.filter_pytypes(builtin_types)
        expected_result = Translator.translate_basetype('int + float + list< set < T1 > > + list< complex >')
        self.assertEqual(result, expected_result)

    def test_basetype_filter_pytypes_2(self):
        bt = Translator.translate_basetype('reversed< T2 >')
        result = bt.filter_pytypes(builtin_types)
        expected_result = Basetype()
        self.assertEqual(result, expected_result)

    # def test_basetype_filter_pytypes_3(self):
    #     bt = Translator.translate_basetype('Sized< T2 >')
    #     result = bt.filter_pytypes(builtin_types)
    #     expected_result = Basetype({PyType(Sized, Basetype({VarType('T2')}))})
    #     self.assertEqual(result, expected_result)

    def test_assignment_filter_pytypes_1(self):
        assignment = Translator.translate_assignment(
            'a:int + float + list< set < T1 > > + list< reversed< T2 > + complex > /\\ b: int + reversed< T3 >'
        )
        result = assignment.filter_pytypes(builtin_types)
        expected_result = Translator.translate_assignment(
            'a:int + float + list< set < T1 > > + list< complex > /\\ b: int'
        )
        self.assertEqual(result, expected_result)

    def test_relation_filter_pytypes_1(self):
        relation = Translator.translate_relation(
            'T1 <= int + float + list< set < T1 > > + list< reversed< T2 > + complex >'
        )
        result = relation.filter_pytypes(builtin_types)
        expected_result = Translator.translate_relation(
            'T1 <= int + float + list< set < T1 > > + list< complex >'
        )
        self.assertEqual(result, expected_result)

    def test_andconstraints_filter_pytypes_1(self):
        andconstr = Translator.translate_and_constraints(
            r'T1 <= int + float + list< set< T1 > > + list< reversed< T2 > + complex > /\ '
            r'T2 <= reversed< T3 > + float'
        )
        result = andconstr.filter_pytypes(builtin_types)
        expected_result = Translator.translate_and_constraints(
            'T1 <= int + float + list< set < T1 > > + list< complex > /\\ T2 <= float'
        )
        self.assertEqual(result, expected_result)

    def test_state_filter_pytypes_1(self):
        state = Translator.translate_state(
            '((a:reversed< Ta > + int /\\ b:complex + float) ^ (Ta <= reversed< T1 > + list< int >))'
        )
        result = state.filter_pytypes(builtin_types)
        expected_result = Translator.translate_state(
            '((a: int /\\ b:complex + float) ^ (Ta <= list< int >))'
        )
        self.assertEqual(result, expected_result)

    def test_stateset_filter_pytypes_1(self):
        stateset = Translator.translate_state_set(
            '((a:reversed< Ta > + int /\\ b:complex + float) ^ (Ta <= reversed< T1 > + list< int >)) \\/ '
            '(a:int /\\ b:reversed + float)'
        )
        result = stateset.filter_pytypes(builtin_types)
        expected_result = Translator.translate_state_set(
            '((a: int /\\ b:complex + float) ^ (Ta <= list< int >)) \\/ '
            '(a:int /\\ b:float)'
        )
        self.assertEqual(result, expected_result)

    def test_funcspec_filter_pytypes_1(self):
        funcspec = Translator.translate_func_spec(
            '((a:reversed< Ta > + int /\\ b:complex + float) -> (return: reversed + complex))'
        )
        result = funcspec.filter_pytypes(builtin_types)
        expected_result = Translator.translate_func_spec(
            '((a:int /\\ b:complex + float) -> (return: complex))'
        )
        self.assertEqual(result, expected_result)

    def test_visit_Tuple_1(self):
        expr = '(2, 3.5)'
        state_set = Translator.translate_state_set(
            r'(a:Ta /\ b:Tb) \/ (a:int /\ b:int)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = Translator.translate_state_set(
            r'(a:Ta /\ b:Tb /\ 2:int /\ 3.5:float /\ (2, 3.5):tuple< int + float >) \/ '
            r'(a:int /\ b:int /\ 2:int /\ 3.5:float /\ (2, 3.5):tuple< int + float >)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_Tuple_2(self):
        expr = '(a, b)'
        state_set = Translator.translate_state_set(
            r'(a:Ta /\ b:Tb) \/ (a:int /\ b:int)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = Translator.translate_state_set(
            r'(a:Ta /\ b:Tb /\ (a, b): tuple< Ta + Tb >) \/ (a:int /\ b:int /\ (a, b): tuple< int >)'
        )
        self.assertEqual(result, expected_result)

    def test_replace_superclasses_1(self):
        state_set = Translator.translate_state_set(r'__obj:Sized')
        result = state_set.replace_superclasses()
        expected_result = Translator.translate_state_set(
            r'__obj:memoryview + range + bytes + str + bytearray + list< top > + set< top > + '
            r'tuple< top > + frozenset< top > + dict< top, top >'
        )
        self.assertEqual(result, expected_result)

    def test_basetype_get_builtin_1(self):
        bt = Translator.translate_basetype(r'Iterable< T1 >')
        result = bt.get_builtin_from_bt()
        expected_result = Translator.translate_basetype(
            r'list< T1 > + set< T1 > + frozenset< T1 > + tuple< T1 > '
        )
        self.assertEqual(result, expected_result)

    def test_basetype_get_builtin_2(self):
        bt = Translator.translate_basetype(r'Iterable< top >')
        result = bt.get_builtin_from_bt()
        expected_result = Translator.translate_basetype(
            r'list< top > + set< top > + frozenset< top > + tuple< top > + '
            r'str + memoryview + bytes + bytearray + range'
        )
        self.assertEqual(result, expected_result)

    def test_basetype_get_builtin_3(self):
        bt = Translator.translate_basetype(r'Iterable')
        result = bt.get_builtin_from_bt()
        expected_result = Translator.translate_basetype(
            r'list< top > + set< top > + frozenset< top > + tuple< top > + dict< top, top > + '
            r'str + memoryview + bytes + bytearray + range'
        )
        self.assertEqual(result, expected_result)

    def test_get_specset_1(self):
        code = 'len(a)'
        node = ast.parse(code).body[0].value
        result = get_specset(node)
        expected_result = hset()
        expected_result.add(
            Translator.translate_func_spec(
                r'((__obj:Sized) -> (return:int))'
            )
        )
        self.assertEqual(result, expected_result)

    def test_substitute_call_state_arguments_1(self):
        expr = 'len(a)'
        call_node = ast.parse(expr).body[0].value
        state = Translator.translate_state(r'(a:int+float /\ b:int+float)')
        result = substitute_state_arguments(state, call_node)
        param_instantiated = Translator.translate_func_spec(
            r'((a:Sized) -> (len(a):int))'
        )
        expected_result = hset()
        expected_result.add(param_instantiated)
        self.assertEqual(result, expected_result)

    def test_visit_Call_1(self):
        expr = 'len(a)'
        state_set = Translator.translate_state_set(r'(a:int+float /\ b:int+float)')
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result = Translator.translate_state_set(
            r'((a:T1 /\ b:int+float /\ len(a):int) ^ (T1 <= int + float /\ T1 <= Sized))'
        )
        self.assertEqual(result, expected_result)

    def test_param_link_1(self):
        # def foo(a:int, b:int, /, c:int, *d:Any, e:int, f:int, **g:Any) -> bool: ...
        callnode = ast.parse('foo(h,i,j,k,l,m,n,e=o,f=p,w=q,x=r,y=s,z=t)').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, None, spec_set[0])
        result = fi.param_to_args()
        expected_result = {
            '__po_a': 'h',
            '__po_b': 'i',
            'c': 'j',
            '__va_d': ['k', 'l', 'm', 'n'],
            '__ko_e': 'o',
            '__ko_f': 'p',
            '__kw_g': {
                '__ko_w': 'q',
                '__ko_x': 'r',
                '__ko_y': 's',
                '__ko_z': 't'
            }
        }
        self.assertEqual(result, expected_result)
        
    def test_param_link_2(self):
        # def qux(a:int, b:float, c:str) -> complex: ...
        callnode = ast.parse('qux(h,i,j)').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, None, spec_set[0])
        result = fi.param_to_args()
        expected_result = {
            'a': 'h',
            'b': 'i',
            'c': 'j',
        }
        self.assertEqual(result, expected_result)

    def test_param_link_3(self):
        # def corge(*args:Any, **kwargs:Any) -> bool: ...
        callnode = ast.parse('corge(a,b,c,d)').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, None, spec_set[0])
        result = fi.param_to_args()
        expected_result = {
            '__va_args': ['a', 'b', 'c', 'd'],
            '__kw_kwargs': {}
        }
        self.assertEqual(result, expected_result)

    def test_param_link_4(self):
        # def corge(*args:Any, **kwargs:Any) -> bool: ...
        callnode = ast.parse('corge(a,b,c,d,e=x,f=y)').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, None, spec_set[0])
        result = fi.param_to_args()
        expected_result = {
            '__va_args': ['a', 'b', 'c', 'd'],
            '__kw_kwargs': {
                '__ko_e': 'x',
                '__ko_f': 'y'
            }
        }
        self.assertEqual(result, expected_result)
