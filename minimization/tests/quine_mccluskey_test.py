import unittest

from minimization import QuineMcCluskey


class TestQuineMcCluskey(unittest.TestCase):
    def test_merge(self):
        merge = QuineMcCluskey._QuineMcCluskey__merge

        self.assertEqual(merge('0000', '0001'), '000-')
        self.assertEqual(merge('0--0', '0--1'), '0---')
        self.assertEqual(merge('0-10', '0-11'), '0-1-')
        self.assertEqual(merge('--10', '--11'), '--1-')

    def test_are_similar(self):
        are_similar = QuineMcCluskey._QuineMcCluskey__are_similar

        self.assertTrue(are_similar('0000', '0001'))
        self.assertTrue(are_similar('100-', '101-'))
        self.assertTrue(are_similar('0--1', '0--0'))
        self.assertTrue(are_similar('0101', '0111'))
        self.assertTrue(are_similar('--0-', '--1-'))
        self.assertTrue(are_similar('-110', '-11-'))

        self.assertFalse(are_similar('100-', '10-0'))

        # def test_group(self):
        #     group = QuineMcCluskey._QuineMcCluskey__group
        #
        #     self.assertEqual(group([]), [])
        #     self.assertEqual(group(['0000', '1000', '1100', '1110', '1111']),
        #                      [['0000'], ['1000'], ['1100'], ['1110'], ['1111']])

    def test_all(self):
        self.assertSetEqual(QuineMcCluskey([0], [], 'abcd').get(), {'0000'})
        self.assertSetEqual(QuineMcCluskey([2], [], 'ab').get(), {'10'})
        self.assertSetEqual(QuineMcCluskey([4, 8, 10, 11, 12, 15], [9, 14], 'ab').get(),
                            {'1--0', '-100', '1-1-', '10--'})
        self.assertSetEqual(QuineMcCluskey([3, 4, 7, 8, 9, 13], [5, 6, 15]).get(),
                            {'100-', '0-11', '1-01', '01--', '-1-1'})
        self.assertSetEqual(QuineMcCluskey(range(4)).get(), {'--'})
        self.assertSetEqual(QuineMcCluskey([0, 1, 3]).get(), {'0-', '-1'})
        self.assertSetEqual(QuineMcCluskey([0, 1, 2, 5, 6, 7]).get(),
                            {'00-', '11-', '-01', '-10', '0-0', '1-1'})


if __name__ == '__main__':
    unittest.main()
