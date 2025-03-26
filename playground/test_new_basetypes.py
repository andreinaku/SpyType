import unittest
import sys
import os
from typing_test import *
import _typeshed


class NewTypeTester(unittest.TestCase):
    def test_eq_atomtype_1(self):
        at1 = create_basetype(int)
        at2 = create_basetype(float)
        self.assertNotEqual(at1, at2)

    def test_eq_atomtype_1(self):
        at1 = create_basetype(int)
        at2 = create_basetype(float)
        self.assertNotEqual(at1, at2)

    def test_eq_containertype_1(self):
        ct1 = create_basetype(list[int])
        ct2 = create_basetype(list[int])
        self.assertEqual(ct1, ct2)

    def test_eq_containertype_2(self):
        ct1 = create_basetype(list[int])
        ct2 = create_basetype(list[float])
        self.assertNotEqual(ct1, ct2)

    def test_eq_producttype_1(self):
        pt1 = create_basetype(tuple[int, float])
        pt2 = create_basetype(tuple[int, float])
        self.assertEqual(pt1, pt2)
    
    def test_eq_producttype_2(self):
        pt1 = create_basetype(tuple[int, float])
        pt2 = create_basetype(tuple[float, int])
        self.assertNotEqual(pt1, pt2)

    def test_eq_producttype_3(self):
        pt1 = create_basetype(tuple[int, float])
        pt2 = create_basetype(tuple[str])
        self.assertNotEqual(pt1, pt2)

    def test_eq_producttype_4(self):
        pt1 = create_basetype(tuple[int])
        pt2 = create_basetype(tuple[int])
        self.assertEqual(pt1, pt2)

    def test_eq_dicttype_1(self):
        dt1 = create_basetype(dict[int, float])
        dt2 = create_basetype(dict[int, float])
        self.assertEqual(dt1, dt2)
    
    def test_eq_dicttype_2(self):
        dt1 = create_basetype(dict[int, float])
        dt2 = create_basetype(dict[float, int])
        self.assertNotEqual(dt1, dt2)

    def test_eq_dicttype_3(self):
        dt1 = create_basetype(dict[int, float])
        dt2 = create_basetype(dict[str])
        self.assertNotEqual(dt1, dt2)

    def test_eq_dicttype_4(self):
        dt1 = create_basetype(dict[int])
        dt2 = create_basetype(dict[int])
        self.assertEqual(dt1, dt2)
    
    def test_eq_atomsumtype_1(self):
        at1 = create_basetype(int)
        st1 = create_basetype(int | float)
        st1.__args__ = (create_basetype(int),)
        self.assertEqual(at1, st1)

    def test_eq_atomsumtype_2(self):
        at1 = create_basetype(int)
        st1 = create_basetype(int | float)
        st1.__args__ = (create_basetype(int),)
        self.assertEqual(st1, at1)

    def test_atom_atom_leq(self):
        # From actual type_pairs: int <= float, float <= SupportsAdd, etc.
        int_bt = create_basetype(int)
        float_bt = create_basetype(float)
        complex_bt = create_basetype(complex)

        # self.assertTrue(int_bt <= float_bt)   # if (int, float) is in type_pairs
        self.assertTrue(float_bt <= create_basetype(_typeshed.SupportsAdd))
        self.assertFalse(float_bt <= int_bt)  # float <= int likely not in type_pairs
        self.assertFalse(complex_bt <= int_bt)

    def test_atom_sum_leq(self):
        int_bt = create_basetype(int)
        float_bt = create_basetype(float)
        str_bt = create_basetype(str)

        union_bt = SumType.from_basetypes([int_bt, float_bt])

        self.assertTrue(int_bt <= union_bt)
        self.assertTrue(float_bt <= union_bt)
        self.assertFalse(str_bt <= union_bt)

    def test_container_leq(self):
        list_int = create_basetype(list[int])
        list_float = create_basetype(list[float])
        list_union = create_basetype(list[int | float])

        self.assertTrue(list_int <= list_union)
        self.assertFalse(list_float <= list_int)

    def test_product_leq(self):
        tup1 = create_basetype(tuple[int, float])
        tup2 = create_basetype(tuple[int | float, float | str])
        tup3 = create_basetype(tuple[int])

        self.assertTrue(tup1 <= tup2)
        self.assertFalse(tup1 <= tup3)

    def test_mismatched_types(self):
        int_bt = create_basetype(int)
        list_bt = create_basetype(list[int])
        tuple_bt = create_basetype(tuple[int])

        self.assertFalse(int_bt <= list_bt)
        self.assertFalse(list_bt <= tuple_bt)
        self.assertFalse(tuple_bt <= int_bt)
