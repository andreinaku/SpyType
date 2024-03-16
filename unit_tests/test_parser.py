import unittest
from statev2.transfer import *
from statev2.pyiparser_2 import *


class ParseTestCases(unittest.TestCase):
    def test_parse_node_type_1(self):
        node = ast.parse('list[int]').body[0].value
        result = parse_node_type(node)
        expected_result = Basetype({PyType(list, Basetype({PyType(int)}))})
        self.assertEqual(result, expected_result)

    def test_parse_node_type_2(self):
        node = ast.parse('int').body[0].value
        result = parse_node_type(node)
        expected_result = Basetype({PyType(int)})
        self.assertEqual(result, expected_result)

    def test_parse_node_type_3(self):
        node = ast.parse('dict[int, float]').body[0].value
        result = parse_node_type(node)
        expected_result = Basetype({PyType(dict, Basetype({PyType(int)}), Basetype({PyType(float)}))})
        self.assertEqual(result, expected_result)

    def test_parse_node_type_4(self):
        node = ast.parse('list[int, float]').body[0].value
        result = parse_node_type(node)
        expected_result = Basetype({PyType(list, Basetype({PyType(int), PyType(float)}))})
        self.assertEqual(result, expected_result)

    def test_parse_node_type_5(self):
        node = ast.parse('list[int | float]').body[0].value
        result = parse_node_type(node)
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
        cv = ClassdefToBasetypes()
        cv.visit(node)
        result = cv.self_type
        expected_result = Basetype({PyType(list, Basetype({VarType('T?0')}))})
        self.assertEqual(result, expected_result)
