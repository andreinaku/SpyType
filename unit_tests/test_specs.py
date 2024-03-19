import unittest
from statev2.transfer import *
from statev2.pyiparser_2 import VARTYPE_REPLACE


class SpecTestCases(unittest.TestCase):
    def test_apply_spec_1(self):
        state = Translator.translate_state(r'((a:int+float /\ b:int+float))')
        spec = Translator.translate_state(r'(a:float /\ b:int)')
        expected_result = Translator.translate_state(
            r'((a:Ta` /\ b:Tb`) ^ '
            r'((Ta` <= int+float) /\ (Ta` <= float) /\ (Tb` <= int+float) /\ (Tb` <= int))'
            r')'
        )
        result = state_apply_spec(state, spec, testmode=True)
        self.assertEqual(result, expected_result)

    def test_apply_spec_set_1(self):
        stateset = Translator.translate_state_set(
            r'((a:Ta /\ b:Tb))'
        )
        specset = Translator.translate_state_set(
            r'((a:int /\ b:int)) \/ ((a:float /\ b:float))'
        )
        expected_result = Translator.translate_state_set(
            r'((a:Ta` /\ b:Tb`) ^ (Ta` <= Ta /\ Ta` <= int /\ Tb` <= Tb /\ Tb` <= int)) \/ '
            r'((a:Ta` /\ b:Tb`) ^ (Ta` <= Ta /\ Ta` <= float /\ Tb` <= Tb /\ Tb` <= float))'
        )
        result = set_apply_spec(stateset, specset, testmode=True)
        self.assertEqual(result, expected_result)

    def test_apply_spec_set_2(self):
        stateset = Translator.translate_state_set(
            r'((a:Ta /\ b:Tb) ^ (Ta <= int+float /\ Tb <= str))'
        )
        specset = Translator.translate_state_set(
            r'((a:int /\ b:int)) \/ ((a:float /\ b:float))'
        )
        expected_result = Translator.translate_state_set(
            r'((a:Ta` /\ b:Tb`) ^ '
            r'(Ta` <= Ta /\ Ta` <= int /\ Tb` <= Tb /\ Tb` <= int /\ Ta <= int+float /\ Tb <= str)) \/ '
            r'((a:Ta` /\ b:Tb`) ^ '
            r'(Ta <= int+float /\ Tb <= str /\ Ta` <= Ta /\ Ta` <= float /\ Tb` <= Tb /\ Tb` <= float))'
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
        state_set = Translator.translate_state_set(r'(a:Ta /\ b:Tb)')
        result = set_apply_binop_spec(state_set, binop_node, testmode=True)
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):complex) ^ '
                    r'(Ta` <= Ta /\ Ta` <= complex /\ Tb` <= Tb /\ Tb` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= Ta /\ Ta` <= float /\ Tb` <= Tb /\ Tb` <= float))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= Ta /\ Ta` <= int /\ Tb` <= Tb /\ Tb` <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_set_apply_binop_spec_2(self):
        expr = 'a / b'
        binop_node = ast.parse(expr).body[0].value
        state_set = Translator.translate_state_set(
            r'((a:Ta /\ b:Tb) ^ (Ta <= int+float /\ Tb <= int+float)) \/ '
            r'(a:str /\ b:str)'
        )
        result = set_apply_binop_spec(state_set, binop_node, testmode=True)
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):complex) ^ '
                    r'(Ta <= int+float /\ Tb <= int+float /\ Ta` <= Ta /\ Ta` <= complex /\ Tb` <= Tb /\ Tb` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta <= int+float /\ Tb <= int+float /\ Ta` <= Ta /\ Ta` <= float /\ Tb` <= Tb /\ Tb` <= float))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta <= int+float /\ Tb <= int+float /\ Ta` <= Ta /\ Ta` <= int /\ Tb` <= Tb /\ Tb` <= int))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):complex) ^ '
                    r'(Ta` <= str /\ Ta` <= complex /\ Tb` <= str /\ Tb` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= float /\ Tb` <= str /\ Tb` <= float))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= int /\ Tb` <= str /\ Tb` <= int))'
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
                    r'((a:Ta` /\ b:Tb` /\ (a / b):complex) ^ '
                    r'(Ta` <= str /\ Ta` <= complex /\ Tb` <= str /\ Tb` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= float /\ Tb` <= str /\ Tb` <= float))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= int /\ Tb` <= str /\ Tb` <= int))'
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
                    r'((a:Ta` /\ b:Tb` /\ (a / b):complex) ^ '
                    r'(Ta` <= str /\ Ta` <= complex /\ Tb` <= str /\ Tb` <= complex))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= float /\ Tb` <= str /\ Tb` <= float))'
                ),
                Translator.translate_state(
                    r'((a:Ta` /\ b:Tb` /\ (a / b):float) ^ '
                    r'(Ta` <= str /\ Ta` <= int /\ Tb` <= str /\ Tb` <= int))'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_visit_BinOp_2(self):
        expr = '(a >> b) / c'
        state_set = Translator.translate_state_set(
            r'(a:Ta /\ b:Tb /\ c:Tc)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, False)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'((a:T1 /\ b:T2 /\ c:T4 /\ (a >> b):T3 /\ ((a >> b) / c):float) ^ '
                    r'(T1 <= Ta /\ T1 <= int /\ T2 <= Tb /\ T2 <= int /\ T4 <= int /\ T3 <= int /\ T4 <= Tc))'
                ),
                Translator.translate_state(
                    r'((a:T1 /\ b:T2 /\ c:T4 /\ (a >> b):T3 /\ ((a >> b) / c):float) ^ '
                    r'(T1 <= Ta /\ T1 <= int /\ T2 <= Tb /\ T2 <= int /\ T4 <= float /\ T3 <= int /\ T3 <= float /\ T4 <= Tc))'
                ),
                Translator.translate_state(
                    r'((a:T1 /\ b:T2 /\ c:T4 /\ (a >> b):T3 /\ ((a >> b) / c):complex) ^ '
                    r'(T1 <= Ta /\ T1 <= int /\ T2 <= Tb /\ T2 <= int /\ T4 <= complex /\ T3 <= int /\ T3 <= complex /\ T4 <= Tc))'
                ),
            }
        )
        self.assertEqual(result, expected_result)

    def test_visit_Constant_1(self):
        expr = '3'
        state_set = Translator.translate_state_set(
            r'(a:Ta /\ b:Tb) \/ (a:int /\ b:int)'
        )
        node = ast.parse(expr)
        tf = TransferFunc(state_set, True)
        tf.visit(node)
        result = tf.state_set
        expected_result = StateSet(
            {
                Translator.translate_state(
                    r'(a:Ta /\ b:Tb /\ (3):int)'
                ),
                Translator.translate_state(
                    r'(a:int /\ b:int /\ (3):int)'
                )
            }
        )
        self.assertEqual(result, expected_result)

    def test_basetype_replace_vartype_1(self):
        bt = Translator.translate_basetype('list< T_1 > + dict< T_K, T_V >')
        result = bt.replace_vartype('T_1', 'T?0')
        result = result.replace_vartype('T_K', 'T?K')
        result = result.replace_vartype('T_V', 'T?V')
        expected_result = Translator.translate_basetype('list< T?0 > + dict< T?K, T?V >')
        self.assertEqual(result, expected_result)

    def test_basetype_replace_vartype_2(self):
        bt = Basetype({
            PyType(list, Basetype({VarType('_T')})),
            PyType(dict, Basetype({VarType('_KT')}), Basetype({VarType('_VT')}))
        })
        for entry, replacement in VARTYPE_REPLACE.items():
            bt = bt.replace_vartype(entry, replacement)
        result = bt
        expected_result = Translator.translate_basetype('list< T?0 > + dict< T?K, T?V >')
        self.assertEqual(result, expected_result)
