import unittest

from polynomial import display_poly
from utils import set_to_array


class testUtils(unittest.TestCase):
    def test_set_to_array(self):
        assert set_to_array('{}') == []
        assert set_to_array('{1,2,3}') == [1, 2, 3]
        assert set_to_array('{-1,-2,-3}') == [-1, -2, -3]
        assert set_to_array('{333, -333}') == [333, -333]
        assert set_to_array('{0,0,0}') == [0, 0, 0]


class testPoly(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
