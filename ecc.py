from random import randint

class FieldElement:

    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = 'Num {} not in field range 0 to {}'.format(num, prime - 1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return 'F({})'.format(self.num)
        # return 'F_{}( {} )'.format(self.prime, self.num)

    def __eq__(self, other):
        if other is None:
            return False
        elif other == 0:
            return self.num == 0
        else:
            return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        return self.arithmetic(other, lambda x, y: x + y)

    def __sub__(self, other):
        return self.arithmetic(other, lambda x, y: x - y)

    def __mul__(self, other):
        return self.arithmetic(other, lambda x, y: x * y)

    def __rmul__(self, m):
        p = self.prime
        n = self.num
        return self.__class__((n * m) % p, p)

    def __pow__(self, exponent):
        p = self.prime
        n = self.num
        return self.__class__(pow(n, exponent, p), p)

    def __truediv__(self, other):
        return self * (other ** -1)

    def arithmetic(self, other, op):
        self.assertSamePrime(other)
        p = self.prime
        n = op(self.num, other.num) % p
        return self.__class__(n, p)

    def assertSamePrime(self, other):
        if other is None:
            raise ValueError('...')
        if self.prime != other.prime:
            raise TypeError('...')
        return

#

P = 2**256 - 2**32 - 977

#

class S256Field(FieldElement):

    def __init__(self, num, prime=None):
        super().__init__(num, P)

    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)

#

class Point:
    # y^2 = x^3 + ax + b

    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        if x is None and y is None:
            return
        elif y**2 == x**3 + a*x + b:
            return
        error = 'Not a valid Point: (x,y,a,b)=({},{},{},{})'.format(x, y, a, b)
        raise ValueError(error)

    def __eq__(self, other):
        return self.x == other.x and \
                self.y == other.y and \
                self.a == other.a and \
                self.b == other.b

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        x = self.x
        y = self.y
        a = self.a
        b = self.b
        return 'Point({},{})'.format(x, y)
        # return 'Point_{{{}x+{}}}( {}, {} )'.format(a, b, x, y)

    def assertSameCurve(self, other):
        if other is None:
            raise ValueError('...')

        if self.a != other.a or self.b != other.b:
            raise TypeError('...')

        return

    def __add__(self, other):
        self.assertSameCurve(other)
        a = self.a
        b = self.b
        infinity = self.__class__(None, None, a, b)

        if self.x is None:
            return other
        elif other.x is None:
            return self
        elif self == other and self.y != 0:
            x1 = self.x
            y1 = self.y
            s = (3 * (x1**2) + a) / (2*y1)
            x = s**2 - x1 - x1
            y = s * (x1 - x) - y1
            return self.__class__(x, y, a, b)
        elif self == other and 2*self.y == 0:
            return infinity
        elif self.x == other.x and self.y != other.y:
            return infinity
        else:
            x1 = self.x
            y1 = self.y
            x2 = other.x
            y2 = other.y
            s = (y2 - y1) / (x2 - x1)
            x = s**2 - x1 - x2
            y = s * (x1 - x) - y1
            return self.__class__(x, y, a, b)

    def __rmul__(self, n):
        a = self.a
        b = self.b
        curr = self
        acc = self.__class__(None, None, a, b)
        while n > 0:
            if n & 1:
                acc = acc + curr
            curr = curr + curr
            n >>= 1
        return acc

#

Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

#

class S256Point(Point):

    def __init__(self, x, y, a=None, b=None):
        a = S256Field(0)
        b = S256Field(7)
        if type(x) == int and type(y) == int:
            super().__init__(S256Field(x), S256Field(y), a, b)
        else:
            super().__init__(x, y, a, b) # for Inf Point

    def __rmul__(self, n):
        if self.x.num == Gx and self.y.num == Gy:
            return super().__rmul__(n % N)
        else:
            return super().__rmul__(n)

    def verify(self, z, sig):
        s_inv = pow(sig.s, N-2, N)
        u = (z * s_inv) % N
        v = (sig.r * s_inv) % N
        comb = u * G + v * self
        return comb.x.num == sig.r
#

G = S256Point(Gx, Gy)
Z = S256Point(None, None)

#

class Signature:

    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Signature({:x},{:x})'.format(self.r, self.s)

#

class PrivateKey:

    def __init__(self, e):
        self.e = e
        self.point = e * G

    def hex(self):
        return '{:x}'.format(self.e).zfill(64)

    def sign(self, z):
        k = randint(0, N) # !!
        r = (k*G).x.num
        k_inv = pow(k, N-2, N)
        s = ((z + r * self.e) * k_inv) % N
        # https://bitcoin.stackexchange.com/questions/85946/low-s-value-in-bitcoin-signature
        if s > N/2:
            s = N - s
        return Signature(r, s)
