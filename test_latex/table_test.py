import unittest

from latex.table import multicolumn


class TestTable(unittest.TestCase):
    def test_multicolumn(self):
        self.assertEqual(multicolumn(1, 'v'), r'\multicolumn{1}{|c|}{v}')
        self.assertEqual(multicolumn(2, ''), r'\multicolumn{2}{|c|}{}')


if __name__ == '__main__':
    unittest.main()
