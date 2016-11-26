import unittest

from minimization import bin_len, to_bin


class TestMinimization(unittest.TestCase):
    def test_to_bin(self):
        self.assertEqual(to_bin('*'), '')
        self.assertEqual(to_bin(0), '0')
        self.assertEqual(to_bin(1), '1')
        self.assertEqual(to_bin(2, 4), '0010')

    def test_bin_len(self):
        self.assertEqual(bin_len(0), 1)
        self.assertEqual(bin_len(5), 3)
        self.assertEqual(bin_len(8), 4)
        self.assertEqual(bin_len(20), 5)
        self.assertEqual(bin_len(100), 7)


if __name__ == '__main__':
    unittest.main()
