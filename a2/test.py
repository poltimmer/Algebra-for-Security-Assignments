import unittest

from polynomial import display_poly, add_poly, subtract_poly, long_div_poly, equals_poly_mod, mult, euclid_extended_poly
from utils import set_to_array  # pylint: disable=no-name-in-module


class TestUtils(unittest.TestCase):
    def test_set_to_array(self):
        assert set_to_array('{}') == []
        assert set_to_array('{1,2,3}') == [1, 2, 3]
        assert set_to_array('{-1,-2,-3}') == [-1, -2, -3]
        assert set_to_array('{333, -333}') == [333, -333]
        assert set_to_array('{0,0,0}') == [0, 0, 0]


class TestDisplayPoly(unittest.TestCase):
    def test_display_poly(self):
        m = 12

        f = [1, 2, 1]
        assert display_poly(f, m) == 'X^2+2X+1'

        f = [0]
        assert display_poly(f, m) == '0'

        f = []
        assert display_poly(f, m) == '0'

        f = [14, 12, 11]
        assert display_poly(f, m) == '2X^2+11'

        f = [12, 12, 12]
        assert display_poly(f, m) == '0'

        f = [1, 2, 1, 1]
        assert display_poly(f, m) == 'X^3+2X^2+X+1'

        f = [1, 2, 0, 0]
        assert display_poly(f, m) == 'X^3+2X^2'

        f = [1, 2, 0, 1]
        assert display_poly(f, m) == 'X^3+2X^2+1'

        f = [1, 2, 1, 0]
        assert display_poly(f, m) == 'X^3+2X^2+X'

        f = [-2]
        assert display_poly(f, m) == '10'

        f = [-11, 11]
        assert display_poly(f, m) == 'X+11'

        f = [123, 13]
        assert display_poly(f, m) == '3X+1'

        m = 4
        f = [5, 6, 7, 8]
        assert display_poly(f, m) == 'X^3+2X^2+3X'


class TestAddSubPoly(unittest.TestCase):
    def test_add_poly(self):
        m = 12

        f = [1, 2, 1]
        g = [10, 11, 12, 13]
        assert add_poly(f, g, m) == [10, 0, 2, 2]

        f = [0, 0, 0, 0, 0, 0, 0]
        g = []
        assert add_poly(f, g, m) == [0]

        f = [33]
        g = [11]
        assert add_poly(f, g, m) == [8]

        f = [10, 2]
        g = [3, 5]
        assert add_poly(f, g, m) == [1, 7]

        f = [-7, 5, 6]
        g = [4, 8]
        assert add_poly(f, g, m) == [5, 9, 2]

        f = [-3, -5, -3]
        g = [-5, -3, -5]
        assert add_poly(f, g, m) == [4, 4, 4]

        m = 3
        f = [5, 3, 6, 9]
        g = [1, 4, 3]
        assert add_poly(f, g, m) == [2, 1, 1, 0]

    def test_sub_poly(self):
        m = 12

        f = [1, 2, 1]
        g = [10, 11, 12, 13]
        assert subtract_poly(f, g, m) == [2, 2, 2, 0]

        f = [0, 0, 0, 0, 0, 0, 0]
        g = []
        assert subtract_poly(f, g, m) == [0]

        f = [33]
        g = [11]
        assert subtract_poly(f, g, m) == [10]

        f = [10, 2]
        g = [3, 5]
        assert subtract_poly(f, g, m) == [7, 9]

        f = [-7, 5, 6]
        g = [4, 8]
        assert subtract_poly(f, g, m) == [5, 1, 10]

        f = [-3, -5, -3]
        g = [-5, -3, -5]
        assert subtract_poly(f, g, m) == [2, 10, 2]

        m = 3
        f = [5, 3, 6, 9]
        g = [1, 4, 3]
        assert subtract_poly(f, g, m) == [2, 2, 2, 0]


class TestMultiplyPoly(unittest.TestCase):
    def test_mul_poly(self):
        m = 7

        f = [6]
        g = [5]
        assert mult(f, g, m) == [2]

        f = [0, 0, 0, 0, 0, 0, 0]
        g = []
        assert mult(f, g, m) == [0]

        f = [33]
        g = [27]
        assert mult(f, g, m) == [2]

        f = [1, 1, 1]
        g = [1, -1]
        assert mult(f, g, m) == [1, 0, 0, 6]

        f = [2, 3]
        g = [1, 6, 1]
        assert mult(f, g, m) == [2, 1, 6, 3]

        m = 5
        f = [-2, 3]
        g = [4]
        assert mult(f, g, m) == [2, 2]


class TestLongDivPoly(unittest.TestCase):
    def test1(self):
        a = [3, 5, 2]
        b = [2, 1]
        m = 7
        assert long_div_poly(a, b, m) == ([5, 0], [2])

    def test2(self):
        a = [6, -5, 2]
        b = [2, 1]
        m = 7
        assert long_div_poly(a, b, m) == ([3, 3], [6])

    def test3(self):
        a = [-5, 2]
        b = [2, 1]
        m = 7
        assert long_div_poly(a, b, m) == ([1], [1])


class TestEuclidPoly(unittest.TestCase):
    def test1(self):
        a = [1, 0, 1]
        b = [1, 0, 0, 1]
        m = 7
        assert euclid_extended_poly(a, b, m) == ([3, 3, 4], [4, 4], [1])
        # [answ-a] 3X^2+3X+4
        # [answ-b] 4X+4
        # [answ-d] 1

    def test2(self):
        a = [1, 0, 1]
        b = [1, 0, 0, 1]
        m = 2
        assert euclid_extended_poly(a, b, m) == ([1, 0], [1], [1, 1])
        # [answ-a] X
        # [answ-b] 1
        # [answ-d] X+1

    def test3(self):
        a = [1, 1, 1]
        b = [0]
        m = 7
        assert euclid_extended_poly(a, b, m) == ([1], [0], [1, 1, 1])
        # [answ-a] 1
        # [answ-b] 0
        # [answ-d] X^2+X+1

    def test4(self):
        a = [2, 2, 2]
        b = [0]
        m = 7
        assert euclid_extended_poly(a, b, m) == ([4], [0], [1, 1, 1])
        # [answ-a] 4
        # [answ-b] 0
        # [answ-d] X^2+X+1


class TestEqualsPoly(unittest.TestCase):
    def test_equals_poly_mod(self):
        m = 7

        f = [1, 1, 1]
        g = [10]
        h = [1, -1]
        assert equals_poly_mod(f, g, h, m) == 'TRUE'

        f = [1, 1, 1]
        g = [3]
        h = [0]
        assert equals_poly_mod(f, g, h, m) == 'FALSE'

        m = 5
        f = [1, 1, 1]
        g = [10]
        h = [1, -1]
        assert equals_poly_mod(f, g, h, m) == 'FALSE'
        
class TestIsIrreducible(unittest.TestCase):
    def test_is_irreducible(self):

        m = 3
        f = [2, 2, 1]
        assert is_irreducible(f, m) == 'FALSE'

        m = 2
        f = [1, 1, 1]
        assert is_irreducible(f, m) == 'TRUE'

        f = [1]
        assert is_irreducible(f, m) == 'DEGREE OF F IS TOO SMALL'



if __name__ == "__main__":
    unittest.main()
