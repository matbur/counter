import unittest

from latex import begin_tabular, gen_header, multicolumn, overline, subscript


class TestParts(unittest.TestCase):
    def test_overline(self):
        self.assertEqual(overline(''), r'$\overline{}$')
        self.assertEqual(overline('abc'), r'$\overline{abc}$')
        self.assertEqual(overline('', True), r'\overline{}')
        self.assertEqual(overline('abc', True), r'\overline{abc}')

    def test_subscript(self):
        self.assertEqual(subscript('', ''), '$_{}$')
        self.assertEqual(subscript(1, 2), '$1_{2}$')
        self.assertEqual(subscript(1, 2, True), '1_{2}')

    def test_gen_header(self):
        self.assertEqual(gen_header(), 'Z$Q_{2}$ / $Q_{1}$$Q_{0}$')

    def test_begin_tabular(self):
        self.assertEqual(begin_tabular(1), r'\begin{tabular}{|c|}')

    def test_multicolumn(self):
        self.assertEqual(multicolumn(1, 'v'), r'\multicolumn{1}{|c|}{v}')
        self.assertEqual(multicolumn(2, ''), r'\multicolumn{2}{|c|}{}')


if __name__ == '__main__':
    unittest.main()
