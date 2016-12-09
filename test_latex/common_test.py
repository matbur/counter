import unittest

from latex.common import flatten, gen_fields, gen_gray, split


class TestCommon(unittest.TestCase):
    def test_split(self):
        lst = list(range(10))
        self.assertEqual(list(split(lst)), [[0, 1, 2, 3], [4, 5, 6, 7]])
        self.assertEqual(list(split(lst, 2)), [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
        self.assertEqual(list(split(lst, 7)), [[0, 1, 2, 3, 4, 5, 6]])

    def test_gen_gray(self):
        self.assertEqual(list(gen_gray()), ['00', '01', '11', '10'])
        self.assertEqual(list(gen_gray(0)), ['0'])
        self.assertEqual(list(gen_gray(1)), ['0', '1'])
        self.assertEqual(list(gen_gray(2)), ['00', '01', '11', '10'])
        self.assertEqual(list(gen_gray(0, True)), ['0'])
        self.assertEqual(list(gen_gray(1, True)), ['0', '1'])
        self.assertEqual(list(gen_gray(2, True)), ['00', '01', '11', '10'])
        self.assertEqual(list(gen_gray(isbin=False)), [0, 1, 3, 2])
        self.assertEqual(list(gen_gray(0, False)), [0])
        self.assertEqual(list(gen_gray(1, False)), [0, 1])
        self.assertEqual(list(gen_gray(2, False)), [0, 1, 3, 2])
        self.assertEqual(list(gen_gray(3, False)), [0, 1, 3, 2, 6, 7, 5, 4])

    def test_gen_fields(self):
        self.assertEqual(list(gen_fields(1, 1)), [0, 1, 2, 3])
        self.assertEqual(list(gen_fields(1, 2)), [0, 1, 3, 2, 4, 5, 7, 6])
        self.assertEqual(list(gen_fields(2, 1)), [0, 1, 2, 3, 6, 7, 4, 5])
        self.assertEqual(list(gen_fields(2, 2)), [0, 1, 3, 2, 4, 5, 7, 6,
                                                  12, 13, 15, 14, 8, 9, 11, 10])

    def test_flatten(self):
        self.assertEqual(flatten([[1]]), (1,))
        self.assertEqual(flatten([[1], [2], [3]]), (1, 2, 3))


if __name__ == '__main__':
    unittest.main()
