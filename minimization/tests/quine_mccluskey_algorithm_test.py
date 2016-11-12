import unittest

from minimization import get_unused, group, like, merge


class TestQuineMcCluskeyAlgorithm(unittest.TestCase):
    def test_merge(self):
        self.assertEqual(merge('0000', '0001'), '000-')
        self.assertEqual(merge('0--0', '0--1'), '0---')
        self.assertEqual(merge('0-10', '0-11'), '0-1-')
        self.assertEqual(merge('--10', '--11'), '--1-')

    def test_like(self):
        self.assertTrue(like('0000', '0001'))
        self.assertTrue(like('100-', '101-'))
        self.assertTrue(like('0--1', '0--0'))
        self.assertTrue(like('0101', '0111'))
        self.assertTrue(like('--0-', '--1-'))
        self.assertTrue(like('-110', '-11-'))

        self.assertFalse(like('100-', '10-0'))

    def test_get_unused(self):
        self.assertSetEqual(get_unused([['000-'], ['0--0']], {'0--0'}), {'000-'})

    def test_group(self):
        self.assertEqual(group([]), [])
        self.assertEqual(group(['0000', '1000', '1100', '1110', '1111']),
                         [['0000'], ['1000'], ['1100'], ['1110'], ['1111']])


if __name__ == '__main__':
    unittest.main()
