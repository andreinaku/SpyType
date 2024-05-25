from testbase import *
# from statev2.Translator import *
from statev2.basetype import *


class BasetypeTests(unittest.TestCase):
    def test_contains_atom_1(self):
        bt = Basetype.from_str('int + float + str')
        atom = PyType.from_str('int')
        result = bt.contains_atom(atom, False)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_atom_2(self):
        bt = Basetype.from_str('int + float + str')
        atom = PyType.from_str('complex')
        result = bt.contains_atom(atom, False)
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_contains_atom_3(self):
        bt = Basetype.from_str('list< int + float > + str')
        atom = PyType.from_str('int')
        result = bt.contains_atom(atom, False)
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_contains_atom_4(self):
        bt = Basetype.from_str('list< int + float > + str')
        atom = PyType.from_str('int')
        result = bt.contains_atom(atom, True)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_atom_5(self):
        bt = Basetype.from_str('int + float + str + T1')
        atom = VarType.from_str('T1')
        result = bt.contains_atom(atom, False)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_atom_6(self):
        bt = Basetype.from_str('int + float + str + T1')
        atom = VarType.from_str('T2')
        result = bt.contains_atom(atom, False)
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_contains_atom_7(self):
        bt = Basetype.from_str('int + tuple< float + str + list< T1 > >')
        atom = VarType.from_str('T1')
        result = bt.contains_atom(atom, True)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_atom_8(self):
        bt = Basetype.from_str('int + tuple< float + str + list< T1 > >')
        atom = VarType.from_str('T2')
        result = bt.contains_atom(atom, True)
        expected_result = False
        self.assertEqual(result, expected_result)
    
    def test_contains_basetype_1(self):
        bt1 = Basetype.from_str('int + float')
        bt2 = Basetype.from_str('int + float')
        result = bt1.contains_basetype(bt2) and (bt2 <= bt1)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_basetype_2(self):
        bt1 = Basetype.from_str('int + float')
        bt2 = Basetype.from_str('int + float + str')
        result = bt1.contains_basetype(bt2) and (bt2 <= bt1)
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_contains_basetype_3(self):
        bt1 = Basetype.from_str('int + float + str')
        bt2 = Basetype.from_str('int + float')
        result = bt1.contains_basetype(bt2) and (bt2 <= bt1)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_basetype_4(self):
        bt1 = Basetype.from_str('int + float + list< int + float + str >')
        bt2 = Basetype.from_str('int + float + str')
        result = bt1.contains_basetype(bt2, True)
        expected_result = True
        self.assertEqual(result, expected_result)
    
    def test_contains_basetype_5(self):
        bt1 = Basetype.from_str('int + float + list< int + float + str >')
        bt2 = Basetype.from_str('complex + str')
        result = bt1.contains_basetype(bt2, True)
        expected_result = False
        self.assertEqual(result, expected_result)
    
    def test_contains_basetype_6(self):
        bt1 = Basetype.from_str('int + float + list< tuple < complex + str > + int >')
        bt2 = Basetype.from_str('complex + str')
        result = bt1.contains_basetype(bt2, True)
        expected_result = True
        self.assertEqual(result, expected_result)
    
    def test_contains_basetype_7(self):
        bt1 = Basetype.from_str('int + float + list< tuple < complex + T1 > + int >')
        bt2 = Basetype.from_str('complex + T1')
        result = bt1.contains_basetype(bt2, True)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_basetype_8(self):
        bt1 = Basetype.from_str('int + float + list< tuple < complex + T1 > + int >')
        bt2 = Basetype.from_str('complex + T2')
        result = bt1.contains_basetype(bt2, True)
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_eq_1(self):
        bt1 = Basetype.from_str('int + float + list< tuple < complex + T1 > + int >')
        bt2 = Basetype.from_str('complex + T2')
        result = bt1 == bt2
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_eq_2(self):
        bt1 = Basetype.from_str('int + float + list< tuple < complex + T1 > + int >')
        bt2 = Basetype.from_str('int + float + list< tuple < complex + T1 > + int >')
        result = bt1 == bt2
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_eq_3(self):
        bt1 = Basetype.from_str('int')
        bt2 = Basetype.from_str('int')
        result = bt1 == bt2
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_eq_4(self):
        bt1 = Basetype.from_str('int + float')
        bt2 = Basetype.from_str('float + int')
        result = bt1 == bt2
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_replace_basetype_1(self):
        bt = Basetype.from_str('int + float + str')
        bt1 = Basetype.from_str('float')
        bt2 = Basetype.from_str('list< int >')
        result = bt.replace_basetype(bt1, bt2)
        expected_result = Basetype.from_str('int + str + list< int >')
        self.assertEqual(result, expected_result)

    def test_replace_basetype_2(self):
        bt = Basetype.from_str('int + list< float > + str + float')
        bt1 = Basetype.from_str('float')
        bt2 = Basetype.from_str('list< int >')
        result = bt.replace_basetype(bt1, bt2)
        expected_result = Basetype.from_str('list< int > + int + str + list< list< int > >')
        self.assertEqual(result, expected_result)

    def test_replace_basetype_3(self):
        bt = Basetype.from_str('int + list< float > + str + float')
        bt1 = Basetype.from_str('float')
        bt2 = Basetype.from_str('float')
        result = bt.replace_basetype(bt1, bt2)
        expected_result = bt
        self.assertEqual(result, expected_result)

    def test_replace_basetype_4(self):
        bt = Basetype.from_str('int + T1 + list< float + T1 > + str + float')
        bt1 = Basetype.from_str('float + T1')
        bt2 = Basetype.from_str('float + complex + int')
        result = bt.replace_basetype(bt1, bt2)
        expected_result = Basetype.from_str('list< float + complex + int > + str + float + complex + int')
        self.assertEqual(result, expected_result)

    def test_replace_basetype_5(self):
        bt = Basetype.from_str('int + list< float > + str + float')
        bt1 = Basetype.from_str('float')
        bt2 = Basetype.from_str('list< float >')
        result = bt.replace_basetype(bt1, bt2)
        expected_result = Basetype.from_str('int + list< list< float > > + str + list< float >')
        self.assertEqual(result, expected_result)

    def test_eq_assignment_1(self):
        asg1 = Assignment.from_str('a:int /\\ b:float')
        asg2 = Assignment.from_str('a:int /\\ b:float')
        result = asg1 == asg2
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_eq_assignment_2(self):
        asg1 = Assignment.from_str('a:int /\\ b:float')
        asg2 = Assignment.from_str('a:int /\\ b:int + float')
        result = asg1 == asg2
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_eq_assignment_3(self):
        asg1 = Assignment.from_str('a:int /\\ c:float')
        asg2 = Assignment.from_str('a:int /\\ b:float')
        result = asg1 == asg2
        expected_result = False
        self.assertEqual(result, expected_result)
    
    def test_eq_assignment_4(self):
        asg1 = Assignment.from_str('a:int')
        asg2 = Assignment.from_str('a:int /\\ b:float')
        result = asg1 == asg2
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_eq_state_1(self):
        state1 = State.from_str('a:int /\\ b:float')
        state2 = State.from_str('a:int /\\ b:float')
        result = state1 == state2
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_eq_state_2(self):
        state1 = State.from_str('((a:int /\\ b:float) ^ (T1 <= int))')
        state2 = State.from_str('a:int /\\ b:float')
        result = state1 == state2
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_eq_state_3(self):
        state1 = State.from_str('((a:int /\\ b:float) ^ (T1 <= int))')
        state2 = State.from_str('((a:int /\\ b:float) ^ (T1 <= int))')
        result = state1 == state2
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_eq_state_4(self):
        state1 = State.from_str('((a:int /\\ b:float) ^ (T1 <= int))')
        state2 = State.from_str('((a:int /\\ b:float) ^ (T1 <= float))')
        result = state1 == state2
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_eq_state_5(self):
        state1 = State.from_str('((a:int /\\ b:float) ^ (T1 <= int))')
        state2 = State.from_str('((a:int /\\ b:str) ^ (T1 <= int))')
        result = state1 == state2
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_eq_state_6(self):
        state1 = State.from_str(r'((a:int /\ b:str /\ c:complex) ^ (T1 <= int))')
        state2 = State.from_str(r'((a:int /\ b:str) ^ (T1 <= int))')
        result = state1 == state2
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_relation_replace_basetype_1(self):
        rel = Relation.from_str('T1 <= int + str')
        result = rel.replace_basetype(Basetype.from_str('T1'), Basetype.from_str('str + complex'))
        expected_result = Relation.from_str('str + complex <= int + str')
        self.assertEqual(result, expected_result)

    def test_relation_replace_basetype_2(self):
        rel = Relation.from_str('T1 <= int + str')
        result = rel.replace_basetype(Basetype.from_str('int + str'), Basetype.from_str('str + int'))
        # expected_result = Relation.from_str('str + complex <= int + str')
        self.assertEqual(result, rel)

    def test_relation_replace_basetype_3(self):
        rel = Relation.from_str('T1 <= int + str')
        result = rel.replace_basetype(Basetype.from_str('int + str'), Basetype.from_str('list< str + int >'))
        expected_result = Relation.from_str('T1 <= list< int + str >')
        self.assertEqual(result, expected_result)

    def test_assignment_replace_basetype_1(self):
        assig = Assignment.from_str(r'a:int + T1 /\ b:str + float /\ c:T2')
        result = assig.replace_basetype(Basetype.from_str('T1'), Basetype.from_str('str + complex'))
        expected_result = Assignment.from_str(r'a:int + str + complex /\ b:str + float /\ c:T2')
        self.assertEqual(result, expected_result)
    
    def test_andconstraints_replace_basetype_1(self):
        andconstr = AndConstraints.from_str(r'((T1 <= int + str) /\ (T2 <= float))')
        result = andconstr.replace_basetype(Basetype.from_str('T2'), Basetype.from_str('float'))
        expected_result = AndConstraints.from_str(r'((T1 <= int + str) /\ (float <= float))')
        self.assertEqual(result, expected_result)

    def test_state_replace_basetype_1(self):
        state = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T1 <= float /\ T2 <= T1 + complex))'
        )
        result = state.replace_basetype(Basetype.from_str('T1'), Basetype.from_str('str'))
        expected_result = State.from_str(
            r'((a:str /\ b:T2) ^ (str <= int /\ str <= float /\ T2 <= str + complex))'
        )
        self.assertEqual(result, expected_result)

    def test_stateset_replace_basetype_1(self):
        stateset = StateSet.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T1 <= float /\ T2 <= T1 + complex)) \/ '
            r'((a:T1 /\ b:T2) ^ (T1 <= str /\ T2 <= str))'
        )
        result = stateset.replace_basetype(Basetype.from_str('T1'), Basetype.from_str('str'))
        expected_result = StateSet.from_str(
            r'((a:str /\ b:T2) ^ (str <= int /\ str <= float /\ T2 <= str + complex)) \/ '
            r'((a:str /\ b:T2) ^ (str <= str /\ T2 <= str))'
        )
        self.assertEqual(result, expected_result)
