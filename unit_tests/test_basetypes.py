from testbase import *
from statev2.Translator import *


class BasetypeTests(unittest.TestCase):
    def test_contains_atom_1(self):
        bt = Translator.translate_basetype('int + float + str')
        atom = Translator.translate_type('int')
        result = bt.contains_atom(atom, False)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_atom_2(self):
        bt = Translator.translate_basetype('int + float + str')
        atom = Translator.translate_type('complex')
        result = bt.contains_atom(atom, False)
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_contains_atom_3(self):
        bt = Translator.translate_basetype('list< int + float > + str')
        atom = Translator.translate_type('int')
        result = bt.contains_atom(atom, False)
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_contains_atom_4(self):
        bt = Translator.translate_basetype('list< int + float > + str')
        atom = Translator.translate_type('int')
        result = bt.contains_atom(atom, True)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_atom_5(self):
        bt = Translator.translate_basetype('int + float + str + T1')
        atom = Translator.translate_type('T1')
        result = bt.contains_atom(atom, False)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_atom_6(self):
        bt = Translator.translate_basetype('int + float + str + T1')
        atom = Translator.translate_type('T2')
        result = bt.contains_atom(atom, False)
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_contains_atom_7(self):
        bt = Translator.translate_basetype('int + tuple< float + str + list< T1 > >')
        atom = Translator.translate_type('T1')
        result = bt.contains_atom(atom, True)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_atom_8(self):
        bt = Translator.translate_basetype('int + tuple< float + str + list< T1 > >')
        atom = Translator.translate_type('T2')
        result = bt.contains_atom(atom, True)
        expected_result = False
        self.assertEqual(result, expected_result)
    
    def test_contains_basetype_1(self):
        bt1 = Translator.translate_basetype('int + float')
        bt2 = Translator.translate_basetype('int + float')
        result = bt1.contains_basetype(bt2) and (bt2 <= bt1)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_basetype_2(self):
        bt1 = Translator.translate_basetype('int + float')
        bt2 = Translator.translate_basetype('int + float + str')
        result = bt1.contains_basetype(bt2) and (bt2 <= bt1)
        expected_result = False
        self.assertEqual(result, expected_result)

    def test_contains_basetype_3(self):
        bt1 = Translator.translate_basetype('int + float + str')
        bt2 = Translator.translate_basetype('int + float')
        result = bt1.contains_basetype(bt2) and (bt2 <= bt1)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_basetype_4(self):
        bt1 = Translator.translate_basetype('int + float + list< int + float + str >')
        bt2 = Translator.translate_basetype('int + float + str')
        result = bt1.contains_basetype(bt2, True)
        expected_result = True
        self.assertEqual(result, expected_result)
    
    def test_contains_basetype_5(self):
        bt1 = Translator.translate_basetype('int + float + list< int + float + str >')
        bt2 = Translator.translate_basetype('complex + str')
        result = bt1.contains_basetype(bt2, True)
        expected_result = False
        self.assertEqual(result, expected_result)
    
    def test_contains_basetype_6(self):
        bt1 = Translator.translate_basetype('int + float + list< tuple < complex + str > + int >')
        bt2 = Translator.translate_basetype('complex + str')
        result = bt1.contains_basetype(bt2, True)
        expected_result = True
        self.assertEqual(result, expected_result)
    
    def test_contains_basetype_7(self):
        bt1 = Translator.translate_basetype('int + float + list< tuple < complex + T1 > + int >')
        bt2 = Translator.translate_basetype('complex + T1')
        result = bt1.contains_basetype(bt2, True)
        expected_result = True
        self.assertEqual(result, expected_result)

    def test_contains_basetype_8(self):
        bt1 = Translator.translate_basetype('int + float + list< tuple < complex + T1 > + int >')
        bt2 = Translator.translate_basetype('complex + T2')
        result = bt1.contains_basetype(bt2, True)
        expected_result = False
        self.assertEqual(result, expected_result)
