from testbase import *
from statev2.basetype import *


MAUDE_DUMP = PROJECT_DIR + os.sep + 'tempmod.maude'


class SolverTestCases(unittest.TestCase):
    def test_solve_state_constraints_1(self):
        state = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T1 <= int + str /\ T2 <= float /\ T2 <= float + complex))'
        )
        result = state.solve_constraints(strat1, MAUDE_DUMP)
        expected_result = State.from_str(r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= float))')
        # self.assertEqual(result, expected_result)
        self.assertEqual(State.raw_eq(result, expected_result), True)

    def test_solve_state_constraints_2(self):
        state = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T1 <= int + str /\ T2 <= str /\ T2 <= float + complex))'
        )
        result = state.solve_constraints(strat1, MAUDE_DUMP)
        expected_result = State.from_str(r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= bot))')
        self.assertEqual(State.raw_eq(result, expected_result), True)

    def test_solve_state_constraints_3(self):
        state = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T1 <= int + str /\ T2 <= str /\ T2 <= float + complex))'
        )
        result = state.solve_constraints(strat1, MAUDE_DUMP)
        expected_result = State.from_str(r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= bot))')
        self.assertEqual(State.raw_eq(result, expected_result), True)

    def test_solve_state_constraints_4(self):
        state = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T1 <= int + str /\ T2 <= str /\ T2 <= float + complex))'
        )
        result = state.solve_constraints(strat1, MAUDE_DUMP)
        expected_result = State.from_str(r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= bot))')
        self.assertEqual(State.raw_eq(result, expected_result), True)

    def test_solve_state_constraints_5(self):
        state = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= float /\ T2 <= float /\ int <= str))'
        )
        result = state.solve_constraints(strat1, MAUDE_DUMP)
        expected_result = State.from_str(r'((a:T1 /\ b:T2) ^ (T1 <= float /\ T2 <= float /\ int <= str))')
        self.assertEqual(State.raw_eq(result, expected_result), True)

    def _test_solve_state_constraints_6(self):
        state = State.from_str(
            r'((a:T4 /\ b:T5 /\ c:T3) ^ (T6 <= int /\ T7 <= float /\ T1 <= float /\ T2 <= str /\ T3 <= int /\ T4 <= T6 + T1 /\ T5 <= T7 + T2))'
        )
        result = state.solve_constraints(strat1, MAUDE_DUMP)
        expected_result = None
        self.assertEqual(result, expected_result)

    def test_solve_state_constraints_7(self):
        state = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= T2 /\ T2 <= T1))'
        )
        result = state.solve_constraints(strat1, MAUDE_DUMP)
        expected_result = State.from_str( r'((a:T1 /\ b:T2) ^ (T1 <= T2 /\ T2 <= T1))')
        self.assertEqual(State.raw_eq(result, expected_result), True)

    def test_solve_state_constraint_8(self):
        state = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T3 <= T1 + T2))'
        )
        result = state.solve_constraints()
        expected_result = State.from_str(r'((a:T1 /\ b:T2) ^ (T3 <= T1 + T2))')
        self.assertEqual(State.raw_eq(result, expected_result), True)

    def test_solve_state_constraint_9(self):
        state = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= list< T3 > /\ T2 <= list< T4 >))'
        )
        result = state.solve_constraints()
        expected_result = State.from_str(r'((a:T1 /\ b:T2) ^ (T1 <= list< T3 > /\ T2 <= list< T4 >))')
        self.assertEqual(State.raw_eq(result, expected_result), True)

    def test_solved_state_eq_1(self):
        state1 = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T1 <= int + str /\ T2 <= float /\ T2 <= float + complex))'
        )
        state2 = State.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= float))'
        )
        result = state1.is_same(state2)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_solve_stateset_1(self):
        stateset = StateSet.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= int)) \/ '
            r'((a:T1 /\ b:T2) ^ (T1 <= float /\ T2 <= float))'
        )
        result = stateset.solve_states()
        expected_result = StateSet.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= int)) \/ '
            r'((a:T1 /\ b:T2) ^ (T1 <= float /\ T2 <= float))'
        )
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_solve_stateset_2(self):
        stateset = StateSet.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= int)) \/ '
            r'((a:T1 /\ b:T2) ^ (T1 <= float /\ T2 <= float /\ int <= str))'
        )
        result = stateset.solve_states()
        expected_result = StateSet.from_str(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T2 <= int)) \/ '
            r'((a:T1 /\ b:T2) ^ (T1 <= float /\ T2 <= float /\ int <= str))'
        )
        self.assertEqual(StateSet.raw_eq(result, expected_result), True)

    def test_solve_stateset_3(self):
        stateset = StateSet.from_str(
            r'((b:T4 /\ a:int) ^ (T1 <= int /\ T4 <= int)) \/ '
            r'((b:T4 /\ a:float) ^ ((T4 <= float) /\ (T1 <= float) /\ (T1 <= int))) \/ '
            r'((b:T4 /\ a:bytearray) ^ ((T1 <= bytearray + bytes + memoryview) /\ (T4 <= bytearray) /\ (T1 <= int))) \/ '
            r'((b:T4 /\ a:tuple< T3 + T2 >) ^ ((T4 <= tuple< T3 >) /\ (T1 <= tuple< T2 >) /\ (T1 <= int))) \/ '
            r'((b:T4 /\ a:bytes) ^ ((T4 <= bytes) /\ (T1 <= bytearray + bytes + memoryview) /\ (T1 <= int))) \/ '
            r'((b:T4 /\ a:str) ^ ((T1 <= str) /\ (T4 <= str) /\ (T1 <= int))) \/ '
            r'((b:T4 /\ a:complex) ^ ((T1 <= complex) /\ (T4 <= complex) /\ (T1 <= int))) \/ '
            r'((b:T4 /\ a:list< T3 + T2 >) ^ ((T4 <= list< T3 >) /\ (T1 <= int) /\ (T1 <= list< T2 >))) \/ '
            r'((b:T4 /\ a:tuple< T2 >) ^ ((T1 <= tuple< T2 >) /\ (T4 <= tuple< T2 >) /\ (T1 <= int))) \/ '
            r'((b:T4 /\ a:list< T2 >) ^ ((T1 <= list< T2 >) /\ (T1 <= int) /\ (T4 <= list< T2 >)))'
        )
        result = stateset.solve_states()
        expected_result = StateSet.from_str(
            r'((b:T4 /\ a:int) ^ (T1 <= int /\ T4 <= int))'
        )
        self.assertEqual(result, expected_result)

    def _test_solve_state_constraint_10(self):
        state = State.from_str(
            r'((a:T1) ^ (T1 <= list< T3 > /\ T1 <= T4 /\ T4 <= list< T3 >))'
        )
        result = state.solve_constraints()
        expected_result = State.from_str(
            r'((a:T1) ^ (T1 <= list< T3 > /\ T1 <= T4))'
        )
        self.assertEqual(result, expected_result)

    def test_solve_state_constraint_11(self):
        state = State.from_str(
            r'((a:T1 /\ b:list< T3 >) ^ ((T1 <= list< T3 >) /\ (T2 <= list< T3 >)))'
        )
        result = state.solve_constraints()
        expected_result = State.from_str(r'((a:T1 /\ b:list< T3 >) ^ ((T1 <= list< T3 >) /\ (T2 <= list< T3 >)))')
        self.assertEqual(State.raw_eq(result, expected_result), True)
