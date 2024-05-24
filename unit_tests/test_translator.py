from testbase import *
# from statev2.Translator import *
from statev2.basetype import *


class TranslatorTestCases(unittest.TestCase):
    def test_pytype_from_str_1(self):
        result = PyType.from_str('list< int >')
        expected_result = PyType(list, Basetype({PyType(int)}))
        self.assertEqual(result, expected_result)

    def test_pytype_from_str_2(self):
        result = PyType.from_str('float')
        expected_result = PyType(float)
        self.assertEqual(result, expected_result)

    def test_vartype_from_str_1(self):
        result = PyType.from_str('T1')
        expected_result = VarType('T1')
        self.assertEqual(result, expected_result)

    def test_vartype_from_str_2(self):
        result = PyType.from_str('T?1')
        expected_result = VarType('T?1')
        self.assertEqual(result, expected_result)

    def test_translate_basetype_1(self):
        result = Basetype.from_str('int + float + list< T_a >')
        expected_result = Basetype({PyType(int), PyType(float), PyType(list, Basetype({VarType('T_a')}))})
        self.assertEqual(result, expected_result)

    def test_translate_basetype_2(self):
        result = Basetype.from_str('list< int + set< T1 > + list< T2 > >')
        expected_result = Basetype({
            PyType(
                list, Basetype({
                    PyType(int), PyType(set, Basetype({VarType('T1')})), PyType(list, Basetype({VarType('T2')}))
                })
            )
        })
        self.assertEqual(result, expected_result)

    def test_translate_basetype_3(self):
        result = Basetype.from_str('Sized')
        expected_result = Basetype({PyType(Sized)})
        self.assertEqual(result, expected_result)

    def test_translate_basetype_4(self):
        result = Basetype.from_str('Iterable< T1 >')
        expected_result = Basetype({
            PyType(Iterable, Basetype({VarType('T1')})),
        })
        self.assertEqual(result, expected_result)

    def test_translate_basetype_5(self):
        result = Basetype.from_str('Iterable< top >')
        expected_result = Basetype({
            PyType(Iterable, Basetype({PyType(TopType)})),
        })
        self.assertEqual(result, expected_result)
    
    def test_translate_basetype_6(self):
        result = Basetype.from_str('str')
        expected_result = Basetype({PyType(str)})
        self.assertEqual(result, expected_result)

    def test_translate_assignment(self):
        result = Assignment.from_str(r'(a:int+float /\ b:T_b)')
        expected_result = Assignment()
        expected_result['a'] = Basetype({PyType(int), PyType(float)})
        expected_result['b'] = Basetype({VarType('T_b')})
        self.assertEqual(result, expected_result)

    def test_translate_relop_1(self):
        result = Relation.from_str(r'T_a <= int')
        expected_result = Relation(RelOp.LEQ, Basetype({VarType('T_a')}), Basetype({PyType(int)}))
        self.assertEqual(result, expected_result)

    def test_translate_relop_2(self):
        result = Relation.from_str(r'T_a == int')
        expected_result = Relation(RelOp.EQ, Basetype({VarType('T_a')}), Basetype({PyType(int)}))
        self.assertEqual(result, expected_result)

    def test_translate_relop_3(self):
        result = Relation.from_str(r'T_b` <= int+float')
        expected_result = Relation(
            RelOp.LEQ,
            Basetype({VarType('T_b`')}),
            Basetype({PyType(int), PyType(float)})
        )
        self.assertEqual(result, expected_result)

    def test_translate_and_constr_1(self):
        result = AndConstraints.from_str(r'((T_a <= int) /\ (T_b == int+T_c+list<T_1>))')
        expected_result = AndConstraints()
        expected_result.add(Relation(RelOp.LEQ, Basetype({VarType('T_a')}), Basetype({PyType(int)})))
        expected_result.add(
            Relation(RelOp.EQ,
                     Basetype({VarType('T_b')}),
                     Basetype({PyType(int), VarType('T_c'), PyType(list, Basetype({VarType('T_1')}))})
                     )
        )
        self.assertEqual(result, expected_result)

    def test_translate_state_1(self):
        asgn = Assignment()
        asgn['a'] = Basetype({VarType('T_a')})
        asgn['b'] = Basetype({VarType('T_b')})
        and_constr = AndConstraints()
        and_constr.add(
            Relation(RelOp.LEQ, Basetype({VarType('T_a')}), Basetype({PyType(int)}))
        )
        and_constr.add(
            Relation(RelOp.LEQ, Basetype({VarType('T_a')}), Basetype({PyType(float)}))
        )
        and_constr.add(
            Relation(RelOp.LEQ, Basetype({VarType('T_b')}), Basetype({PyType(int), VarType('T_c')}))
        )
        and_constr.add(
            Relation(RelOp.EQ, Basetype({VarType('T_c')}), Basetype({PyType(float)}))
        )
        and_constr.add(
            Relation(RelOp.EQ, Basetype({VarType('T_c')}), Basetype({PyType(int)}))
        )
        expected_result = State(asgn, and_constr)
        str_state = (
            r'((a:T_a /\ b:T_b) ^ '
            r'((T_a <= int) /\ (T_a <= float) /\ (T_b <= int+T_c) /\ (T_c == float) /\ (T_c == int))'
            r')'
        )
        result = State.from_str(str_state)
        self.assertEqual(result, expected_result)

    def test_translate_state_2(self):
        result = State.from_str(r'(a:int /\ b:float)')
        asgn = Assignment()
        asgn['a'] = Basetype({PyType(int)})
        asgn['b'] = Basetype({PyType(float)})
        expected_result = State(assignment=asgn)
        self.assertEqual(result, expected_result)

    def test_translate_state_3(self):
        result = State.from_str(
            r'((a:T_a` /\ b:T_b`) ^ '
            r'((T_a` <= int+float) /\ (T_a` <= float) /\ (T_b` <= int+float) /\ (T_b` <= int))'
            r')'
        )
        expected_result = State()
        expected_result.assignment['a'] = Basetype({VarType('T_a`')})
        expected_result.assignment['b'] = Basetype({VarType('T_b`')})
        expected_result.constraints.add(
            Relation(
                RelOp.LEQ,
                Basetype({VarType('T_a`')}),
                Basetype({PyType(int), PyType(float)})
            )
        )
        expected_result.constraints.add(
            Relation(
                RelOp.LEQ,
                Basetype({VarType('T_a`')}),
                Basetype({PyType(float)})
            )
        )
        expected_result.constraints.add(
            Relation(
                RelOp.LEQ,
                Basetype({VarType('T_b`')}),
                Basetype({PyType(int), PyType(float)})
            )
        )
        expected_result.constraints.add(
            Relation(
                RelOp.LEQ,
                Basetype({VarType('T_b`')}),
                Basetype({PyType(int)})
            )
        )
        self.assertEqual(result, expected_result)

    def test_translate_state_set_1(self):
        result = StateSet.from_str(
            r'((a:T_a+float /\ b:T_b+int) ^ (T_b <= float /\ T_a <= str+complex)) \/ '
            r'((a:str /\ b:float))'
        )
        expected_result = StateSet()
        state = State()
        state.assignment['a'] = Basetype({VarType('T_a'), PyType(float)})
        state.assignment['b'] = Basetype({VarType('T_b'), PyType(int)})
        state.constraints.add(
            Relation(
                RelOp.LEQ,
                Basetype({VarType('T_b')}),
                Basetype({PyType(float)})
            )
        )
        state.constraints.add(
            Relation(
                RelOp.LEQ,
                Basetype({VarType('T_a')}),
                Basetype({PyType(str), PyType(complex)})
            )
        )
        expected_result.add(deepcopy(state))
        state = State()
        state.assignment['a'] = Basetype({PyType(str)})
        state.assignment['b'] = Basetype({PyType(float)})
        expected_result.add(deepcopy(state))
        self.assertEqual(result, expected_result)

    def test_translate_state_set_2(self):
        result = StateSet.from_str(r'((a:int /\ b:float))')
        expected_result = StateSet()
        state = State()
        state.assignment['a'] = Basetype({PyType(int)})
        state.assignment['b'] = Basetype({PyType(float)})
        expected_result.add(state)
        self.assertEqual(result, expected_result)

    def test_translate_state_set_3(self):
        result = StateSet.from_str(
            r'((self:complex /\ __value:complex /\ return:complex)) \/ '
            r'((self:float /\ __value:float /\ return:float)) \/ '
            r'((self:int /\ __value:int /\ return:float))'
        )
        expected_result = StateSet()
        state = State()
        state.assignment['self'] = Basetype({PyType(complex)})
        state.assignment['__value'] = Basetype({PyType(complex)})
        state.assignment['return'] = Basetype({PyType(complex)})
        expected_result.add(deepcopy(state))
        state = State()
        state.assignment['self'] = Basetype({PyType(float)})
        state.assignment['__value'] = Basetype({PyType(float)})
        state.assignment['return'] = Basetype({PyType(float)})
        expected_result.add(deepcopy(state))
        state = State()
        state.assignment['self'] = Basetype({PyType(int)})
        state.assignment['__value'] = Basetype({PyType(int)})
        state.assignment['return'] = Basetype({PyType(float)})
        expected_result.add(deepcopy(state))
        self.assertEqual(result, expected_result)

    def test_translate_spec_1(self):
        result = FuncSpec.from_str(r'((a:int /\ b:int) -> ((a+b):int))')
        expected_result = FuncSpec()
        expected_result.in_state.assignment['a'] = Basetype({PyType(int)})
        expected_result.in_state.assignment['b'] = Basetype({PyType(int)})
        expected_result.out_state.assignment['(a+b)'] = Basetype({PyType(int)})
        self.assertEqual(result, expected_result)
