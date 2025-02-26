import unittest
import sys
import os
from playground.typing_test import *


class NewTypeTester(unittest.TestCase):
    def test_eq_atomtype_1(self):
        at1 = AtomType(int)
        at2 = AtomType(float)
        self.assertNotEqual(at1, at2)

    def test_eq_atomtype_1(self):
        at1 = AtomType(int)
        at2 = AtomType(float)
        self.assertNotEqual(at1, at2)

    def test_eq_containertype_1(self):
        ct1 = ContainerType(list[int])
        ct2 = ContainerType(list[int])
        self.assertEqual(ct1, ct2)

    def test_eq_containertype_2(self):
        ct1 = ContainerType(list[int])
        ct2 = ContainerType(list[float])
        self.assertNotEqual(ct1, ct2)

    def test_eq_producttype_1(self):
        pt1 = ProductType(tuple[int, float])
        pt2 = ProductType(tuple[int, float])
        self.assertEqual(pt1, pt2)
    
    def test_eq_producttype_2(self):
        pt1 = ProductType(tuple[int, float])
        pt2 = ProductType(tuple[float, int])
        self.assertNotEqual(pt1, pt2)

    def test_eq_producttype_3(self):
        pt1 = ProductType(tuple[int, float])
        pt2 = ProductType(tuple[str])
        self.assertNotEqual(pt1, pt2)

    def test_eq_producttype_4(self):
        pt1 = ProductType(tuple[int])
        pt2 = ProductType(tuple[int])
        self.assertEqual(pt1, pt2)

    def test_eq_dicttype_1(self):
        dt1 = ProductType(dict[int, float])
        dt2 = ProductType(dict[int, float])
        self.assertEqual(dt1, dt2)
    
    def test_eq_dicttype_2(self):
        dt1 = ProductType(dict[int, float])
        dt2 = ProductType(dict[float, int])
        self.assertNotEqual(dt1, dt2)

    def test_eq_dicttype_3(self):
        dt1 = ProductType(dict[int, float])
        dt2 = ProductType(dict[str])
        self.assertNotEqual(dt1, dt2)

    def test_eq_dicttype_4(self):
        dt1 = ProductType(dict[int])
        dt2 = ProductType(dict[int])
        self.assertEqual(dt1, dt2)
    
    def test_eq_atomsumtype_1(self):
        at1 = AtomType(int)
        st1 = SumType(int | float)
        st1.__args__ = (create_basetype(int),)
        self.assertEqual(at1, st1)

    def test_eq_atomsumtype_2(self):
        at1 = AtomType(int)
        st1 = SumType(int | float)
        st1.__args__ = (create_basetype(int),)
        self.assertEqual(st1, at1)
