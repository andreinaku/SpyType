import unittest
from statev2.transfer import *


class ReprTestCases(unittest.TestCase):
    def test_basetype_spaces_1(self):
        bt = Basetype({PyType(set, Basetype({PyType(int), VarType('T1')}))})
        result = str(bt)
        expected_result_1 = 'set< int + T1 >'
        expected_result_2 = 'set< T1 + int >'
        self.assertEqual((result == expected_result_1) or (result == expected_result_2), True)
