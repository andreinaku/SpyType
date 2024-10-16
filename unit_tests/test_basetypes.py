from testbase import *
# from statev2.Translator import *
from statev2.basetype import *


class BasetypeTests(unittest.TestCase):
    def test_contains_atom_1(self):
        bt = Basetype.from_str('int + float + str')
        atom = PyType.from_str('int')
        result = atom in bt
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_atom_2(self):
        bt = Basetype.from_str('int + float + str')
        atom = PyType.from_str('complex')
        result = atom in bt
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_contains_atom_3(self):
        bt = Basetype.from_str('list< int + float > + str')
        atom = PyType.from_str('int')
        result = atom in bt
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_contains_atom_4(self):
        bt = Basetype.from_str('list< int + float > + str')
        atom = PyType.from_str('int')
        result = atom in bt
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_contains_atom_5(self):
        bt = Basetype.from_str('int + float + str + T1')
        atom = VarType.from_str('T1')
        result = atom in bt
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_atom_6(self):
        bt = Basetype.from_str('int + float + str + T1')
        atom = VarType.from_str('T2')
        result = atom in bt
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_contains_atom_7(self):
        bt = Basetype.from_str('int + tuple< float + str + list< T1 > >')
        atom = VarType.from_str('T1')
        result = atom in bt
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_contains_atom_8(self):
        bt = Basetype.from_str('int + tuple< float + str + list< T1 > >')
        atom = VarType.from_str('T2')
        result = atom in bt
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

    def test_basetype_le_1(self):
        bt1 = Basetype.from_str('int + float + str')
        bt2 = Basetype.from_str('int + float')
        result = bt1 <= bt2
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_basetype_le_2(self):
        bt1 = Basetype.from_str('int + float + str')
        bt2 = Basetype.from_str('int + float')
        result = bt2 <= bt1
        expected_result = True
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

    def test_eq_state_7(self):
        state1 = State.from_str(r'((a:T1 + T2 /\ b:T1) ^ (T1 <= T2))')
        state2 = State.from_str(r'((a:T3 + T4 /\ b:T4) ^ (T4 <= T3))')
        result = state1 == state2
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_eq_state_8(self):
        state1 = State.from_str(r'((a:T1 + T2 /\ b:T3) ^ (T3 <= T1))')
        state2 = State.from_str(r'((a:T4 + T5 /\ b:T6) ^ (T6 <= T5))')
        result = state1 == state2
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_eq_stateset_1(self):
        stateset1 = StateSet.from_str(r'((a:T1 + T2 /\ b:T3) ^ (T3 <= T1))')
        stateset2 = StateSet.from_str(r'((a:T4 + T5 /\ b:T6) ^ (T6 <= T5))')
        result = stateset1 == stateset2
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_eq_stateset_2(self):
        stateset1 = StateSet.from_str(r'((a:T1 + T2 /\ b:T3) ^ (T3 <= T1)) \/ (a:int /\ b:int)')
        stateset2 = StateSet.from_str(r'((a:T4 + T5 /\ b:T6) ^ (T6 <= T5)) \/ (a:int /\ b:int)')
        result = stateset1 == stateset2
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_eq_stateset_3(self):
        stateset1 = StateSet.from_str(r'((a:T1 + T2 /\ b:T3) ^ (T3 <= T1)) \/ (a:int /\ b:int)')
        stateset2 = StateSet.from_str(r'((a:T4 + T5 /\ b:T6) ^ (T6 <= T5)) \/ (a:float /\ b:str)')
        result = stateset1 == stateset2
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_leq_from_rel_1(self):
        rel = Relation.from_str(r'int <= int + float')
        if rel.relop != RelOp.LEQ:
            raise RuntimeError('Relation not ok')
        result = rel.bt_left <= rel.bt_right
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_leq_from_rel_2(self):
        rel = Relation.from_str(r'int + T1 <= int + float')
        if rel.relop != RelOp.LEQ:
            raise RuntimeError('Relation not ok')
        result = rel.bt_left <= rel.bt_right
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

    def test_funcspec_replace_basetype_1(self):
        funcspec = FuncSpec.from_str(
            r'((a:int + float /\ b:int + float) -> (return:float))'
        )
        result = funcspec.replace_basetype(Basetype.from_str('int + float'), Basetype.from_str('float'))
        expected_result = FuncSpec.from_str(r'((a:float /\ b:float) -> (return:float))')
        self.assertEqual(result, expected_result)

    def test_state_remove_valid_relations_1(self):
        state = State.from_str(r'((a:int /\ b:float) ^ (int <= int + str /\ int + float <= int + float + complex))')
        result= state.remove_valid_relations()
        expected_result = State.from_str(r'(a:int /\ b:float)')
        self.assertEqual(result, expected_result)

    def test_state_remove_valid_relations_2(self):
        state = State.from_str(r'((a:int /\ b:float) ^ (int <= int + str /\ int + float <= float + complex))')
        result= state.remove_valid_relations()
        expected_result = State.from_str(r'((a:int /\ b:float) ^ (int + float <= float + complex))')
        self.assertEqual(result, expected_result)

    def test_state_remove_valid_relations_3(self):
        state = State.from_str(r'((a:int /\ b:float) ^ (int <= int + str /\ int + T1 <= int))')
        result= state.remove_valid_relations()
        expected_result = State.from_str(r'((a:int /\ b:float) ^ (int + T1 <= int))')
        self.assertEqual(result, expected_result)

    def test_state_remove_valid_relations_4(self):
        state = State.from_str(r'((a:int /\ b:float) ^ (int <= int + str /\ int + float <= int))')
        result= state.remove_valid_relations()
        expected_result = State.from_str(r'((a:int /\ b:float) ^ (int + float <= int))')
        self.assertEqual(result, expected_result)

    def test_stateset_lub_1(self):
        set1 = StateSet.from_str(r'((a:Ta /\ b:Tb) ^ (Ta <= int /\ Tb <= float))')
        set2 = StateSet.from_str(r'((a:T1 /\ b:T2 /\ c:T3) ^ (T1 <= float /\ T2 <= str /\ T3 <= int))')
        result = set1 | set2
        expected_result = StateSet.from_str(
            r'((a:Ta /\ b:Tb) ^ (Ta <= int /\ Tb <= float)) \/ '
            r'((a:T1 /\ b:T2 /\ c:T3) ^ (T1 <= float /\ T2 <= str /\ T3 <= int))'
        )
        self.assertEqual(result, expected_result)

    def test_basetype_lub_1(self):
        bt1 = Basetype.from_str(r'int + float')
        bt2 = Basetype.from_str(r'str + int')
        result = Basetype.lub(bt1, bt2)
        expected_result = Basetype.from_str(r'int + str + float')
        self.assertEqual(result, expected_result)
    
    def test_basetype_lub_2(self):
        bt1 = Basetype.from_str(r'int + float + list< int >')
        bt2 = Basetype.from_str(r'list< str > + int')
        result = Basetype.lub(bt1, bt2)
        expected_result = Basetype.from_str(r'int + float + list< int + str >')
        self.assertEqual(result, expected_result)

    def test_basetype_lub_3(self):
        bt1 = Basetype.from_str(r'int + set< float > + list< int >')
        bt2 = Basetype.from_str(r'list< str > + set< int > + complex')
        result = Basetype.lub(bt1, bt2)
        expected_result = Basetype.from_str(r'int + set< int + float > + list< int + str > + complex')
        self.assertEqual(result, expected_result)

    def test_basetype_lub_4(self):
        bt1 = Basetype.from_str(r'int + set< list< float > >')
        bt2 = Basetype.from_str(r'set< list< int > > + complex')
        result = Basetype.lub(bt1, bt2)
        expected_result = Basetype.from_str(r'int + complex + set< list< int + float > >')
        self.assertEqual(result, expected_result)

    def test_basetype_lub_5(self):
        bt1 = Basetype.from_str(r'int + set< list< float + T1 > >')
        bt2 = Basetype.from_str(r'set< T2 + list< int > > + complex')
        result = Basetype.lub(bt1, bt2)
        expected_result = Basetype.from_str(r'int + complex + set< T2 + list< T1 + float + int > >')
        self.assertEqual(result, expected_result)

    def test_state_lub_1(self):
        state1 = State.from_str(r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= float))')
        state2 = State.from_str(r'((a:T3 /\ b:T4) ^ (T1 <= str /\ T2 <= str))')
        result = State.lub(state1, state2)
        expected_result = State.from_str(
            r'((a:T1 + T3 /\ b:T2 + T4) ^ (T1 <= int))'
        )

    def test_basetypes_solutions_1(self):
        bt1 = Basetype.from_str(r'T1 + T2 + list< T1 >')
        bt2 = Basetype.from_str(r'T3 + T4 + list< T4 >')
        sols, sol_dicts = Basetype.get_solution_replacements(bt1, bt2)
        result = set()
        for sol in sols:
            result.add(frozenset(sol))
        expected_result = {
            frozenset({(VarType('T1'), VarType('T4')), (VarType('T2'), VarType('T3'))})
        }
        self.assertEqual(result, expected_result)

    def test_basetypes_solutions_2(self):
        bt1 = Basetype.from_str(r'T1 + T2 + T5 + list< T1 >')
        bt2 = Basetype.from_str(r'T3 + T4 + T6 + list< T4 >')
        sols, sol_dicts = Basetype.get_solution_replacements(bt1, bt2)
        result = set()
        for sol in sols:
            result.add(frozenset(sol))
        expected_result = {
            frozenset({(VarType('T1'), VarType('T4')), (VarType('T2'), VarType('T3')), (VarType('T5'), VarType('T6'))}),
            frozenset({(VarType('T1'), VarType('T4')), (VarType('T2'), VarType('T6')), (VarType('T5'), VarType('T3'))}),
        }
        self.assertEqual(result, expected_result)

    def test_basetypes_solutions_3(self):
        bt1 = Basetype.from_str(r'T1 + T2 + T5 + list< T1 + T7 >')
        bt2 = Basetype.from_str(r'T3 + T4 + T6 + list< T4 + T8 >')
        sols, sol_dicts = Basetype.get_solution_replacements(bt1, bt2)
        result = set()
        for sol in sols:
            result.add(frozenset(sol))
        expected_result = {
            frozenset({(VarType('T1'), VarType('T4')), (VarType('T7'), VarType('T8')), (VarType('T2'), VarType('T3')), (VarType('T5'), VarType('T6'))}), 
            frozenset({(VarType('T1'), VarType('T4')), (VarType('T7'), VarType('T8')), (VarType('T2'), VarType('T6')), (VarType('T5'), VarType('T3'))}), 
        }
        self.assertEqual(result, expected_result)

    def test_basetypes_solutions_4(self):
        bt1 = Basetype.from_str(r'T1 + T2 + T5 + list< T1 + set< T7 > >')
        bt2 = Basetype.from_str(r'T3 + T4 + T6 + list< T4 + set< T8 > >')
        sols, sol_dicts = Basetype.get_solution_replacements(bt1, bt2)
        result = set()
        for sol in sols:
            result.add(frozenset(sol))
        expected_result = {
            frozenset({(VarType('T1'), VarType('T4')), (VarType('T7'), VarType('T8')), (VarType('T2'), VarType('T3')), (VarType('T5'), VarType('T6'))}), 
            frozenset({(VarType('T1'), VarType('T4')), (VarType('T7'), VarType('T8')), (VarType('T2'), VarType('T6')), (VarType('T5'), VarType('T3'))}), 
        }
        self.assertEqual(result, expected_result)

    def test_basetypes_solutions_5(self):
        bt1 = Basetype.from_str(r'T1 + T2 + T5 + list< T1 + set< T2 > >')
        bt2 = Basetype.from_str(r'T3 + T4 + T6 + list< T4 + set< T3 > >')
        sols, sol_dicts = Basetype.get_solution_replacements(bt1, bt2)
        result = set()
        for sol in sols:
            result.add(frozenset(sol))
        expected_result = {
            frozenset({(VarType('T1'), VarType('T4')), (VarType('T2'), VarType('T3')), (VarType('T5'), VarType('T6'))}), 
        }
        self.assertEqual(result, expected_result)

    def test_basetypes_solutions_replace_1(self):
        bt1 = Basetype.from_str(r'T1 + T2 + list< T1 >')
        bt2 = Basetype.from_str(r'T3 + T4 + list< T4 >')
        sols, sol_dicts = Basetype.get_solution_replacements(bt1, bt2)
        result = True
        for dict_pair in sol_dicts:
            new_bt1 = bt1.replace_vartype_from_solution(dict_pair[0])
            new_bt2 = bt2.replace_vartype_from_solution(dict_pair[1])
            result = result and (new_bt1 == new_bt2)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_basetypes_solutions_replace_2(self):
        bt1 = Basetype.from_str(r'T1 + T2 + T5 + list< T1 >')
        bt2 = Basetype.from_str(r'T3 + T4 + T6 + list< T4 >')
        sols, sol_dicts = Basetype.get_solution_replacements(bt1, bt2)
        result = True
        for dict_pair in sol_dicts:
            new_bt1 = bt1.replace_vartype_from_solution(dict_pair[0])
            new_bt2 = bt2.replace_vartype_from_solution(dict_pair[1])
            result = result and (new_bt1 == new_bt2)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_basetypes_solutions_replace_3(self):
        bt1 = Basetype.from_str(r'T1 + T2 + T5 + list< T1 + T7 >')
        bt2 = Basetype.from_str(r'T3 + T4 + T6 + list< T4 + T8 >')
        sols, sol_dicts = Basetype.get_solution_replacements(bt1, bt2)
        result = True
        for dict_pair in sol_dicts:
            new_bt1 = bt1.replace_vartype_from_solution(dict_pair[0])
            new_bt2 = bt2.replace_vartype_from_solution(dict_pair[1])
            result = result and (new_bt1 == new_bt2)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_basetypes_solutions_replace_4(self):
        bt1 = Basetype.from_str(r'T1 + T2 + T5 + list< T1 + set< T7 > >')
        bt2 = Basetype.from_str(r'T3 + T4 + T6 + list< T4 + set< T8 > >')
        sols, sol_dicts = Basetype.get_solution_replacements(bt1, bt2)
        result = True
        for dict_pair in sol_dicts:
            new_bt1 = bt1.replace_vartype_from_solution(dict_pair[0])
            new_bt2 = bt2.replace_vartype_from_solution(dict_pair[1])
            result = result and (new_bt1 == new_bt2)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_basetypes_solutions_replace_5(self):
        bt1 = Basetype.from_str(r'T1 + T2 + T5 + list< T1 + set< T2 > >')
        bt2 = Basetype.from_str(r'T3 + T4 + T6 + list< T4 + set< T3 > >')
        sols, sol_dicts = Basetype.get_solution_replacements(bt1, bt2)
        result = True
        for dict_pair in sol_dicts:
            new_bt1 = bt1.replace_vartype_from_solution(dict_pair[0])
            new_bt2 = bt2.replace_vartype_from_solution(dict_pair[1])
            result = result and (new_bt1 == new_bt2)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_assignment_get_vartype_pairs_1(self):
        assign1 = Assignment.from_str(r'a:T1 + T2 /\ b:T1')
        assign2 = Assignment.from_str(r'a:T3 + T4 /\ b:T4')
        sols, sol_dicts = Assignment.get_solution_replacements(assign1, assign2)
        result = set()
        for sol in sols:
            result.add(frozenset(sol))
        expected_result = {
            frozenset({(VarType('T1'), VarType('T4')), (VarType('T2'), VarType('T3'))})
        }
        self.assertEqual(result, expected_result)
    
    def test_assignment_get_vartype_pairs_2(self):
        assign1 = Assignment.from_str(r'a:T1 + T2 /\ b:T3')
        assign2 = Assignment.from_str(r'a:T4 + T5 /\ b:T6')
        sols, sol_dicts = Assignment.get_solution_replacements(assign1, assign2)
        result = set()
        for sol in sols:
            result.add(frozenset(sol))
        expected_result = {
            frozenset({(VarType('T1'), VarType('T4')), (VarType('T2'), VarType('T5')), (VarType('T3'), VarType('T6'))}),
            frozenset({(VarType('T1'), VarType('T5')), (VarType('T2'), VarType('T4')), (VarType('T3'), VarType('T6'))})
        }
        self.assertEqual(result, expected_result)

    def test_assignment_replace_from_solution_1(self):
        assign1 = Assignment.from_str(r'a:T1 + T2 /\ b:T1')
        assign2 = Assignment.from_str(r'a:T3 + T4 /\ b:T4')
        sols, sol_dicts = Assignment.get_solution_replacements(assign1, assign2)
        result = True
        for dict_pair in sol_dicts:
            new_assign1 = assign1.replace_vartype_from_solution(dict_pair[0])
            new_assign2 = assign2.replace_vartype_from_solution(dict_pair[1])
            result = result and (new_assign1 == new_assign2)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_assignment_replace_from_solution_2(self):
        assign1 = Assignment.from_str(r'a:T1 + T2 /\ b:T3')
        assign2 = Assignment.from_str(r'a:T4 + T5 /\ b:T6')
        sols, sol_dicts = Assignment.get_solution_replacements(assign1, assign2)
        result = True
        for dict_pair in sol_dicts:
            new_assign1 = assign1.replace_vartype_from_solution(dict_pair[0])
            new_assign2 = assign2.replace_vartype_from_solution(dict_pair[1])
            result = result and (new_assign1 == new_assign2)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_state_replace_from_solution_1(self):
        state1 = State.from_str(r'((a:T1 + T2 /\ b:T1) ^ (T1 <= T2))')
        state2 = State.from_str(r'((a:T3 + T4 /\ b:T4) ^ (T4 <= T3))')
        sols, sol_dicts = State.get_solution_replacements(state1, state2)
        result = True
        for dict_pair in sol_dicts:
            new_state1 = state1.replace_vartype_from_solution(dict_pair[0])
            new_state2 = state2.replace_vartype_from_solution(dict_pair[1])
            result = result and (new_state1 == new_state2)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_state_replace_from_solution_2(self):
        state1 = State.from_str(r'((a:T1 + T2 /\ b:T3) ^ (T3 <= T1))')
        state2 = State.from_str(r'((a:T4 + T5 /\ b:T6) ^ (T6 <= T5))')
        sols, sol_dicts = State.get_solution_replacements(state1, state2)
        result = False
        for dict_pair in sol_dicts:
            new_state1 = state1.replace_vartype_from_solution(dict_pair[0])
            new_state2 = state2.replace_vartype_from_solution(dict_pair[1])
            result = result or (new_state1 == new_state2)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_state_replace_from_solution_3(self):
        state1 = State.from_str(r'((a:T1 /\ b:T2) ^ (T1 <= T2))')
        state2 = State.from_str(r'((a:T?0 /\ b:T?1) ^ (T?1 <= T?0))')
        sols, sol_dicts = Assignment.get_solution_replacements(state1.assignment, state2.assignment)
        result = deepcopy(state2)
        self.assertEqual(len(sols), 1)
        for pair in list(sols)[0]:
            result = result.replace_vartype(pair[1].varexp, pair[0].varexp)
        expected_result = State.from_str(r'((a:T1 /\ b:T2) ^ (T2 <= T1))')
        self.assertEqual(result, expected_result)

    def test_state_generate_fresh_vartypes(self):
        state = State.from_str(r'((a:T1 /\ b:T2 /\ c:T?1 /\ d:set< T?2 >) ^ (T2 <= list< T?1 > /\ T2 <= T?2))')
        state.gen_id = 3
        result = state.generate_fresh_vartypes()
        expected_result_1 = State.from_str(
            r'((a:T1 /\ b:T2 /\ c:T3 /\ d:set< T4 >) ^ (T2 <= list< T3 > /\ T2 <= T4))'
        )
        expected_result_2 = State.from_str(
            r'((a:T1 /\ b:T2 /\ c:T4 /\ d:set< T3 >) ^ (T2 <= list< T4 > /\ T2 <= T3))'
        )
        # the order in which type variables are found can go either way
        cond1 = (result.assignment == expected_result_1.assignment) or (result.assignment == expected_result_2.assignment)
        cond2 = (result.constraints == expected_result_1.constraints) or (result.constraints == expected_result_2.constraints)
        self.assertEqual(cond1 and cond2, True)

    def test_stateset_contains_1(self):
        stateset = StateSet.from_str(
            r'(a:int /\ b:int) \/ (a:float /\ b:float)'
        )
        state1 = State.from_str(r'(a:int /\ b:int)')
        state2 = State.from_str(r'(a:float /\ b:float)')
        result = (state1 in stateset) and (state2 in stateset)
        expected_result = True
        self.assertEqual(result, expected_result)
 
    # def test_stateset_contains_2(self):
    #     stateset = StateSet.from_str(
    #         r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= int)) \/ '
    #         r'(a:float /\ b:float)'
    #     )
    #     state1 = State.from_str(r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= int))')
    #     state2 = State.from_str(r'(a:float /\ b:float)')
    #     result = (state1 in stateset) and (state2 in stateset)
    #     expected_result = True
    #     self.assertEqual(result, expected_result)

    # def test_stateset_contains_3(self):
    #     stateset = StateSet.from_str(
    #         r'((a:T3 /\ b:T4) ^ (T3 <= int /\ T4 <= int)) \/ '
    #         r'(a:float /\ b:float)'
    #     )
    #     state1 = State.from_str(r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= int))')
    #     state2 = State.from_str(r'(a:float /\ b:float)')
    #     result = (state1 in stateset) and (state2 in stateset)
    #     expected_result = True
    #     self.assertEqual(result, expected_result)

    def test_stateset_le_1(self):
        ss1 = StateSet.from_str(
            r'(a:int /\ b:int) \/ (a:float /\ b:float)'
        )
        ss2 = StateSet.from_str(
            r'(a:int /\ b:int)'
        )
        result = ss2 <= ss1
        expected_result = True
        self.assertEqual(result, expected_result)

    # def test_stateset_le_2(self):
    #     ss1 = StateSet.from_str(
    #         r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= int)) \/ '
    #         r'(a:float /\ b:float)'
    #     )
    #     ss2 = StateSet.from_str(
    #         r'((a:T3 /\ b:T4) ^ (T3 <= int /\ T4 <= int))'
    #     )
    #     result = ss2 <= ss1
    #     expected_result = True
    #     self.assertEqual(result, expected_result)

    # def test_stateset_le_3(self):
    #     ss1 = StateSet.from_str(
    #         r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= int)) \/ '
    #         r'(a:float /\ b:float)'
    #     )
    #     ss2 = StateSet.from_str(
    #         r'((a:T3 /\ b:T4) ^ (T3 <= int /\ T4 <= int)) \/ '
    #         r'(b:float /\ a:float)'
    #     )
    #     result = (ss2 <= ss1) and (ss1 <= ss2)
    #     expected_result = True
    #     self.assertEqual(result, expected_result)

    def test_stateset_le_4(self):
        ss1 = StateSet.from_str(r'a:list < list < int > > /\ b:float')
        ss2 = StateSet.from_str(r'a:list < top > /\ b:int + float')
        result = ss1 <= ss2
        self.assertEqual(result, True)


    def test_state_replace_from_constraints_1(self):
        state = State.from_str(r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T1 + T2 <= float))')
        result = state.replace_from_constraints()
        expected_result = State.from_str(r'((a:int /\ b:T2) ^ (int + T2 <= float))')
        self.assertEqual(result, expected_result)

    def _test_get_spectype_substitutions_1(self):
        bt = Basetype.from_str(r'int + list< set< T1 + int > >')
        specbt = Basetype.from_str(r'int + float + list< T?0 >')
        result = Basetype.get_spectype_substitutions(bt, specbt)
        expected_result = {
            Basetype.from_str('T?0'): { Basetype.from_str(r'set< T1 + int >') }
        }
        self.assertEqual(result, expected_result)

    def _test_get_spectype_substitutions_2(self):
        bt = Basetype.from_str(r'int + list< T1 + int >')
        specbt = Basetype.from_str(r'int + float + list< T?0 >')
        result = Basetype.get_spectype_substitutions(bt, specbt)
        expected_result = {
            Basetype.from_str('T?0'): { Basetype.from_str(r'T1 + int') }
        }
        self.assertEqual(result, expected_result)

    def _test_get_spectype_substitutions_3(self):
        bt = Basetype.from_str(r'int + set< T1 + int >')
        specbt = Basetype.from_str(r'int + float + list< T?0 >')
        result = Basetype.get_spectype_substitutions(bt, specbt)
        expected_result = dict()
        self.assertEqual(result, expected_result)

    def test_get_builtin_from_bt_1(self):
        # bt = Basetype.from_str(r'Iterable< int + float >')
        bt = Basetype.from_str(r'Iterable< int > + Iterable< float >')
        result = bt.get_builtin_from_bt()
        result.flatten()
        expected_result = Basetype.from_str(
            r'list< int + float > + tuple< int + float > + set< int + float > + frozenset< int + float >'
        )
        self.assertEqual(result, expected_result)

    def test_basetype_flatten_1(self):
        bt = Basetype.from_str(r'int + list< int + float > + set< T1 > + set< int + float >')
        bt.flatten()
        result = bt
        expected_result = Basetype.from_str(r'int + list< int + float > + set< T1 + int + float >')
        self.assertEqual(result, expected_result)

    def test_basetype_container_with_spaces_1(self):
        result = Basetype.from_str(r'list < int + float >')
        expected_result = Basetype({PyType(list, Basetype({PyType(int), PyType(float)}))})
        self.assertEqual(result, expected_result)

    def test_basetype_container_with_spaces_2(self):
        result = Basetype.from_str(r'list < int + float > + set < float >')
        expected_result = Basetype({
            PyType(list, Basetype({PyType(int), PyType(float)})),
            PyType(set, Basetype({PyType(float)}))
        })
        self.assertEqual(result, expected_result)

    def test_vartypes_to_spectypes(self):
        st = State.from_str(r'(a:list < T3 + int > + T1 + bytearray)')
        result = st.vartypes_to_spectypes()
        expected_result = State.from_str('(a:list < T?3 + int > + T?1 + bytearray)')
        self.assertEqual(result.is_same(expected_result), True)

    def test_basetype_remove_vartype(self):
        bt = Basetype.from_str(r'list < T?3 + int > + T?1 + float')
        result = bt.remove_vartypes(('T?1', 'T?3'))
        expected_result = Basetype.from_str(r'list < int > + float')
        self.assertEqual(result, expected_result)

    def test_basetype_remove_irrelevant_vartypes_1(self):
        spec = FuncSpec.from_str(r'((x:T?1 + int /\ y:T?2 + int) -> (return:int))')
        result = spec.remove_irrelevant_vartypes()
        expected_result = FuncSpec.from_str(r'((x:int /\ y:int) -> (return:int))')
        self.assertEqual(result, expected_result)

    def test_basetype_remove_irrelevant_vartypes_2(self):
        spec = FuncSpec.from_str(r'((x:T?1 + int + list < T?1 > /\ y:T?2 + int) -> (return:int))')
        result = spec.remove_irrelevant_vartypes()
        expected_result = FuncSpec.from_str(r'((x:T?1 + int + list < T?1 > /\ y:int) -> (return:int))')
        self.assertEqual(result, expected_result)

    def test_basetype_remove_irrelevant_vartypes_3(self):
        spec = FuncSpec.from_str(r'((x:T?1 + int /\ y:T?1 + int) -> (return:int))')
        result = spec.remove_irrelevant_vartypes()
        expected_result = FuncSpec.from_str(r'((x:T?1 + int /\ y:T?1 + int) -> (return:int))')
        self.assertEqual(result, expected_result)

    def test_basetype_lesser_1(self):
        bt1 = Basetype.from_str(r'list < list < int > >')
        bt2 = Basetype.from_str(r'list < top >')
        result = bt1 <= bt2
        self.assertEqual(result, True)

    def test_basetype_lesser_2(self):
        bt1 = Basetype.from_str(r'list < list < int > >')
        bt2 = Basetype.from_str(r'bot')
        result = bt2 <= bt1
        self.assertEqual(result, True)

    def test_basetype_lesser_3(self):
        bt1 = Basetype.from_str(r'list < list < int > >')
        bt2 = Basetype.from_str(r'top')
        result = bt1 <= bt2
        self.assertEqual(result, True)

    def test_basetype_lesser_4(self):
        bt1 = Basetype.from_str(r'int + float')
        bt2 = Basetype.from_str(r'int + float + complex')
        result = bt1 <= bt2
        self.assertEqual(result, True)

    def test_basetype_lesser_5(self):
        bt1 = Basetype.from_str(r'int + float')
        bt2 = Basetype.from_str(r'list < int + float >')
        result = bt1 <= bt2
        self.assertEqual(result, False)

    def test_basetype_lesser_6(self):
        bt1 = Basetype.from_str(r'list < int + float >')
        bt2 = Basetype.from_str(r'list < int + float + complex >')
        result = bt1 <= bt2
        self.assertEqual(result, True)

    def test_basetype_lesser_7(self):
        bt1 = Basetype.from_str(r'list < int + float >')
        bt2 = Basetype.from_str(r'top')
        result = bt1 <= bt2
        self.assertEqual(result, True)

    def test_basetype_lesser_8(self):
        bt1 = Basetype.from_str(r'list < int + float >')
        bt2 = Basetype.from_str(r'bot')
        result = bt2 <= bt1
        self.assertEqual(result, True)

    def test_pytype_lesser_1(self):
        pt1 = PyType.from_str(r'int')
        pt2 = PyType.from_str(r'float')
        result = pt1 <= pt2
        self.assertEqual(result, False)

    def test_pytype_lesser_2(self):
        pt1 = PyType.from_str(r'int')
        pt2 = PyType.from_str(r'int')
        result = pt1 <= pt2
        self.assertEqual(result, True)

    def test_pytype_lesser_3(self):
        pt1 = PyType.from_str(r'bot')
        pt2 = PyType.from_str(r'int')
        result = pt1 <= pt2
        self.assertEqual(result, True)

    def test_pytype_lesser_4(self):
        pt1 = PyType.from_str(r'int')
        pt2 = PyType.from_str(r'top')
        result = pt1 <= pt2
        self.assertEqual(result, True)

    def test_state_le_1(self):
        st1 = State.from_str(r'a:int /\ b:float')
        st2 = State.from_str(r'a:int + float /\ b:int + float')
        result = st1 <= st2
        self.assertEqual(result, True)

    def test_state_le_2(self):
        st1 = State.from_str(r'a:int + T1 /\ b:float')
        st2 = State.from_str(r'a:int + float + T2 /\ b:int + float')
        result = st1 <= st2
        self.assertEqual(result, True)

    def test_state_le_3(self):
        st1 = State.from_str(r'a:int + T1 /\ b:float')
        st2 = State.from_str(r'a:int + complex + T2 /\ b:int + float')
        result = st1 <= st2
        self.assertEqual(result, True)

    def test_state_le_4(self):
        st1 = State.from_str(r'a:list < list < int > > /\ b:float')
        st2 = State.from_str(r'a:list < top > /\ b:int + float')
        result = st1 <= st2
        self.assertEqual(result, True)

    def test_basetype_depth_1(self):
        bt = Basetype.from_str(r'int + float + list < int >')
        result = bt.get_depth()
        self.assertEqual(result, 2)

    def test_basetype_depth_2(self):
        bt = Basetype.from_str(r'list < tuple < int > > + float + list < int >')
        result = bt.get_depth()
        self.assertEqual(result, 3)

    def test_basetype_depth_3(self):
        bt = Basetype.from_str(r'dict < int, list < tuple < float + int > > > + float + list < int >')
        result = bt.get_depth()
        self.assertEqual(result, 4)

    def test_basetype_depth_4(self):
        bt = Basetype.from_str(r'list < int >')
        result = bt.get_depth()
        self.assertEqual(result, 2)

    def test_basetype_depth_5(self):
        bt = Basetype.from_str(r'list < int + list < float > >')
        result = bt.get_depth()
        self.assertEqual(result, 3)

    def test_basetype_depth_6(self):
        bt = Basetype.from_str(r'dict < int, list < int > >')
        result = bt.get_depth()
        self.assertEqual(result, 3)

    def test_basetype_widen_1(self):
        '''
        width > max_width
        '''
        bt = Basetype.from_str(r'int + float + complex')
        result = bt.widen(max_width=2)
        expected_result = Basetype.from_str(r'top')
        self.assertEqual(result, expected_result)

    def test_basetype_widen_2(self):
        '''
        widh > max_width inside container
        '''
        bt = Basetype.from_str(r'list < int + float + complex >')
        result = bt.widen(max_width=2)
        expected_result = Basetype.from_str(r'list < top >')
        self.assertEqual(result, expected_result)

    def test_basetype_widen_3(self):
        '''
        depth > max_depth
        '''
        bt = Basetype.from_str(r'list < list < int + float + complex > >')
        result = bt.widen(max_depth=2)
        expected_result = Basetype.from_str(r'list < top >')
        self.assertEqual(result, expected_result)

    def test_basetype_widen_4(self):
        '''
        width <= max_width and depth <= max_depth
        '''
        bt = Basetype.from_str(r'list < list < int + float + complex > >')
        result = bt.widen(max_depth=3)
        expected_result = Basetype.from_str(r'list < list < int + float + complex > >')
        self.assertEqual(result, expected_result)

    def test_basetype_widen_5(self):
        '''
        width > max_width on just keys
        '''
        bt = Basetype.from_str(r'dict < int + float + complex, str >')
        result = bt.widen(max_width=2)
        expected_result = Basetype.from_str(r'dict < top, str >')
        self.assertEqual(result, expected_result)

    def test_basetype_widen_6(self):
        '''
        width > max_width on just values
        '''
        bt = Basetype.from_str(r'dict < str, int + float + complex >')
        result = bt.widen(max_width=2)
        expected_result = Basetype.from_str(r'dict < str, top >')
        self.assertEqual(result, expected_result)

    def test_basetype_widen_7(self):
        '''
        max_depth 1 for dict
        '''
        bt = Basetype.from_str(r'dict < str, int + float + complex >')
        result = bt.widen(max_width=1, max_depth=1)
        expected_result = Basetype.from_str(r'dict < top, top >')
        self.assertEqual(result, expected_result)

    def test_basetype_widen_8(self):
        '''
        depth > max_depth for keys in dict
        '''
        bt = Basetype.from_str(r'dict < str, list < tuple < int > > >')
        result = bt.widen(max_depth=3)
        expected_result = Basetype.from_str(r'dict < str, top >')
        self.assertEqual(result, expected_result)

    def test_state_widen_1(self):
        '''
        width and depth exceeded 
        '''
        st = State.from_str(r'a:int + float + complex /\ b:list < list < list < int > > >')
        result = st.widen(2, 2)
        expected_result = State.from_str(r'a:top /\ b:list < top >')
        self.assertEqual(result, expected_result)

    def test_stateset_widen_1(self):
        '''
        width and depth exceeded for one state
        '''
        st = StateSet.from_str(
            r'(a:int + float + complex /\ b:list < list < list < int > > >) \/ '
            r'(a:int /\ b:float)'
        )
        result = st.widen(2, 2)
        expected_result = StateSet.from_str(
            r'(a:top /\ b:list < top >) \/ '
            r'(a:int /\ b:float)'
        )
        self.assertEqual(result, expected_result)
    