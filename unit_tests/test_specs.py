from testbase import *
from statev2.transfer import *
from pyiparser_2 import VARTYPE_REPLACE, builtin_types
from typing import *
from statev2.function_instance import FunctionInstance


class SpecTestCases(unittest.TestCase):
    def test_apply_spec_1(self):
        state = State.from_str(r'((a:int+float /\ b:int+float))')
        spec = State.from_str(r'(a:float /\ b:int)')
        expected_result = State.from_str(
            r'((a:Ta` /\ b:Tb`) ^ '
            r'((Ta` <= int+float) /\ (Ta` <= float) /\ (Tb` <= int+float) /\ (Tb` <= int))'
            r')'
        )
        result = state_apply_spec(state, spec, testmode=True)
        self.assertEqual(result, expected_result)

    def test_apply_spec_set_1(self):
        stateset = StateSet.from_str(
            r'((a:Ta /\ b:Tb))'
        )
        specset = StateSet.from_str(
            r'((a:int /\ b:int)) \/ ((a:float /\ b:float))'
        )
        expected_result = StateSet.from_str(
            r'((a:Ta /\ b:Tb) ^ (Ta <= int /\ Tb <= int)) \/ '
            r'((a:Ta /\ b:Tb) ^ (Ta <= float /\ Tb <= float))'
        )
        result = set_apply_spec(stateset, specset, testmode=True)
        self.assertEqual(result, expected_result)

    def test_apply_spec_set_2(self):
        stateset = StateSet.from_str(
            r'((a:Ta /\ b:Tb) ^ (Ta <= int+float /\ Tb <= str))'
        )
        specset = StateSet.from_str(
            r'((a:int /\ b:int)) \/ ((a:float /\ b:float))'
        )
        expected_result = StateSet.from_str(
            r'((a:Ta /\ b:Tb) ^ '
            r'(Ta <= int /\ Tb <= int /\ Ta <= int+float /\ Tb <= str)) \/ '
            r'((a:Ta /\ b:Tb) ^ '
            r'(Ta <= int+float /\ Tb <= str /\ Ta <= float /\ Tb <= float))'
        )
        result = set_apply_spec(stateset, specset, testmode=True)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_spec_to_state_1(self):
        spec = FuncSpec.from_str(r'((a:int /\ b:int) -> ((a+b):int))')
        result = spec_to_state(spec)
        expected_result = State.from_str(r'(a:int /\ b:int /\ (a+b):int)')
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
                FuncSpec.from_str(r'((self:complex /\ __value:complex) -> (return:complex))'),
                FuncSpec.from_str(r'((self:float /\ __value:float) -> (return:float))'),
                FuncSpec.from_str(r'((self:int /\ __value:int) -> (return:float))')
            }
        )
        self.assertEqual(result, expected_result)

    def test_substitute_binop_state_arguments_1(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state = State.from_str(r'(a:int+float /\ b:int+float)')
        result = substitute_state_arguments(binop_node)
        expected_result = hset(
            {
                FuncSpec.from_str(r'((a:complex /\ b:complex) -> ((a / b):complex))'),
                FuncSpec.from_str(r'((a:float /\ b:float) -> ((a / b):float))'),
                FuncSpec.from_str(r'((a:int /\ b:int) -> ((a / b):float))')
            }
        )
        self.assertEqual(result, expected_result)

    def test_set_apply_binop_spec_1(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state_set = StateSet.from_str(r'(a:Ta /\ b:Tb)')
        # result = set_apply_binop_spec(state_set, binop_node, testmode=True)
        result = set_apply_specset(state_set, binop_node, testmode=True)
        expected_result = StateSet(
            {
                State.from_str(
                    r'((a:Ta /\ b:Tb /\ (a / b):complex) ^ '
                    r'(Ta <= complex /\ Tb <= complex))'
                ),
                State.from_str(
                    r'((a:Ta /\ b:Tb /\ (a / b):float) ^ '
                    r'(Ta <= float /\ Tb <= float))'
                ),
                State.from_str(
                    r'((a:Ta /\ b:Tb /\ (a / b):float) ^ '
                    r'(Ta <= int /\ Tb <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_set_apply_binop_spec_2(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state_set = StateSet.from_str(
            r'((a:Ta /\ b:Tb) ^ (Ta <= int+float /\ Tb <= int+float)) \/ '
            r'(a:str /\ b:str)'
        )
        result = set_apply_specset(state_set, binop_node, testmode=True)
        expected_result = StateSet(
            {
                State.from_str(
                    r'((a:Ta /\ b:Tb /\ (a / b):complex) ^ '
                    r'(Ta <= int+float /\ Tb <= int+float /\ Ta <= complex /\ Tb <= complex))'
                ),
                State.from_str(
                    r'((a:Ta /\ b:Tb /\ (a / b):float) ^ '
                    r'(Ta <= int+float /\ Tb <= int+float /\ Ta <= float /\ Tb <= float))'
                ),
                State.from_str(
                    r'((a:Ta /\ b:Tb /\ (a / b):float) ^ '
                    r'(Ta <= int+float /\ Tb <= int+float /\ Ta <= int /\ Tb <= int))'
                ),
                State.from_str(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):complex) ^ '
                    r'(Ta` <= str /\ Ta` <= complex /\ Tb` <= str /\ Tb` <= complex))'
                ),
                State.from_str(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= float /\ Tb` <= str /\ Tb` <= float))'
                ),
                State.from_str(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= int /\ Tb` <= str /\ Tb` <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_set_apply_binop_spec_3(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state_set = StateSet.from_str(
            r'(a:str /\ b:str)'
        )
        result = set_apply_specset(state_set, binop_node, testmode=True)
        expected_result = StateSet(
            {
                State.from_str(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):complex) ^ '
                    r'(Ta` <= str /\ Ta` <= complex /\ Tb` <= str /\ Tb` <= complex))'
                ),
                State.from_str(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= float /\ Tb` <= str /\ Tb` <= float))'
                ),
                State.from_str(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= int /\ Tb` <= str /\ Tb` <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_1(self):
        expr = 'a / b'
        state_set = StateSet.from_str(
            r'(a:str /\ b:str)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet(
            {
                State.from_str(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):complex) ^ '
                    r'(Ta` <= str /\ Ta` <= complex /\ Tb` <= str /\ Tb` <= complex))'
                ),
                State.from_str(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= float /\ Tb` <= str /\ Tb` <= float))'
                ),
                State.from_str(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= int /\ Tb` <= str /\ Tb` <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_2(self):
        expr = '(a >> b) / c'
        state_set = StateSet.from_str(
            r'(a:Ta /\ b:Tb /\ c:Tc)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet(
            {
                State.from_str(
                    r'((a:Ta /\ b:Tb /\ c:Tc /\ (a >> b):T3 /\ ((a >> b) / c):float) ^ '
                    r'(Ta <= int /\ Tb <= int /\ Tc <= int /\ T3 <= int))'
                ),
                State.from_str(
                    r'((a:Ta /\ b:Tb /\ c:Tc /\ (a >> b):T3 /\ ((a >> b) / c):float) ^ '
                    r'(Ta <= int /\ Tb <= int /\ Tc <= float /\ T3 <= int /\ T3 <= float))'
                ),
                State.from_str(
                    r'((a:Ta /\ b:Tb /\ c:Tc /\ (a >> b):T3 /\ ((a >> b) / c):complex) ^ '
                    r'(Ta <= int /\ Tb <= int /\ Tc <= complex /\ T3 <= int /\ T3 <= complex))'
                ),
            }
        )
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_3(self):
        state = State.from_str(r'(a:T1 /\ b:T2)')
        state.gen_id = 3
        state_set = StateSet()
        state_set.add(deepcopy(state))
        code = 'a >> b'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'((a:T1 /\ b:T2 /\ (a >> b):int) ^ (T1 <= int /\ T2 <= int))'
        )
        self.assertEqual(result, expected_result)

    def test_visit_Constant_1(self):
        expr = '3'
        state_set = StateSet.from_str(
            r'(a:Ta /\ b:Tb) \/ (a:int /\ b:int)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:Ta /\ b:Tb /\ 3:int) \/ (a:int /\ b:int /\ 3:int)'
        )
        self.assertEqual(result, expected_result)

    def test_basetype_replace_vartype_1(self):
        bt = Basetype.from_str('list< T_1 > + dict< T_K, T_V >')
        result = bt.replace_vartype('T_1', 'T?0')
        result = result.replace_vartype('T_K', 'T?K')
        result = result.replace_vartype('T_V', 'T?V')
        expected_result = Basetype.from_str('list< T?0 > + dict< T?K, T?V >')
        self.assertEqual(result, expected_result)

    def test_basetype_replace_vartype_2(self):
        bt = Basetype({
            PyType(list, Basetype({VarType('_T')})),
            PyType(dict, Basetype({VarType('_KT')}), Basetype({VarType('_VT')}))
        })
        for entry, replacement in VARTYPE_REPLACE.items():
            bt = bt.replace_vartype(entry, replacement)
        result = bt
        expected_result = Basetype.from_str('list< T?0 > + dict< T?1, T?2 >')
        self.assertEqual(result, expected_result)

    def test_basetype_replace_vartype_with_basetype_1(self):
        bt = Basetype.from_str('T1 + int')
        result = bt.replace_vartype_with_basetype('T1',
                                                  Basetype.from_str('str + float')
                                                  )
        expected_result = Basetype.from_str('int + str + float')
        self.assertEqual(result, expected_result)

    def test_basetype_filter_pytypes_1(self):
        bt = Basetype.from_str('int + float + list< set < T1 > > + list< reversed< T2 > + complex >')
        result = bt.filter_pytypes(builtin_types)
        expected_result = Basetype.from_str('int + float + list< set < T1 > > + list< complex >')
        self.assertEqual(result, expected_result)

    def test_basetype_filter_pytypes_2(self):
        bt = Basetype.from_str('reversed< T2 >')
        result = bt.filter_pytypes(builtin_types)
        expected_result = Basetype()
        self.assertEqual(result, expected_result)

    # def test_basetype_filter_pytypes_3(self):
    #     bt = Basetype.from_str('Sized< T2 >')
    #     result = bt.filter_pytypes(builtin_types)
    #     expected_result = Basetype({PyType(Sized, Basetype({VarType('T2')}))})
    #     self.assertEqual(result, expected_result)

    def test_assignment_filter_pytypes_1(self):
        assignment = Assignment.from_str(
            'a:int + float + list< set < T1 > > + list< reversed< T2 > + complex > /\\ b: int + reversed< T3 >'
        )
        result = assignment.filter_pytypes(builtin_types)
        expected_result = Assignment.from_str(
            'a:int + float + list< set < T1 > > + list< complex > /\\ b: int'
        )
        self.assertEqual(result, expected_result)

    def test_relation_filter_pytypes_1(self):
        relation = Relation.from_str(
            'T1 <= int + float + list< set < T1 > > + list< reversed< T2 > + complex >'
        )
        result = relation.filter_pytypes(builtin_types)
        expected_result = Relation.from_str(
            'T1 <= int + float + list< set < T1 > > + list< complex >'
        )
        self.assertEqual(result, expected_result)

    def test_andconstraints_filter_pytypes_1(self):
        andconstr = AndConstraints.from_str(
            r'T1 <= int + float + list< set< T1 > > + list< reversed< T2 > + complex > /\ '
            r'T2 <= reversed< T3 > + float'
        )
        result = andconstr.filter_pytypes(builtin_types)
        expected_result = AndConstraints.from_str(
            'T1 <= int + float + list< set < T1 > > + list< complex > /\\ T2 <= float'
        )
        self.assertEqual(result, expected_result)

    def test_state_filter_pytypes_1(self):
        state = State.from_str(
            '((a:reversed< Ta > + int /\\ b:complex + float) ^ (Ta <= reversed< T1 > + list< int >))'
        )
        result = state.filter_pytypes(builtin_types)
        expected_result = State.from_str(
            '((a: int /\\ b:complex + float) ^ (Ta <= list< int >))'
        )
        self.assertEqual(result, expected_result)

    def test_stateset_filter_pytypes_1(self):
        stateset = StateSet.from_str(
            '((a:reversed< Ta > + int /\\ b:complex + float) ^ (Ta <= reversed< T1 > + list< int >)) \\/ '
            '(a:int /\\ b:reversed + float)'
        )
        result = stateset.filter_pytypes(builtin_types)
        expected_result = StateSet.from_str(
            '((a: int /\\ b:complex + float) ^ (Ta <= list< int >)) \\/ '
            '(a:int /\\ b:float)'
        )
        self.assertEqual(result, expected_result)

    def test_funcspec_filter_pytypes_1(self):
        funcspec = FuncSpec.from_str(
            '((a:reversed< Ta > + int /\\ b:complex + float) -> (return: reversed + complex))'
        )
        result = funcspec.filter_pytypes(builtin_types)
        expected_result = FuncSpec.from_str(
            '((a:int /\\ b:complex + float) -> (return: complex))'
        )
        self.assertEqual(result, expected_result)

    def test_visit_Tuple_1(self):
        expr = '(2, 3.5)'
        state_set = StateSet.from_str(
            r'(a:Ta /\ b:Tb) \/ (a:int /\ b:int)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:Ta /\ b:Tb /\ 2:int /\ 3.5:float /\ (2, 3.5):tuple< int + float >) \/ '
            r'(a:int /\ b:int /\ 2:int /\ 3.5:float /\ (2, 3.5):tuple< int + float >)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_Tuple_2(self):
        expr = '(a, b)'
        state_set = StateSet.from_str(
            r'(a:Ta /\ b:Tb) \/ (a:int /\ b:int)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:Ta /\ b:Tb /\ (a, b): tuple< Ta + Tb >) \/ (a:int /\ b:int /\ (a, b): tuple< int >)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_List_1(self):
        expr = '[2, 3.5]'
        state_set = StateSet.from_str(
            r'(a:Ta /\ b:Tb) \/ (a:int /\ b:int)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:Ta /\ b:Tb /\ 2:int /\ 3.5:float /\ [2, 3.5]:list< int + float >) \/ '
            r'(a:int /\ b:int /\ 2:int /\ 3.5:float /\ [2, 3.5]:list< int + float >)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_List_2(self):
        expr = '[a, b]'
        state_set = StateSet.from_str(
            r'(a:Ta /\ b:Tb) \/ (a:int /\ b:int)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:Ta /\ b:Tb /\ [a, b]: list< Ta + Tb >) \/ (a:int /\ b:int /\ [a, b]: list< int >)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_Set_1(self):
        expr = '{2, 3.5}'
        state_set = StateSet.from_str(
            r'(a:Ta /\ b:Tb) \/ (a:int /\ b:int)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:Ta /\ b:Tb /\ 2:int /\ 3.5:float /\ {2, 3.5}:set< int + float >) \/ '
            r'(a:int /\ b:int /\ 2:int /\ 3.5:float /\ {2, 3.5}:set< int + float >)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_Set_2(self):
        expr = '{a, b}'
        state_set = StateSet.from_str(
            r'(a:Ta /\ b:Tb) \/ (a:int /\ b:int)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:Ta /\ b:Tb /\ {a, b}: set< Ta + Tb >) \/ (a:int /\ b:int /\ {a, b}: set< int >)'
        )
        self.assertEqual(result, expected_result)
    
    def test_visit_add_1(self):
        expr = 'a + b'
        state_set = StateSet.from_str(
            r'(a:Ta /\ b:Tb)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'((a:Ta /\ b:Tb /\ (a + b):int) ^ (Ta <= int /\ Tb <= int)) \/ '
            r'((a:Ta /\ b:Tb /\ (a + b):tuple< T1 >) ^ (Ta <= tuple< T1 > /\ Tb <= tuple< T1 >)) \/ '
            r'((a:Ta /\ b:Tb /\ (a + b):bytearray) ^ (Ta <= bytearray /\ Tb <= bytearray + bytes + memoryview)) \/ '
            r'((a:Ta /\ b:Tb /\ (a + b):float) ^ (Ta <= float /\ Tb <= float)) \/ '
            r'((a:Ta /\ b:Tb /\ (a + b):bytes) ^ (Ta <= bytes /\ Tb <= bytearray + bytes + memoryview)) \/ '
            r'((a:Ta /\ b:Tb /\ (a + b):tuple< T1 + T2 >) ^ (Ta <= tuple< T1 > /\ Tb <= tuple< T2 >)) \/ '
            r'((a:Ta /\ b:Tb /\ (a + b):list< T1 + T2 >) ^ (Ta <= list< T1 > /\ Tb <= list< T2 >)) \/ '
            r'((a:Ta /\ b:Tb /\ (a + b):str) ^ (Ta <= str /\ Tb <= str)) \/ '
            r'((a:Ta /\ b:Tb /\ (a + b):complex) ^ (Ta <= complex /\ Tb <= complex)) \/ '
            r'((a:Ta /\ b:Tb /\ (a + b):list< T1 >) ^ (Ta <= list< T1 > /\ Tb <= list< T1 >))'
        )
        self.assertEqual(result, expected_result)
        # self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_replace_superclasses_1(self):
        state_set = StateSet.from_str(r'__obj:Sized')
        result = state_set.replace_superclasses()
        expected_result = StateSet.from_str(
            r'__obj:memoryview + range + bytes + str + bytearray + list< top > + set< top > + '
            r'tuple< top > + frozenset< top > + dict< top, top >'
        )
        self.assertEqual(result, expected_result)

    def test_basetype_get_builtin_1(self):
        bt = Basetype.from_str(r'Iterable< T1 >')
        result = bt.get_builtin_from_bt()
        expected_result = Basetype.from_str(
            r'list< T1 > + set< T1 > + frozenset< T1 > + tuple< T1 > '
        )
        self.assertEqual(result, expected_result)

    def test_basetype_get_builtin_2(self):
        bt = Basetype.from_str(r'Iterable< top >')
        result = bt.get_builtin_from_bt()
        expected_result = Basetype.from_str(
            r'list< top > + set< top > + frozenset< top > + tuple< top > + '
            r'str + memoryview + bytes + bytearray + range'
        )
        self.assertEqual(result, expected_result)

    def test_basetype_get_builtin_3(self):
        bt = Basetype.from_str(r'Iterable')
        result = bt.get_builtin_from_bt()
        expected_result = Basetype.from_str(
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
            FuncSpec.from_str(
                r'((__obj:Sized) -> (return:int))'
            )
        )
        self.assertEqual(result, expected_result)

    def test_substitute_call_state_arguments_1(self):
        expr = 'len(a)'
        call_node = ast.parse(expr).body[0].value
        state = State.from_str(r'(a:int+float /\ b:int+float)')
        result = substitute_state_arguments(call_node)
        param_instantiated = FuncSpec.from_str(
            r'((a:Sized) -> (len(a):int))'
        )
        expected_result = hset()
        expected_result.add(param_instantiated)
        self.assertEqual(result, expected_result)

    def test_visit_Call_1(self):
        expr = 'len(a)'
        state_set = StateSet.from_str(r'(a:int+float /\ b:int+float)')
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'((a:T1 /\ b:int+float /\ len(a):int) ^ (T1 <= int + float /\ T1 <= Sized))'
        )
        self.assertEqual(result, expected_result)

    def test_visit_Call_2(self):
        # def waldo(*args: Iterable[_KT] , **kwargs: Iterable[_VT]) -> bool: ...
        # callnode = ast.parse('waldo(a, b, c=x, d=y)').body[0].value
        expr = 'waldo(a, b, c=x, d=y)'
        state_set = StateSet.from_str(r'(a:int+float /\ b:int+float /\ x:float /\ y:str)')
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result_1 = StateSet.from_str(
            r'((a:T1 /\ b:T2 /\ x:T3 /\ y:T4 /\ waldo(a, b, c=x, d=y):bool) ^ '
            r'(T1 <= int + float /\ T1 <= T5 /\ T2 <= int+float /\ T2 <= T5 /\ '
            r'T3 <= float /\ T3 <= T6 /\ T4 <= str /\ T4 <= T6))'
        )
        expected_result_2 = StateSet.from_str(
            r'((a:T1 /\ b:T2 /\ x:T3 /\ y:T4 /\ waldo(a, b, c=x, d=y):bool) ^ '
            r'(T1 <= int + float /\ T1 <= T6 /\ T2 <= int+float /\ T2 <= T6 /\ '
            r'T3 <= float /\ T3 <= T5 /\ T4 <= str /\ T4 <= T5))'
        )
        res = StateSet.raw_eq(result, expected_result_1) or StateSet.raw_eq(result, expected_result_2)
        self.assertEqual(res, True)
    
    def test_visit_Call_3(self):
        expr = 'len(a)'
        state_set = StateSet.from_str(r'(a:T1)')
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'((a:T1 /\ len(a):int) ^ (T1 <= Sized))'
        )
        self.assertEqual(result, expected_result)

    def test_param_link_1(self):
        # def foo(a:int, b:int, /, c:int, *d:Any, e:int, f:int, **g:Any) -> bool: ...
        callnode = ast.parse('foo(h,i,j,k,l,m,n,e=o,f=p,w=q,x=r,y=s,z=t)').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, spec_set[0])
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
        fi = FunctionInstance(callnode, spec_set[0])
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
        fi = FunctionInstance(callnode, spec_set[0])
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
        fi = FunctionInstance(callnode, spec_set[0])
        result = fi.param_to_args()
        expected_result = {
            '__va_args': ['a', 'b', 'c', 'd'],
            '__kw_kwargs': {
                '__ko_e': 'x',
                '__ko_f': 'y'
            }
        }
        self.assertEqual(result, expected_result)
    
    def test_param_link_5(self):
        callnode = ast.parse('a+b').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, spec_set[0])
        result = fi.param_to_args()
        expected_result = {
            'self': 'a',
            '__value': 'b'
        }
        self.assertEqual(result, expected_result)

    def test_instantiate_spec_1(self):
        callnode = ast.parse('a>>b').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, spec_set[0])
        result = fi.instantiate_spec(astor.to_source(callnode).strip())
        expected_result = FuncSpec.from_str(
            r'((a:int /\ b:int) -> ((a >> b):int))'
        )
        self.assertEqual(result, expected_result)

    def test_instantiate_spec_2(self):
        # def corge(*args:Any, **kwargs:Any) -> bool: ...
        callnode = ast.parse('corge(a, b, c=x, d=y)').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, spec_set[0])
        result = fi.instantiate_spec(astor.to_source(callnode).strip())
        expected_result = FuncSpec.from_str(
            r'((a:top /\ b:top /\ x:top /\ y:top) -> (corge(a, b, c=x, d=y):bool))'
        )
        self.assertEqual(result, expected_result)

    def test_instantiate_spec_3(self):
        # def fred(*args:str, **kwargs:str) -> bool: ...
        callnode = ast.parse('fred(a, b, c=x, d=y)').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, spec_set[0])
        result = fi.instantiate_spec(astor.to_source(callnode).strip())
        expected_result = FuncSpec.from_str(
            r'((a:str /\ b:str /\ x:str /\ y:str) -> (fred(a, b, c=x, d=y):bool))'
        )
        self.assertEqual(result, expected_result)

    def test_instantiate_spec_4(self):
        # def thud(*args: _KT, **kwargs: _VT) -> bool: ...
        callnode = ast.parse('thud(a, b, c=x, d=y)').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, spec_set[0])
        result = fi.instantiate_spec(astor.to_source(callnode).strip())
        expected_result = FuncSpec.from_str(
            r'((a:top /\ b:top /\ x:top /\ y:top) -> (thud(a, b, c=x, d=y):bool))'
        )
        self.assertEqual(result, expected_result)

    def test_instantiate_spec_5(self):
        # def waldo(*args: Iterable[_KT] , **kwargs: Iterable[_VT]) -> bool: ...
        callnode = ast.parse('waldo(a, b, c=x, d=y)').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, spec_set[0])
        result = fi.instantiate_spec(astor.to_source(callnode).strip())
        expected_result = FuncSpec.from_str(
            r'((a:T?1 /\ b:T?1 /\ x:T?2 /\ y:T?2) -> (waldo(a, b, c=x, d=y):bool))'
        )
        self.assertEqual(result, expected_result)

    def test_state_apply_assign_1(self):
        state_set = StateSet.from_str(
            r'((a:Ta /\ b:Tb /\ c:Tc /\ d:Td) ^ (Ta <= Tb))'
        )
        code = 'a, b = c, d'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'((a:Tc /\ b:Td /\ c:Tc /\ d:Td /\ (c, d):tuple< Tc + Td >) ^ (Ta <= Tb))'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_2(self):
        state_set = StateSet.from_str(
            r'((a:Ta /\ b:Tb /\ c:list< Tc >) ^ (Ta <= Tb))'
        )
        code = 'a, b = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'((a:Tc /\ b:Tc /\ c:list< Tc >) ^ (Ta <= Tb))'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_3(self):
        state_set = StateSet.from_str(
            r'((a:Ta /\ b:Tb /\ c:int + list< float > + tuple< str > + str) ^ (Ta <= Tb))'
        )
        code = 'a, b = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'((a:float + str /\ b:float + str /\ c:list< float > + tuple< str > + str) ^ (Ta <= Tb))'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_4(self):
        state_set = StateSet.from_str(
            r'((a:Ta /\ b:Tb /\ c:int + list< float > + tuple< str > + str + Tc) ^ (Ta <= Tb))'
        )
        code = 'a, b = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'((a:float + str /\ b:float + str /\ c:list< float > + tuple< str > + str + Tc) ^ (Ta <= Tb /\ Tc <= Iterable< float + str >))'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_5(self):
        state_set = StateSet.from_str(
            r'((a:Ta /\ b:Tb /\ c:int + list< float > + tuple< str > + str + Tc) ^ (Ta <= Tb))'
        )
        code = 'a = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'((a:int + list< float > + tuple< str > + str + Tc /\ b:Tb /\ c:int + list< float > + tuple< str > + str + Tc) ^ (Ta <= Tb))'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_6(self):
        state_set = StateSet.from_str(
            r'((a:Ta /\ b:Tb /\ c:str) ^ (Ta <= Tb))'
        )
        code = 'a = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
           r'((a:str /\ b:Tb /\ c:str) ^ (Ta <= Tb))'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_5(self):
        state_set = StateSet.from_str(
            r'((a:Ta /\ b:Tb /\ c:int + list< float > + tuple< str > + str + Tc) ^ (Ta <= Tb))'
        )
        code = 'a = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'((a:int + list< float > + tuple< str > + str + Tc /\ b:Tb /\ c:int + list< float > + tuple< str > + str + Tc) ^ (Ta <= Tb))'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_6(self):
        state_set = StateSet.from_str(
            r'((a:Ta /\ b:Tb /\ c:str) ^ (Ta <= Tb))'
        )
        code = 'a = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
           r'((a:str /\ b:Tb /\ c:str) ^ (Ta <= Tb))'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    #a,b = 1,2.5
    def test_state_apply_assign_7(self):
        state_set = StateSet.from_str(
            r'(a:Ta /\ b:Tb)'
        )
        code = 'a,b = 1,2.5'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
           r'(a:int /\ b:float /\ 1:int /\ 2.5:float /\ (1, 2.5):tuple< int + float >)'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_8(self):
        state_set = StateSet.from_str(
            r'(a:Ta /\ b:Tb)'
        )
        code = 'a,b = [1,2.5]'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
           r'(a:int /\ b:float /\ 1:int /\ 2.5:float /\ [1, 2.5]:list< int + float >)'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_9(self):
        state_set = StateSet.from_str(
            r'(a:Ta /\ b:Tb)'
        )
        code = '[a,b] = [1,2.5]'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
           r'(a:int /\ b:float /\ 1:int /\ 2.5:float /\ [1, 2.5]:list< int + float >)'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_10(self):
        state_set = StateSet.from_str(
            r'(board:Tb /\ pos:Tp)'
        )
        code = 'row, column = pos'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'((board:Tb /\ pos:Tp /\ row:T1 /\ column:T2) ^ (Tp <= Iterable< T1 + T2 >))'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)
