import unittest
from Translator import *
from statev2.basetype import *
from statev2.transfer import *


class SpecTestCases(unittest.TestCase):
    def test_apply_spec_1(self):
        state = Translator.translate_state(r'((a:int+float /\ b:int+float))')
        spec = Translator.translate_state(r'(a:float /\ b:int)')
        expected_result = Translator.translate_state(
            r'((a:T_a` /\ b:T_b`) ^ '
            r'((T_a` <= int+float) /\ (T_a` <= float) /\ (T_b` <= int+float) /\ (T_b` <= int))'
            r')'
        )
        result = state_apply_spec(state, spec, testmode=True)
        self.assertEqual(result, expected_result)

    def test_apply_spec_set_1(self):
        stateset = Translator.translate_state_set(
            r'((a:T_a /\ b:T_b))'
        )
        specset = Translator.translate_state_set(
            r'((a:int /\ b:int)) \/ ((a:float /\ b:float))'
        )
        expected_result = Translator.translate_state_set(
            r'((a:T_a` /\ b:T_b`) ^ (T_a` <= T_a /\ T_a` <= int /\ T_b` <= T_b /\ T_b` <= int)) \/ '
            r'((a:T_a` /\ b:T_b`) ^ (T_a` <= T_a /\ T_a` <= float /\ T_b` <= T_b /\ T_b` <= float))'
        )
        result = set_apply_spec(stateset, specset, testmode=True)
        self.assertEqual(result, expected_result)

    def test_apply_spec_set_2(self):
        stateset = Translator.translate_state_set(
            r'((a:T_a /\ b:T_b) ^ (T_a <= int+float /\ T_b <= str))'
        )
        specset = Translator.translate_state_set(
            r'((a:int /\ b:int)) \/ ((a:float /\ b:float))'
        )
        expected_result = Translator.translate_state_set(
            r'((a:T_a` /\ b:T_b`) ^ '
            r'(T_a` <= T_a /\ T_a` <= int /\ T_b` <= T_b /\ T_b` <= int /\ T_a <= int+float /\ T_b <= str)) \/ '
            r'((a:T_a` /\ b:T_b`) ^ '
            r'(T_a <= int+float /\ T_b <= str /\ T_a` <= T_a /\ T_a` <= float /\ T_b` <= T_b /\ T_b` <= float))'
        )
        result = set_apply_spec(stateset, specset, testmode=True)
        self.assertEqual(result, expected_result)

    def test_spec_to_state_1(self):
        spec = Translator.translate_func_spec(r'((a:int /\ b:int) -> ((a+b):int))')
        result = spec_to_state(spec)
        expected_result = Translator.translate_state(r'(a:int /\ b:int /\ (a+b):int)')
        self.assertEqual(result, expected_result)
