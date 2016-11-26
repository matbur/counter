import unittest

from minimization import Minimization


class TestMinimization(unittest.TestCase):
    def test_get_signal(self):
        get_signal = Minimization._Minimization__get_signal
        self.assertEqual(get_signal('-100', 3, 'd'), '/d')
        self.assertEqual(get_signal('11--', 2, 'c'), '')
        self.assertEqual(get_signal('-0--', 1, 'b'), '/b')
        self.assertEqual(get_signal('1--0', 0, 'a'), 'a')

    def test_all(self):
        self.assertEqual(Minimization([4, 8, 10, 11, 12, 15], [9, 14], 'abcd').get(), 'ac + a/d + b/c/d')
        self.assertEqual(Minimization.from_data(range(4), [0, 0, 1, 0], 'ab').get(), 'a/b')


if __name__ == '__main__':
    unittest.main()
