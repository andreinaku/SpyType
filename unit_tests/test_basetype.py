import unittest
from statev2.basetype import *
from Translator import *


class BasetypeTestCases(unittest.TestCase):
    def test_apply_spec(self):
        state = Translator.translate_state(r'(a:int+float /\ b:int+float)')
        spec = Translator.translate_state(r'(a:float /\ b:int)')
        expected_result = Translator.translate_state(
            r"((a:T_a` /\ b:T_b`) ^ ((T_a` <= int+float \/ T_a` <= float) /\ (T_b` <= int+float \/  T_b` <= int)))"
        )
        result = apply_spec(state, spec, testmode=True)
        self.assertEqual(result, expected_result)
