import unittest
from Translator import Translator
from statev2.basetype import Basetype, Assignment, RelOp, Relation, AndConstraints, OrConstraints, State
from TypeExp import *


class TranslatorTestCases(unittest.TestCase):
    def test_translate_basetype(self):
        result = Translator.translate_basetype('int+float+list<T_a>')
        expected_result = Basetype({PyType(int), PyType(float), PyType(list, Basetype({VarType('T_a')}))})
        self.assertEqual(result, expected_result)

    def test_translate_assignment(self):
        result = Translator.translate_assignment(r'(a:int+float /\ b:T_b)')
        expected_result = Assignment()
        expected_result['a'] = Basetype({PyType(int), PyType(float)})
        expected_result['b'] = Basetype({VarType('T_b')})
        self.assertEqual(result, expected_result)

    def test_translate_relop_1(self):
        result = Translator.translate_relation(r'T_a <= int')
        expected_result = Relation(RelOp.LEQ, Basetype({VarType('T_a')}), Basetype({PyType(int)}))
        self.assertEqual(result, expected_result)

    def test_translate_relop_2(self):
        result = Translator.translate_relation(r'T_a == int')
        expected_result = Relation(RelOp.EQ, Basetype({VarType('T_a')}), Basetype({PyType(int)}))
        self.assertEqual(result, expected_result)

    def test_translate_or_constr_1(self):
        result = Translator.translate_or_constraints(
            r'(T_a+int <= T_a+float \/ T_a <= str+complex \/ T_a == str)'
        )
        expected_result = OrConstraints()
        expected_result.add(
            Relation(
                RelOp.LEQ,
                Basetype({VarType('T_a'), PyType(int)}),
                Basetype({VarType('T_a'), PyType(float)})
            )
        )
        expected_result.add(
            Relation(
                RelOp.LEQ,
                Basetype({VarType('T_a')}),
                Basetype({PyType(str), PyType(complex)})
            )
        )
        expected_result.add(
            Relation(
                RelOp.EQ,
                Basetype({'T_a'}),
                Basetype({PyType(str)})
            )
        )
        self.assertEqual(result, expected_result)

    def test_translate_and_constr_1(self):
        result = Translator.translate_and_constraints(r'((T_a <= int) /\ (T_b == int+T_c+list<T_1>))')
        expected_result = AndConstraints()
        orconstr = OrConstraints()
        orconstr.add(Relation(RelOp.LEQ, Basetype({VarType('T_a')}), Basetype({PyType(int)})))
        expected_result.add(orconstr)
        orconstr = OrConstraints()
        orconstr.add(
            Relation(RelOp.EQ,
                     Basetype({VarType('T_b')}),
                     Basetype({PyType(int), VarType('T_c'), PyType(list, Basetype({VarType('T_1')}))})
                     )
        )
        expected_result.add(orconstr)
        self.assertEqual(result, expected_result)

    def test_translate_and_constr_2(self):
        result = Translator.translate_and_constraints(
            r'((T_a <= int \/ T_a <= int+float) /\ (T_b == int+T_c+list<T_1> \/ T_b <= int))'
        )
        expected_result = AndConstraints()
        orconstr = OrConstraints()
        orconstr.add(Relation(RelOp.LEQ, Basetype({VarType('T_a')}), Basetype({PyType(int)})))
        orconstr.add(Relation(RelOp.LEQ, Basetype({VarType('T_a')}), Basetype({PyType(int), PyType(float)})))
        expected_result.add(orconstr)
        orconstr = OrConstraints()
        orconstr.add(
            Relation(RelOp.EQ,
                     Basetype({VarType('T_b')}),
                     Basetype({PyType(int), VarType('T_c'), PyType(list, Basetype({VarType('T_1')}))})
                     )
        )
        orconstr.add(
            Relation(RelOp.LEQ,
                     Basetype({VarType('T_b')}),
                     Basetype({PyType(int)})
                     )
        )
        expected_result.add(orconstr)
        self.assertEqual(result, expected_result)

    def test_translate_state(self):
        asgn = Assignment()
        asgn['a'] = Basetype({VarType('T_a')})
        asgn['b'] = Basetype({VarType('T_b')})
        orcons1 = OrConstraints()
        orcons1.add(
            Relation(RelOp.LEQ, Basetype({VarType('T_a')}), Basetype({PyType(int)}))
        )
        orcons1.add(
            Relation(RelOp.LEQ, Basetype({VarType('T_a')}), Basetype({PyType(float)}))
        )
        orcons2 = OrConstraints()
        orcons2.add(
            Relation(RelOp.LEQ, Basetype({VarType('T_b')}), Basetype({PyType(int), VarType('T_c')}))
        )
        orcons3 = OrConstraints()
        orcons3.add(
            Relation(RelOp.EQ, Basetype({VarType('T_c')}), Basetype({PyType(float)}))
        )
        orcons3.add(
            Relation(RelOp.EQ, Basetype({VarType('T_c')}), Basetype({PyType(int)}))
        )
        andcons1 = AndConstraints()
        andcons1.add(orcons1)
        andcons1.add(orcons2)
        andcons1.add(orcons3)
        expected_result = State(asgn, andcons1)
        str_state = (
            r'((a:T_a /\ b:T_b) ^ '
            r'((T_a <= int \/ T_a <= float) /\ (T_b <= int+T_c) /\ (T_c == float \/ T_c == int)))'
        )
        result = Translator.translate_state(str_state)
        self.assertEqual(result, expected_result)
