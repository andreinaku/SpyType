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

    def test_find_specs_1(self):
        expr = 'a + b'
        binop_node = ast.parse(expr).body[0].value
        result = find_spec_from_binop(binop_node)
        expected_result = unitedspecs['__add__']
        self.assertEqual(result, expected_result)

    def test_get_specset_from_binop_1(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        result = get_specset_from_binop(binop_node)
        expected_result = hset(
            {
                Translator.translate_func_spec(r'((self:complex /\ __value:complex) -> (return:complex))'),
                Translator.translate_func_spec(r'((self:float /\ __value:float) -> (return:float))'),
                Translator.translate_func_spec(r'((self:int /\ __value:int) -> (return:float))')
            }
        )
        self.assertEqual(result, expected_result)

    def test_substitute_binop_state_arguments_1(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state = Translator.translate_state(r'(a:int+float /\ b:int+float)')
        result = substitute_binop_state_arguments(state, binop_node)
        expected_result = hset(
            {
                Translator.translate_func_spec(r'((a:complex /\ b:complex) -> ((a / b):complex))'),
                Translator.translate_func_spec(r'((a:float /\ b:float) -> ((a / b):float))'),
                Translator.translate_func_spec(r'((a:int /\ b:int) -> ((a / b):float))')
            }
        )
        self.assertEqual(result, expected_result)

    def test_set_apply_binop_spec_1(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state_set = Translator.translate_state_set(r'(a:T_a /\ b:T_b)')
        result = set_apply_binop_spec(state_set, binop_node, testmode=True)
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):complex) ^ '
                    r'(T_a` <= T_a /\ T_a` <= complex /\ T_b` <= T_b /\ T_b` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):float) ^ '
                    r'(T_a` <= T_a /\ T_a` <= float /\ T_b` <= T_b /\ T_b` <= float))'
                ),
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):float) ^ '
                    r'(T_a` <= T_a /\ T_a` <= int /\ T_b` <= T_b /\ T_b` <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_set_apply_binop_spec_2(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state_set = Translator.translate_state_set(
            r'((a:T_a /\ b:T_b) ^ (T_a <= int+float /\ T_b <= int+float)) \/ '
            r'(a:str /\ b:str)'
        )
        result = set_apply_binop_spec(state_set, binop_node, testmode=True)
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):complex) ^ '
                    r'(T_a <= int+float /\ T_b <= int+float /\ T_a` <= T_a /\ T_a` <= complex /\ T_b` <= T_b /\ T_b` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):float) ^ '
                    r'(T_a <= int+float /\ T_b <= int+float /\ T_a` <= T_a /\ T_a` <= float /\ T_b` <= T_b /\ T_b` <= float))'
                ),
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):float) ^ '
                    r'(T_a <= int+float /\ T_b <= int+float /\ T_a` <= T_a /\ T_a` <= int /\ T_b` <= T_b /\ T_b` <= int))'
                ),
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):complex) ^ '
                    r'(T_a` <= str /\ T_a` <= complex /\ T_b` <= str /\ T_b` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):float) ^ '
                    r'(T_a` <= str /\ T_a` <= float /\ T_b` <= str /\ T_b` <= float))'
                ),
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):float) ^ '
                    r'(T_a` <= str /\ T_a` <= int /\ T_b` <= str /\ T_b` <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_set_apply_binop_spec_3(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state_set = Translator.translate_state_set(
            r'(a:str /\ b:str)'
        )
        result = set_apply_binop_spec(state_set, binop_node, testmode=True)
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):complex) ^ '
                    r'(T_a` <= str /\ T_a` <= complex /\ T_b` <= str /\ T_b` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):float) ^ '
                    r'(T_a` <= str /\ T_a` <= float /\ T_b` <= str /\ T_b` <= float))'
                ),
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):float) ^ '
                    r'(T_a` <= str /\ T_a` <= int /\ T_b` <= str /\ T_b` <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_1(self):
        expr = 'a / b'
        state_set = Translator.translate_state_set(
            r'(a:str /\ b:str)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):complex) ^ '
                    r'(T_a` <= str /\ T_a` <= complex /\ T_b` <= str /\ T_b` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):float) ^ '
                    r'(T_a` <= str /\ T_a` <= float /\ T_b` <= str /\ T_b` <= float))'
                ),
                Translator.translate_state(
                    r'((a:T_a` /\ b:T_b` /\ (a / b):float) ^ '
                    r'(T_a` <= str /\ T_a` <= int /\ T_b` <= str /\ T_b` <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_2(self):
        expr = '(a >> b) / c'
        state_set = Translator.translate_state_set(
            r'(a:T_a /\ b:T_b /\ c:T_c)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'((a:T_1 /\ b:T_2 /\ c:T_4 /\ (a >> b):T_3 /\ ((a >> b) / c):float) ^ '
                    r'(T_1 <= T_a /\ T_1 <= int /\ T_2 <= T_b /\ T_2 <= int /\ T_4 <= int /\ T_3 <= int /\ T_4 <= T_c))'
                ),
                Translator.translate_state(
                    r'((a:T_1 /\ b:T_2 /\ c:T_4 /\ (a >> b):T_3 /\ ((a >> b) / c):float) ^ '
                    r'(T_1 <= T_a /\ T_1 <= int /\ T_2 <= T_b /\ T_2 <= int /\ T_4 <= float /\ T_3 <= int /\ T_3 <= float /\ T_4 <= T_c))'
                ),
                Translator.translate_state(
                    r'((a:T_1 /\ b:T_2 /\ c:T_4 /\ (a >> b):T_3 /\ ((a >> b) / c):complex) ^ '
                    r'(T_1 <= T_a /\ T_1 <= int /\ T_2 <= T_b /\ T_2 <= int /\ T_4 <= complex /\ T_3 <= int /\ T_3 <= complex /\ T_4 <= T_c))'
                ),
            }
        )
        self.assertEqual(result, expected_result)

    def test_visit_Constant_1(self):
        expr = '3'
        state_set = Translator.translate_state_set(
            r'(a:T_a /\ b:T_b) \/ (a:int /\ b:int)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'(a:T_a /\ b:T_b /\ (3):int)'
                ),
                Translator.translate_state(
                    r'(a:int /\ b:int /\ (3):int)'
                )
            }
        )
        self.assertEqual(result, expected_result)
