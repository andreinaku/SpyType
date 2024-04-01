import unittest
from statev2.transfer import *
from statev2.pyiparser_2 import *


class ParseTestCases(unittest.TestCase):
    def test_parse_node_type_1(self):
        node = ast.parse('list[int]').body[0].value
        cv = ClassdefToBasetypes()
        result = cv.parse_node_type(node)
        expected_result = Basetype({PyType(list, Basetype({PyType(int)}))})
        self.assertEqual(result, expected_result)

    def test_parse_node_type_2(self):
        node = ast.parse('int').body[0].value
        cv = ClassdefToBasetypes()
        result = cv.parse_node_type(node)
        expected_result = Basetype({PyType(int)})
        self.assertEqual(result, expected_result)

    def test_parse_node_type_3(self):
        node = ast.parse('dict[int, float]').body[0].value
        cv = ClassdefToBasetypes()
        result = cv.parse_node_type(node)
        expected_result = Basetype({PyType(dict, Basetype({PyType(int)}), Basetype({PyType(float)}))})
        self.assertEqual(result, expected_result)

    def test_parse_node_type_4(self):
        node = ast.parse('list[int, float]').body[0].value
        cv = ClassdefToBasetypes()
        result = cv.parse_node_type(node)
        expected_result = Basetype({PyType(list, Basetype({PyType(int), PyType(float)}))})
        self.assertEqual(result, expected_result)

    def test_parse_node_type_5(self):
        node = ast.parse('list[int | float]').body[0].value
        cv = ClassdefToBasetypes()
        result = cv.parse_node_type(node)
        expected_result = Basetype({PyType(list, Basetype({PyType(int), PyType(float)}))})
        self.assertEqual(result, expected_result)

    def test_parse_class_type_1(self):
        node = ast.parse('class type: ...')
        cv = ClassdefToBasetypes()
        cv.visit(node)
        result = cv.self_type
        expected_result = Basetype({PyType(type)})
        self.assertEqual(result, expected_result)

    def test_parse_class_type_2(self):
        node = ast.parse('class list(MutableSequence[_T], Generic[_T]):...')
        node = TypeReplacer().visit(node)
        cv = ClassdefToBasetypes()
        cv.visit(node)
        result = cv.self_type
        expected_result = Basetype({PyType(list, Basetype({VarType('_T')}))})
        self.assertEqual(result, expected_result)

    def test_parse_funcdef_1(self):
        code = '''
class int:
    def __add__(self, __value: int) -> int: ...
'''
        node = ast.parse(code)
        cv = ClassdefToBasetypes()
        cv.visit(node)
        result = list(cv.spec_dict['__add__'])[0]
        expected_result = FuncSpec()
        expected_result.in_state.assignment['self'] = Basetype({PyType(int)})
        expected_result.in_state.assignment['__value'] = Basetype({PyType(int)})
        expected_result.out_state.assignment['return'] = Basetype({PyType(int)})
        self.assertEqual(result, expected_result)

    def test_parse_funcdef_2(self):
        code = '''
class bytes(Sequence[int]):
    def __add__(self, __value: ReadableBuffer) -> _PositiveInteger: ...
'''
        node = ast.parse(code)
        cv = ClassdefToBasetypes()
        node = TypeReplacer().visit(node)
        cv.visit(node)
        result = list(cv.spec_dict['__add__'])[0]
        expected_result = FuncSpec()
        expected_result.in_state.assignment['self'] = Basetype({PyType(bytes)})
        expected_result.in_state.assignment['__value'] = Basetype({
            # bytes | bytearray | memoryview
            PyType(bytes), PyType(bytearray), PyType(memoryview)
        })
        expected_result.out_state.assignment['return'] = Basetype({PyType(int)})
        self.assertEqual(result, expected_result)

    def test_parse_funcdef_3(self):
        code = '''
class bytearray(MutableSequence[int]):
    def __iadd__(self, __value: ReadableBuffer) -> Self: ...
        '''
        node = ast.parse(code)
        cv = ClassdefToBasetypes()
        node = TypeReplacer().visit(node)
        cv.visit(node)
        result = list(cv.spec_dict['__iadd__'])[0]
        expected_result = FuncSpec()
        expected_result.in_state.assignment['self'] = Basetype({PyType(bytearray)})
        expected_result.in_state.assignment['__value'] = Basetype({
            # bytes | bytearray | memoryview
            PyType(bytes), PyType(bytearray), PyType(memoryview)
        })
        expected_result.out_state.assignment['return'] = Basetype({PyType(bytearray)})
        self.assertEqual(result, expected_result)

    def test_parse_funcdef_4(self):
        code = r'def len(__obj: Sized) -> int: ...'
        funcnode = ast.parse(code).body[0]
        # funcnode = TypeReplacer().visit(funcnode)
        result = ClassdefToBasetypes().parse_funcdef(funcnode)
        expected_result = Translator.translate_func_spec(
            r'((__obj:Sized) -> (return:int))'
        )
        self.assertEqual(result, expected_result)

    def test_parse_funcdef_5(self):
        code = r'def len(__obj: SupportsAbs[_T]) -> int: ...'
        funcnode = ast.parse(code).body[0]
        # funcnode = TypeReplacer().visit(funcnode)
        result = False
        try:
            aux = ClassdefToBasetypes().parse_funcdef(funcnode)
        except TypeError as te:
            result = True
        self.assertEqual(result, True)
