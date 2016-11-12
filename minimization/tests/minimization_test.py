import unittest

from minimization import group, like, merge, to_bin


class TestMinimization(unittest.TestCase):
    def test_to_bin(self):
        self.assertEqual(to_bin('*'), '***')
        self.assertEqual(to_bin(0), '000')
        self.assertEqual(to_bin(1), '001')
        self.assertEqual(to_bin(2, 4), '0010')

    def test_group(self):
        self.assertEqual(group([]), [])
        self.assertEqual(group(['0000', '1000', '1100', '1110', '1111']),
                         [['0000'], ['1000'], ['1100'], ['1110'], ['1111']])

    def test_merge(self):
        self.assertEqual(merge('0000', '0001'), '000-')
        self.assertEqual(merge('0-10', '0-11'), '0-1-')

    def test_like(self):
        self.assertTrue(like('0000', '0001'))
        self.assertTrue(like('100-', '101-'))
        self.assertTrue(like('0--1', '0--0'))
        self.assertTrue(like('0101', '0111'))
        self.assertTrue(like('--0-', '--1-'))
        self.assertTrue(like('-110', '-11-'))

        self.assertFalse(like('100-', '10-0'))
