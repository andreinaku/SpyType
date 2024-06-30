from testbase import *
from statev2.transfer import *
from pyiparser_2 import VARTYPE_REPLACE, builtin_types
from typing import *
from statev2.function_instance import FunctionInstance


class SpecTestCases(unittest.TestCase):

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
                FuncSpec.from_str(r'((a:complex /\ b:complex) -> (a / b:complex))'),
                FuncSpec.from_str(r'((a:float /\ b:float) -> (a / b:float))'),
                FuncSpec.from_str(r'((a:int /\ b:int) -> (a / b:float))')
            }
        )
        self.assertEqual(result, expected_result)

    def _test_set_apply_binop_spec_1(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state_set = StateSet.from_str(r'(a:T1 /\ b:T2)')
        # result = set_apply_binop_spec(state_set, binop_node, testmode=True)
        result = set_apply_specset(state_set, binop_node, testmode=True)
        expected_result = StateSet.from_str(
            r'(a:complex /\ b:complex /\ a / b:complex) \/ ' \
            r'(a:float /\ b:float /\ a / b:float) \/ ' \
            r'(a:int /\ b:int /\ a / b:float)'
        )
        self.assertEqual(result, expected_result)

    def _test_set_apply_binop_spec_2(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state_set = StateSet.from_str(
            r'(a:int + float /\ b:int + float) \/ '
            r'(a:str /\ b:str)'
        )
        result = set_apply_specset(state_set, binop_node)
        expected_result = StateSet.from_str(
            r'(a:int /\ b:int /\ a / b:float) \/ '
            r'(a:float /\ b:float /\ a / b:float)'
        )
        self.assertEqual(result, expected_result)

    def _test_set_apply_binop_spec_3(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state_set = StateSet.from_str(
            r'(a:str /\ b:str)'
        )
        result = set_apply_specset(state_set, binop_node)
        expected_result = StateSet()
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_1(self):
        expr = 'a / b'
        state_set = StateSet.from_str(
            r'(a:str /\ b:str)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet()
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_2(self):
        expr = '(a >> b) / c'
        state_set = StateSet.from_str(
            r'(a:T1 /\ b:T2 /\ c:T3)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:int /\ b:int /\ c:int /\ a >> b:int /\ (a >> b) / c:float)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_3(self):
        state = State.from_str(r'(a:T1 /\ b:T2)')
        state_set = StateSet()
        state_set.add(deepcopy(state))
        code = 'a >> b'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:int /\ b:int /\ a >> b:int)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_4(self):
        state_set = StateSet.from_str(r'(a:list< T1 + T2 > /\ b:list< T3 >)')
        code = 'a + b'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:list< T1 + T2 > /\ b:list< T3 > /\ a + b:list< T1 + T2 + T3 >)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_5(self):
        state_set = StateSet.from_str(r'(a:T1 /\ b:T2 /\ c:T3)')
        code = 'a + b + c'
        # code = 'a + b'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:int /\ b:int /\ c:int /\ a + b:int /\ a + b + c:int) \/ ' \
            r'(a:float /\ b:float /\ c:float /\ a + b:float /\ a + b + c:float) \/ ' \
            r'(a:complex /\ b:complex /\ c:complex /\ a + b:complex /\ a + b + c:complex) \/ ' \
            r'(a:str /\ b:str /\ c:str /\ a + b:str /\ a + b + c:str) \/ ' \
            r'(a:bytes /\ b:bytes + memoryview + bytearray /\ c:bytes + memoryview + bytearray /\ ' \
                r'a + b:bytes /\ a + b + c:bytes) \/ ' \
            r'(a:tuple< T1 > /\ b:tuple< T1 > /\ c:tuple< T1 > /\ a + b:tuple< T1 > /\ a + b + c:tuple< T1 >) \/ ' \
            r'(a:tuple< T1 > /\ b:tuple< T1 > /\ c:tuple< T2 > /\ a + b:tuple< T1 > /\ a + b + c:tuple< T1 + T2 >) \/ ' \
            r'(a:tuple< T1 > /\ b:tuple< T2 > /\ c:tuple< T1 + T2 > /\ a + b:tuple< T1 + T2 > /\ a + b + c:tuple< T1 + T2 >) \/ ' \
            r'(a:tuple< T1 > /\ b:tuple< T2 > /\ c:tuple< T3 > /\ a + b:tuple< T1 + T2 > /\ a + b + c:tuple< T1 + T2 + T3 >) \/ ' \
            r'(a:list< T1 > /\ b:list< T1 > /\ c:list< T1 > /\ a + b:list< T1 > /\ a + b + c:list< T1 >) \/ ' \
            r'(a:list< T1 > /\ b:list< T1 > /\ c:list< T2 > /\ a + b:list< T1 > /\ a + b + c:list< T1 + T2 >) \/ ' \
            r'(a:list< T1 > /\ b:list< T2 > /\ c:list< T1 + T2 > /\ a + b:list< T1 + T2 > /\ a + b + c:list< T1 + T2 >) \/ ' \
            r'(a:list< T1 > /\ b:list< T2 > /\ c:list< T3 > /\ a + b:list< T1 + T2 > /\ a + b + c:list< T1 + T2 + T3 >) \/ ' \
            r'(a:bytearray /\ b:bytes + memoryview + bytearray /\ c:bytes + memoryview + bytearray /\ ' \
                r'a + b:bytearray /\ a + b + c:bytearray)'
        )
        # expected_result = StateSet.from_str(
        #     r'(a:list< T1 > /\ b:list< T2 > /\ c:list< T3 > /\ a + b:list< T1 + T2 > /\ a + b + c:list< T1 + T2 + T3 >)'
        # )
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
            r'(a:T1 /\ b:T2) \/ (a:int /\ b:int)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:T1 /\ b:T2 /\ {a, b}: set< T1 + T2 >) \/ (a:int /\ b:int /\ {a, b}: set< int >)'
        )
        self.assertEqual(result, expected_result)
    
    def test_visit_add_1(self):
        expr = 'a + b'
        state_set = StateSet.from_str(
            r'(a:T1 /\ b:T2)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:int /\ b:int /\ a + b:int) \/ '\
            r'(a:float /\ b:float /\ a + b:float) \/ '\
            r'(a:complex /\ b:complex /\ a + b:complex) \/ '\
            r'(a:list< T1 > /\ b:list< T1 > /\ a + b:list< T1 >) \/ '\
            r'(a:list< T1 > /\ b:list< T2 > /\ a + b:list< T1 + T2 >) \/ '\
            r'(a:tuple< T1 > /\ b:tuple< T1 > /\ a + b:tuple< T1 >) \/ '\
            r'(a:tuple< T1 > /\ b:tuple< T2 > /\ a + b:tuple< T1 + T2 >) \/ '\
            r'(a:bytes /\ b:bytearray + bytes + memoryview /\ a + b:bytes) \/ '\
            r'(a:str /\ b:str /\ a + b:str) \/ '\
            r'(a:bytearray /\ b:bytearray + bytes + memoryview /\ a + b:bytearray)'
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
            r'list< T1 > + set< T1 > + frozenset< T1 > + tuple< T1 >'
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
        expected_result = StateSet()
        self.assertEqual(result, expected_result)
    
    def test_visit_Call_4(self):
        expr = 'len(a)'
        state_set = StateSet.from_str(r'(a:int+float+list<int>+set<float> /\ b:int+float)')
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:list< int > + set< float > /\ b:int + float /\ len(a):int)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_Call_2(self):
        # def waldo(*args: Iterable[_KT] , **kwargs: Iterable[_VT]) -> bool: ...
        # callnode = ast.parse('waldo(a, b, c=x, d=y)').body[0].value
        expr = 'waldo(a, b, c=x, d=y)'
        # state_set = StateSet.from_str(r'(a:int+float /\ b:int+float /\ x:float /\ y:str)')
        state_set = StateSet.from_str(r'(a:float /\ b:int /\ x:float /\ y:str)')
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:float /\ b:int /\ x:float /\ y:str /\ waldo(a, b, c=x, d=y):bool /\ (a, b):tuple < int + float > /\ (x, y):tuple < str + float >)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_Call_5(self):
        # def waldo(*args: Iterable[_KT] , **kwargs: Iterable[_VT]) -> bool: ...
        # callnode = ast.parse('waldo(a, b, c=x, d=y)').body[0].value
        expr = 'waldo(a, b, c=x, d=y)'
        state_set = StateSet.from_str(r'(a:int+float /\ b:int+float /\ x:float /\ y:str)')
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:int+float /\ b:int+float /\ x:float /\ y:str /\ waldo(a, b, c=x, d=y):bool /\ '
            r'(a, b):tuple < int + float > /\ (x, y):tuple < str + float >)'
        )
        self.assertEqual(result, expected_result)
    
    def test_visit_Call_3(self):
        expr = 'len(a)'
        state_set = StateSet.from_str(r'(a:T1)')
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'((a:range + str + bytes + bytearray + memoryview + set < top > + frozenset < top > + '
            r'list < top > + tuple < top > + dict < top, top > /\ len(a):int))'
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
        result = fi.instantiate_spec()
        expected_result = FuncSpec.from_str(
            r'((a:int /\ b:int) -> (a >> b:int))'
        )
        self.assertEqual(result, expected_result)

    def test_instantiate_spec_2(self):
        # def corge(*args:Any, **kwargs:Any) -> bool: ...
        callnode = ast.parse('corge(a, b, c=x, d=y)').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, spec_set[0])
        result = fi.instantiate_spec()
        # expected_result = FuncSpec.from_str(
        #     r'((a:top /\ b:top /\ x:top /\ y:top) -> (corge(a, b, c=x, d=y):bool))'
        # )
        expected_result = FuncSpec.from_str(
            r'(((a, b):tuple < top >  /\ (x, y):tuple < top >) -> (corge(a, b, c=x, d=y):bool))'
        )
        self.assertEqual(result, expected_result)

    def test_instantiate_spec_3(self):
        # def fred(*args:str, **kwargs:str) -> bool: ...
        callnode = ast.parse('fred(a, b, c=x, d=y)').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, spec_set[0])
        result = fi.instantiate_spec()
        # expected_result = FuncSpec.from_str(
        #     r'((a:str /\ b:str /\ x:str /\ y:str) -> (fred(a, b, c=x, d=y):bool))'
        # )
        expected_result = FuncSpec.from_str(
            r'(((a, b):tuple < str > /\ (x, y):tuple < str >) -> (fred(a, b, c=x, d=y):bool))'
        )
        self.assertEqual(result, expected_result)

    def test_instantiate_spec_5(self):
        # def waldo(*args: Iterable[_KT] , **kwargs: Iterable[_VT]) -> bool: ...
        callnode = ast.parse('waldo(a, b, c=x, d=y)').body[0].value
        spec_set = get_specset(callnode)
        fi = FunctionInstance(callnode, spec_set[0])
        result = fi.instantiate_spec()
        # expected_result = FuncSpec.from_str(
        #     r'((a:T?1 /\ b:T?1 /\ x:T?2 /\ y:T?2) -> (waldo(a, b, c=x, d=y):bool))'
        # )
        expected_result = FuncSpec.from_str(
            r'(((a, b): tuple < T?1 > /\ (x, y):tuple < T?2 >) -> (waldo(a, b, c=x, d=y):bool))'
        )
        self.assertEqual(result, expected_result)

    def test_state_apply_assign_1(self):
        state_set = StateSet.from_str(
            r'((a:T1 /\ b:T2 /\ c:T3 /\ d:T4) ^ (T1 <= T2))'
        )
        code = 'a, b = c, d'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:T3 /\ b:T4 /\ c:T3 /\ d:T4 /\ (c, d):tuple< T3 + T4 >)'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_2(self):
        state_set = StateSet.from_str(
            r'(a:T1 /\ b:T2 /\ c:list< T3 >)'
        )
        code = 'a, b = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:T3 /\ b:T3 /\ c:list< T3 >)'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_3(self):
        state_set = StateSet.from_str(
            r'((a:T1 /\ b:T2 /\ c:int + list< float > + tuple< str > + str) ^ (T1 <= T2))'
        )
        code = 'a, b = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:float + str /\ b:float + str /\ c:str + list< float > + tuple< str >)'
        )
        self.assertEqual(result, expected_result)

    def test_state_apply_assign_16(self):
        state_set = StateSet.from_str(
            r'(a:T1 /\ b:T2 /\ c:str)'
        )
        code = 'a = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
           r'(a:str /\ b:T2 /\ c:str)'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_5(self):
        state_set = StateSet.from_str(
            r'((a:T1 /\ b:T2 /\ c:int + list< float > + tuple< str > + str + T3) ^ (T1 <= T2))'
        )
        code = 'a = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'((a:int + list< float > + tuple< str > + str + T3 /\ b:T2 /\ '
            r'c:int + list< float > + tuple< str > + str + T3))'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_state_apply_assign_6(self):
        state_set = StateSet.from_str(
            r'((a:T1 /\ b:T2 /\ c:str) ^ (T1 <= T2))'
        )
        code = 'a = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
           r'(a:str /\ b:T2 /\ c:str)'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    #a,b = 1,2.5
    def test_state_apply_assign_7(self):
        state_set = StateSet.from_str(
            r'(a:T1 /\ b:T2)'
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
            r'(a:T1 /\ b:T2)'
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
            r'(a:T1 /\ b:T2)'
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
            r'(row:bot /\ column:bot /\ board:T1 /\ pos:T2)'
        )
        code = 'row, column = pos'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'row:T3 + str /\ column:T4 + str /\ board:T1 /\ pos:str + list < T3 + T4 > + '
            r'set < T3 + T4 > + frozenset < T3 + T4 > + tuple < T3 + T4 >'
        )
        self.assertEqual(result, expected_result)
        # self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_stateset_remove_no_names_1(self):
        state_set = StateSet.from_str(
            r'a:int /\ b:int /\ (a + b): float /\ (a * b):int'
        )
        result = state_set.remove_no_names()
        expected_result = StateSet.from_str(
            r'a:int /\ b:int'
        )
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_6(self):
        ss = StateSet.from_str(r'(a:list<T1> /\ b:list<T2>) \/ (a:int /\ b:int)')
        expr = 'a - 1, b + 1'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:int /\ b:int /\ 1:int /\ a - 1:int /\ b + 1: int /\ (a - 1, b + 1):tuple<int>)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_7(self):
        ss = StateSet.from_str(r'(a:T1 /\ b:T2)')
        expr = 'a + b'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        ss = deepcopy(result)
        expr = 'a - 1, b + 1'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:int /\ b:int /\ a + b:int /\ 1:int /\ a - 1:int /\ b + 1: int /\ (a - 1, b + 1):tuple<int>)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_assign_1(self):
        ss = StateSet.from_str(r'a:T1 /\ b:T2')
        expr = 'a = b'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(r'a:T2 /\ b:T2')
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_visit_subscript_1(self):
        ss = StateSet.from_str(r'a:T1')
        expr = 'a[2] = 3'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        # expected_result = StateSet.from_str(r'a:T2 /\ b:T2')
        result = result.remove_no_names()
        expected_result = StateSet.from_str(
            r'(a:list < int + T1 >) \/ (a:set < int + T1 >) \/ (a:frozenset < int + T1 >) \/ '
            r'(a:tuple < int + T1 >) \/ (a:dict < T2, int + T1 >)'
        )
        # self.assertEqual(StateSet.raw_eq(result, expected_result), True)
        self.assertEqual(result, expected_result)

    def test_visit_assign_2(self):
        ss = StateSet.from_str(r'a:int /\ b:T1')
        expr = 'a = b'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(r'a:T1 /\ b:T1')
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_visit_assign_3(self):
        ss = StateSet.from_str(r'a:int /\ c:int /\ b:tuple < T1 >')
        # expr = 'simpleassign(b, a, c)'
        expr = 'a, c = b'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(r'a:T1 /\ c:T1 /\ b:tuple < T1 >')
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_visit_assign_4(self):
        ss = StateSet.from_str(r'a:int /\ b:int /\ c:float /\ d:str')
        # expr = 'simpleassign(b, a, c)'
        expr = 'a, b = c, d'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(r'a:float /\ b:str /\ c:float /\ d:str /\ (c, d):tuple < float + str >')
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_visit_assign_5(self):
        ss = StateSet.from_str(r'a:bot /\ b:T1')
        expr = 'a = b'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(r'a:T1 /\ b:T1')
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_visit_assign_6(self):
        ss = StateSet.from_str(r'a:T1 /\ b:T2 /\ c:T3 /\ d:T4')
        # expr = 'simpleassign(b, a, c)'
        expr = 'a, b = c, d'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(r'a:T3 /\ b:T4 /\ c:T3 /\ d:T4 /\ (c, d):tuple < T3 + T4 >')
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_visit_assign_7(self):
        ss = StateSet.from_str(r'a:bot /\ b:bot /\ c:T1')
        expr = 'a, b = c'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'a:T1 + str /\ b:T2 + str /\ c:tuple < T1 + T2 > + list < T1 + T2 > + set< T1 + T2 > + frozenset < T1 + T2 > + str'
        )
        # self.assertEqual(StateSet.raw_eq(result, expected_result), True)
        self.assertEqual(result, expected_result)

    def test_visit_assign_8(self):
        state_set = StateSet.from_str(
            r'(a:T1 /\ b:T2 /\ c:list < T3 >)'
        )
        code = 'a, b = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set

        expected_result = StateSet.from_str(
            r'(a:T3 /\ b:T3 /\ c:list< T3 >)'
        )
        # self.assertEqual(result, expected_result)
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_visit_assign_9(self):
        state_set = StateSet.from_str(
            r'(a:bot /\ b:bot /\ c:list < T3 >)'
        )
        code = 'a, b = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:T3 /\ b:T3 /\ c:list< T3 >)'
        )
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_visit_assign_10(self):
        state_set = StateSet.from_str(
            r'(a:T1 /\ b:T2 /\ c:list < T3 >)'
        )
        code = 'a, b = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:T3 /\ b:T3 /\ c:list< T3 >)'
        )
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_visit_assign_11(self):
        state_set = StateSet.from_str(
            r'(a:T1 /\ b:T2 /\ c:T3)'
        )
        code = 'a, b = c'
        node = ast.parse(code)
        tf = TransferFunc(state_set)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'(a:T1 + str /\ b:T2 + str /\ '
            r'c:list< T1 + T2 > + set< T1 + T2 > + frozenset< T1 + T2 > + tuple< T1 + T2 > + str)'
        )
        self.assertEqual(result, expected_result)

    def test_visit_subscript_2(self):
        ss = StateSet.from_str(r'a:T1 /\ b:T2 /\ c:T3')
        expr = 'a[b - 1, c + 1]'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        expected_result = None
        self.assertEqual(True, True)

    def test_visit_subscript_3(self):
        ss = StateSet.from_str(r'a:T1 /\ b:T2 /\ c:T3')
        expr = 'a[b, c]'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(
            r'a:dict < T2 + T3, T4 > /\ b:T2 /\ c:T3 /\ (b, c):tuple < T2 + T3 > /\ a[b, c]:T4'
        )
        self.assertEqual(result, expected_result)


    def _test_foo(self):
        ss = StateSet.from_str(r'a:T1 /\ 3:int')
        expr = 'subscriptassign(a, 3)'
        node = ast.parse(expr)
        tf = TransferFunc(ss)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet.from_str(r'a:T2 /\ b:T2')
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)
