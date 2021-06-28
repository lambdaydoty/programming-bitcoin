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
        raise ValueError()

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
