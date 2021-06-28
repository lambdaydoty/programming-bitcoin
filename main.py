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

    def test_on_curve(self):
        valids = [(192, 105), (17, 56), (1, 193)]
        invalids = [(200, 119), (42, 99)]
        for x, y in valids:
            ECCTest.curve_a0_b7_F223(x, y)
        for x, y in invalids:
            with self.assertRaises(ValueError):
                ECCTest.curve_a0_b7_F223(x, y)

    def test_rmul(self):
        p = ECCTest.curve_a0_b7_F223(47, 71)
        q = ECCTest.curve_a0_b7_F223(154, 73)
        z = ECCTest.curve_a0_b7_F223(None, None)
        p_2 = ECCTest.curve_a0_b7_F223(36, 111)
        p_3 = ECCTest.curve_a0_b7_F223(15, 137)
        self.assertEqual(p + p, p_2)
        self.assertEqual(p + p + p, p_3)
        self.assertEqual(0 * p, z)
        self.assertEqual(1 * p, p)
        self.assertEqual(2 * p, p_2)
        self.assertEqual(11 * p, q)
        self.assertEqual(21 * p, z)

unittest.main(exit=False)
