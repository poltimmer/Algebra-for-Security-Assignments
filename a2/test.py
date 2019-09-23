import unittest

from utils import set_to_array


class testUtils(unittest.TestCase):
    def test_set_to_array(self):
        assert set_to_array('{}') == []
        assert set_to_array('{1,2,3}') == [1, 2, 3]
        assert set_to_array('{-1,-2,-3}') == [-1, -2, -3]
        assert set_to_array('{333, -333}') == [333, -333]
        assert set_to_array('{0,0,0}') == [0, 0, 0]


class test1(unittest.TestCase):
    def testfunc1(self):
        assert 1 == 1

    def testfunc2(self):
        assert 2 == 2


class test2(unittest.TestCase):
    def testfunc3(self):
        assert 2 == 2


if __name__ == "__main__":
    unittest.main()
