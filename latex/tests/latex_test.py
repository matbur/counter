import unittest

from latex_old import gen_row, multicolumn, subscript


class TestLatex(unittest.TestCase):
    def test_subscript(self):
        self.assertEqual(subscript('', ''), '$_{}$')
        self.assertEqual(subscript(1, 2), '$1_{2}$')

    def test_multicolumn(self):
        self.assertEqual(multicolumn(1, 'v'), r'\multicolumn{1}{|c|}{v}')
        self.assertEqual(multicolumn(2, ''), r'\multicolumn{2}{|c|}{}')

    def test_gen_row(self):
        self.assertEqual(gen_row(['a', 'b']), r'a & b \\')


if __name__ == '__main__':
    unittest.main()
