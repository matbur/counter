import unittest

from minimization import get_function, get_implicant, get_signal, to_bin


class TestMinimization(unittest.TestCase):
    def test_to_bin(self):
        self.assertEqual(to_bin('*'), '***')
        self.assertEqual(to_bin(0), '000')
        self.assertEqual(to_bin(1), '001')
        self.assertEqual(to_bin(2, 4), '0010')

    def test_get_signal(self):
        self.assertEqual(get_signal('-100', 3, 'd'), '/d')
        self.assertEqual(get_signal('11--', 2, 'c'), '')
        self.assertEqual(get_signal('-0--', 1, 'b'), '/b')
        self.assertEqual(get_signal('1--0', 0, 'a'), 'a')

    def test_get_implicant(self):
        self.assertEqual(get_implicant('-100', 'abcd'), 'b/c/d')
        self.assertEqual(get_implicant('11--', 'abcd'), 'ab')
        self.assertEqual(get_implicant('-0--', 'abcd'), '/b')
        self.assertEqual(get_implicant('1--0', 'abcd'), 'a/d')

    def test_get_function(self):
        self.assertEqual(get_function(['11-1', '00-1'], 'abcd'), 'abd + /a/bd')
        self.assertEqual(get_function(['1--0'], 'abcd'), 'a/d')
        self.assertEqual(get_function(['00-0', '1-1-'], 'abcd'), 'ac + /a/b/d')


if __name__ == '__main__':
    unittest.main()
