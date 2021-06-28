from ecc import Point
from ecc import FieldElement

#
# !docker run -it --rm --volume `pwd`:/src --workdir /src jupyter/datascience-notebook:33add21fab64 python3 %
#
#
# y^2 = x^3 + ax + b, where a, b are FieldElement
#

import unittest

class ECCTest(unittest.TestCase):

    @staticmethod
    def curve_a0_b7_F223(_x, _y):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        if _x is None and _y is None:
            return Point(None, None, a, b)
        else:
            x = FieldElement(_x, prime)
            y = FieldElement(_y, prime)
            return Point(x, y, a, b)

    @staticmethod
    def curve_secp256k1(_x, _y):
        prime = 2**256 - 2**32 - 977
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        if _x is None and _y is None:
            return Point(None, None, a, b)
        else:
            x = FieldElement(_x, prime)
            y = FieldElement(_y, prime)
            return Point(x, y, a, b)

    def test_on_curve(self):
        valids = [(192, 105), (17, 56), (1, 193)]
        invalids = [(200, 119), (42, 99)]
        for x, y in valids:
            ECCTest.curve_a0_b7_F223(x, y)
        for x, y in invalids:
            with self.assertRaises(ValueError):
                ECCTest.curve_a0_b7_F223(x, y)

    def test_add(self): # ch3-ex2
        tests = [
                ((170, 142), (60, 139), (220, 181)),
                ((47,71), (17,56), (215,68)),
                ((143,98), (76,66), (47,71)),
                ]
        for (p_raw, q_raw, sumpq_raw) in tests:
            p = ECCTest.curve_a0_b7_F223(p_raw[0], p_raw[1])
            q = ECCTest.curve_a0_b7_F223(q_raw[0], q_raw[1])
            sumpq = ECCTest.curve_a0_b7_F223(sumpq_raw[0], sumpq_raw[1])
            self.assertEqual(p + q, sumpq)

    def test_rmul(self): # ch3-ex4
        tests = [
                (0, (47, 71), (None, None)),
                (1, (47, 71), (47, 71)),
                (2, (47, 71), (36, 111)),
                (3, (47, 71), (15, 137)),
                (11, (47, 71), (154, 73)),
                (21, (47, 71), (None, None)),
                ]
        for (s, (x1, y1), (x2, y2)) in tests:
            p = ECCTest.curve_a0_b7_F223(x1, y1)
            q = ECCTest.curve_a0_b7_F223(x2, y2)
            self.assertEqual(s * p, q)

    def test_find_order(self): # ch3-ex5
        p = ECCTest.curve_a0_b7_F223(15, 86)
        z = ECCTest.curve_a0_b7_F223(None, None)
        for i in range(1, 100):
            if i * p == z:
                self.assertEqual(i, 7)
                break

    def test_secp256k1_G(self):
        gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
        gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
        G = ECCTest.curve_secp256k1(gx, gy)
        z = ECCTest.curve_secp256k1(None, None)
        self.assertEqual(n * G, z)

unittest.main(exit=False)
