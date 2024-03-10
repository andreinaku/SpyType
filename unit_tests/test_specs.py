import unittest
from Translator import *
from statev2 import *


class SpecTestCases(unittest.TestCase):
    def test_apply_spec_1(self):
        state = Translator.translate_state(r'(a:int+float /\ b:int+float)')
        spec = Translator.translate_state(r'(a:float /\ b:int)')
        expected_result = Translator.translate_state(
            r'((a:T_a` /\ b:T_b`) ^ '
            r'((T_a` <= int+float) /\ (T_a` <= float) /\ (T_b` <= int+float) /\ (T_b` <= int))'
            r')'
        )
        result = state_apply_spec(state, spec, testmode=True)
        self.assertEqual(result, expected_result)

    def test_apply_spec_set_1(self):
        pass

    def skip_test_apply_spec_2(self):
        state = Translator.translate_state(r'(a:int+float /\ b:int+float)')
        spec = Translator.translate_state(r'(a:float /\ b:int)')
        result = state_apply_spec(state, spec, testmode=True)
        result2 = state_apply_spec(result, spec, testmode=True)
        self.assertEqual(result, result2)

    def skip_test_apply_spec_3(self):
        state = Translator.translate_state(r'(a:int+float /\ b:int+float')
        spec = Translator.translate_state(r'(a:T_a /\ b:T_b)')
        result = state_apply_spec(state, spec, testmode=True)
        expected_result = Translator.translate_state(r'(a:int+float /\ b:int+float')
        self.assertEqual(result, expected_result)

    def skip_test_apply_spec_4(self):
        state = Translator.translate_state(r'(a:int+float /\ b:int+float)')
        spec = Translator.translate_state(r'(a:T_a /\ b:float)')
        result = state_apply_spec(state, spec, testmode=True)
        expected_result = Translator.translate_state(r'(a:int+float /\ b:float)')
        self.assertEqual(result, expected_result)

    def skip_test_apply_spec_5(self):
        state = Translator.translate_state(r'(a:list<int> /\ b:T_b)')
        spec = Translator.translate_state(r'(a:list<T_1> /\ b:int)')
        result = state_apply_spec(state, spec, testmode=True)
        expected_result = Translator.translate_state(r'(a:list<int> /\ b:T_b) ^ ((T_b <= int \/ int <= T_b))')
        self.assertEqual(result, expected_result)
