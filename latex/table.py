class Table:
    __end = r'\end{tabular}'
    __hline = r'\hline'

    def __init__(self, rows):
        self._rows = rows

    def __begin_tabular(self):
        """ Function generates opening tag for table.

        :param width: number of column in table
        :return: string in Latex syntax
        """
        tab = self._rows
        num = max(len(i) for i in tab) or 1
        return r'\begin{tabular}{|' + 'c|' * num + '}'

    @staticmethod
    def gen_row(row):
        """ Function transforms list of items to one row from Latex.

        :param row: list of items
        :return: merged row
        """
        row = map(str, row)
        return ' & '.join(row) + r' \\'

    def gen_rows(self):
        rows = self._rows
        return (self.gen_row(i) for i in rows)

    # TODO: change name to to_latex
    def gen_tabular(self, sep=' '):
        """ Function combines all parts of table.

        :param rows: list of rows
        :param sep: separator between rows
        :return: string, merged table
        """
        s = [self.__begin_tabular(),
             *self.gen_rows(),
             self.__end]
        # sep = '\n'
        return '{0}{1}{0}'.format(sep, self.__hline).join(s)

    @staticmethod
    def multicolumn(width: int, value=''):
        """ Function merges n columns and fills it with value.

        :param width: number of merged columns
        :param value: text in merged columns
        :return: string in Latex syntax
        """
        return r'\multicolumn{{{}}}{{|c|}}{{{}}}'.format(width, value)

    def to_csv(self, sep=','):
        rows = self._rows
        return '\n'.join(sep.join(map(str, i)) for i in rows)


if __name__ == '__main__':
    t = Table([
        [1, 3],
        [2, 4]
    ])
    print(t.gen_tabular())
    print(t.to_csv())
