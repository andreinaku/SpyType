from testbase import *
from statev2.ConstraintSolver import *


def maude_start():
    maude.init()
    init_module = 'init.maude'
    if not maude.load('init.maude'):
        raise RuntimeError(f'Could not load {init_module}')


class SolverTestCases(unittest.TestCase):
    def test_solve_state_constraints_1(self):
        maude_start()
        state = Translator.translate_state(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T1 <= int + str /\ T2 <= float /\ T2 <= float + complex))'
        )
        result = ConstraintSolver(state).solve_state_constraints(strat1)
        expected_result = Translator.translate_state(r'a:int /\ b:float')
        self.assertEqual(result, expected_result)

    def test_solved_state_eq_1(self):
        maude_start()
        state1 = Translator.translate_state(
            r'((a:T1 /\ b:T2) ^ (T1 <= int /\ T1 <= int + str /\ T2 <= float /\ T2 <= float + complex))'
        )
        state2 = Translator.translate_state(
            r'a:int /\ b:float'
        )
        solved1 = ConstraintSolver(state1).solve_state_constraints(strat1)
        solved2 = ConstraintSolver(state2).solve_state_constraints(strat1)
        result = solved1 == solved2
        expected_result = True
        self.assertEqual(result, expected_result)
