from ecc import Point
from ecc import FieldElement
from ecc import S256Point, N, G, Z
from ecc import Signature

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
        self.assertEqual(N * G, Z)

    def test_verify(self): # ch3-ex6
        # The Public Key:
        P = S256Point(
                0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c,
                0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34
                )
        tests = [
                {
                    'z': 0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60,
                    'r': 0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395,
                    's': 0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4
                    },
                {
                    'z': 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d,
                    'r': 0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c,
                    's': 0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6
                    }
                ]
        for test in tests:
            z = test['z']
            sig = Signature(test['r'], test['s'])
            self.assertEqual(P.verify(z, sig), True)


unittest.main(exit=False)
