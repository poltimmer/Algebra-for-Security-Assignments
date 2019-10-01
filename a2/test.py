import unittest

from polynomial import add_sub_poly, display_poly, long_div_poly, mul_poly
from utils import set_to_array  # pylint: disable=no-name-in-module


class TestUtils(unittest.TestCase):
    def test_set_to_array(self):
        assert set_to_array('{}') == []
        assert set_to_array('{1,2,3}') == [1, 2, 3]
        assert set_to_array('{-1,-2,-3}') == [-1, -2, -3]
        assert set_to_array('{333, -333}') == [333, -333]
        assert set_to_array('{0,0,0}') == [0, 0, 0]


class TestPoly(unittest.TestCase):
    def test_display_poly(self):
        obj = {}
        obj['mod'] = 12

        obj['f'] = [1, 2, 1]
        assert display_poly(obj)['answer'] == 'X^2+2X+1'

        obj['f'] = [0]
        assert display_poly(obj)['answer'] == '0'

        obj['f'] = []
        assert display_poly(obj)['answer'] == '0'

        obj['f'] = [14, 12, 11]
        assert display_poly(obj)['answer'] == '2X^2+11'

        obj['f'] = [12, 12, 12]
        assert display_poly(obj)['answer'] == '0'

        obj['f'] = [1, 2, 1, 1]
        assert display_poly(obj)['answer'] == 'X^3+2X^2+X+1'

        obj['f'] = [1, 2, 0, 0]
        assert display_poly(obj)['answer'] == 'X^3+2X^2'

        obj['f'] = [1, 2, 0, 1]
        assert display_poly(obj)['answer'] == 'X^3+2X^2+1'

        obj['f'] = [1, 2, 1, 0]
        assert display_poly(obj)['answer'] == 'X^3+2X^2+X'

        obj['f'] = [-2]
        assert display_poly(obj)['answer'] == '10'

        obj['f'] = [-11, 11]
        assert display_poly(obj)['answer'] == 'X+11'

        obj['f'] = [123, 13]
        assert display_poly(obj)['answer'] == '3X+1'

        obj['mod'] = 4
        obj['f'] = [5, 6, 7, 8]
        assert display_poly(obj)['answer'] == 'X^3+2X^2+3X'

    def test_add_sub_poly_add(self):
        obj = {}
        obj['mod'] = 12

        obj['f'] = [1, 2, 1]
        obj['g'] = [10, 11, 12, 13]
        assert add_sub_poly(obj, 'add')['answer'] == '10X^3+2X+2'

        obj['f'] = [0, 0, 0, 0, 0, 0, 0]
        obj['g'] = []
        assert add_sub_poly(obj, 'add')['answer'] == '0'

        obj['f'] = [33]
        obj['g'] = [11]
        assert add_sub_poly(obj, 'add')['answer'] == '8'

        obj['f'] = [10, 2]
        obj['g'] = [3, 5]
        assert add_sub_poly(obj, 'add')['answer'] == 'X+7'

        obj['f'] = [-7, 5, 6]
        obj['g'] = [4, 8]
        assert add_sub_poly(obj, 'add')['answer'] == '5X^2+9X+2'

        obj['f'] = [-3, -5, -3]
        obj['g'] = [-5, -3, -5]
        assert add_sub_poly(obj, 'add')['answer'] == '4X^2+4X+4'

        obj['mod'] = 3
        obj['f'] = [5, 3, 6, 9]
        obj['g'] = [1, 4, 3]
        assert add_sub_poly(obj, 'add')['answer'] == '2X^3+X^2+X'

    def test_add_sub_poly_sub(self):
        obj = {}
        obj['mod'] = 12

        obj['f'] = [1, 2, 1]
        obj['g'] = [10, 11, 12, 13]
        assert add_sub_poly(obj, 'sub')['answer'] == '2X^3+2X^2+2X'

        obj['f'] = [0, 0, 0, 0, 0, 0, 0]
        obj['g'] = []
        assert add_sub_poly(obj, 'sub')['answer'] == '0'

        obj['f'] = [33]
        obj['g'] = [11]
        assert add_sub_poly(obj, 'sub')['answer'] == '10'

        obj['f'] = [10, 2]
        obj['g'] = [3, 5]
        assert add_sub_poly(obj, 'sub')['answer'] == '7X+9'

        obj['f'] = [-7, 5, 6]
        obj['g'] = [4, 8]
        assert add_sub_poly(obj, 'sub')['answer'] == '5X^2+X+10'

        obj['f'] = [-3, -5, -3]
        obj['g'] = [-5, -3, -5]
        assert add_sub_poly(obj, 'sub')['answer'] == '2X^2+10X+2'

        obj['mod'] = 3
        obj['f'] = [5, 3, 6, 9]
        obj['g'] = [1, 4, 3]
        assert add_sub_poly(obj, 'sub')['answer'] == '2X^3+2X^2+2X'

    def test_mul_poly(self):
        obj = {}
        obj['mod'] = 7

        obj['f'] = [6]
        obj['g'] = [5]
        assert mul_poly(obj)['answer'] == '2'

        obj['f'] = [0, 0, 0, 0, 0, 0, 0]
        obj['g'] = []
        assert mul_poly(obj, 'sub')['answer'] == '0'

        obj['f'] = [33]
        obj['g'] = [27]
        assert mul_poly(obj, 'sub')['answer'] == '2'

        obj['f'] = [1,1,1]
        obj['g'] = [1,-1]
        assert mul_poly(obj, 'sub')['answer'] == 'X^3+6'

        obj['f'] = [2,3]
        obj['g'] = [1,6,1]
        assert mul_poly(obj, 'sub')['answer'] == '2X^3+X^2+6X+3'


    def test_long_div_poly(self):
        a = [3, 5, 2]
        b = [2, 1]
        m = 7
        assert long_div_poly(a, b, m) == [5, 0], [2]

        a = [6, -5, 2]
        b = [2, 1]
        m = 7
        assert long_div_poly(a, b, m) == [3, 3], [6]

        a = [-5, 2]
        b = [2, 1]
        m = 7
        assert long_div_poly(a, b, m) == [1], [1]


if __name__ == "__main__":
    unittest.main()
