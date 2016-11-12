import unittest

from latex import change_negation, gen_gray, gen_row, gen_tabular, split


class TestLogic(unittest.TestCase):
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

    def test_gen_row(self):
        self.assertEqual(gen_row(['a']), r'a \\')
        self.assertEqual(gen_row(['a', 'b']), r'a & b \\')
        self.assertEqual(gen_row([1, 2, 3]), r'1 & 2 & 3 \\')

    def test_gen_tabular(self):
        self.assertEqual(gen_tabular([['row']]), r'\begin{tabular}{|c|} \hline row \\ \hline \end{tabular}')
        self.assertEqual(gen_tabular([['col1', 'col2']]),
                         r'\begin{tabular}{|c|c|} \hline col1 & col2 \\ \hline \end{tabular}')
        self.assertEqual(gen_tabular([['row1'], ['row2']]),
                         r'\begin{tabular}{|c|} \hline row1 \\ \hline row2 \\ \hline \end{tabular}')

    def test_change_negation(self):
        self.assertEqual(change_negation(''), '')
        self.assertEqual(change_negation('a/bc'), r'a\overline{b}c')
        self.assertEqual(change_negation('xy'), r'xy')


if __name__ == '__main__':
    unittest.main()
