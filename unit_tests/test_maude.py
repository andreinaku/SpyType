from testbase import *
from statev2.basetype import *


MAUDE_DUMP = PROJECT_DIR + os.sep + 'tempmod.maude'


class SolverTestCases(unittest.TestCase):
    def test_solve_state_constraints_1(self):
        state = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T1 <= int + str /\ T2 <= float /\ T2 <= float + complex))'
        )
        state1 = state.solve_constraints(strat1, MAUDE_DUMP)
        state2 = State.from_str(r'a:int /\ b:float')
        result = state1.is_same(state2)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_solve_state_constraints_2(self):
        state = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T1 <= int + str /\ T2 <= str /\ T2 <= float + complex))'
        )
        state1 = state.solve_constraints(strat1, MAUDE_DUMP)
        state2 = State.from_str(r'a:int /\ b:bot')
        result = state1.is_same(state2)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_solved_state_eq_1(self):
        state1 = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T1 <= int + str /\ T2 <= float /\ T2 <= float + complex))'
        )
        state2 = State.from_str(
            r'a:int /\ b:float'
        )
        result = state1.is_same(state2)
        expected_result = True
        self.assertEqual(result, expected_result)
