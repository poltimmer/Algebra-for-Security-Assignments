import unittest


class test1(unittest.TestCase):
    def testfunc1(self):
        assert 1 == 1

    def testfunc2(self):
        assert 2 == 2


class test2(unittest.TestCase):
    def testfunc3(self):
        assert 3 == 2


if __name__ == "__main__":
    unittest.main()
