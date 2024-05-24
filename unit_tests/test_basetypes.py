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
        state1 = State.from_str(r'a:int /\\ b:float')
        state2 = State.from_str(r'a:int /\\ b:float')
        result = state1 == state2
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_eq_state_2(self):
        state1 = State.from_str(r'((a:int /\\ b:float) ^ (T1 <= int))')
        state2 = State.from_str(r'a:int /\\ b:float')
        result = state1 == state2
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_eq_state_3(self):
        state1 = State.from_str(r'((a:int /\\ b:float) ^ (T1 <= int))')
        state2 = State.from_str(r'((a:int /\\ b:float) ^ (T1 <= int))')
        result = state1 == state2
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_eq_state_4(self):
        state1 = State.from_str(r'((a:int /\\ b:float) ^ (T1 <= int))')
        state2 = State.from_str(r'((a:int /\\ b:float) ^ (T1 <= float))')
        result = state1 == state2
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_eq_state_5(self):
        state1 = State.from_str(r'((a:int /\\ b:float) ^ (T1 <= int))')
        state2 = State.from_str(r'((a:int /\\ b:str) ^ (T1 <= int))')
        result = state1 == state2
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_eq_state_6(self):
        state1 = State.from_str(r'((a:int /\\ b:str /\\ c:complex) ^ (T1 <= int))')
        state2 = State.from_str(r'((a:int /\\ b:str) ^ (T1 <= int))')
        result = state1 == state2
        expected_result = False
        self.assertEqual(result, expected_result)
