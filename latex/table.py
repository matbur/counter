class Table:
    __end = r'\end{tabular}'
    __hline = r'\hline'

    def __init__(self, rows):
        self._rows = rows

    def __begin_tabular(self):
        """ Function generates opening tag for table.

        :return: string in Latex syntax
        """
        tab = self._rows
        num = max(len(i) for i in tab) or 1
        return r'\begin{tabular}{|' + 'c|' * num + '}'

    @staticmethod
    def __gen_row(row):
        """ Function transforms list of items to one row from Latex.

        :param row: list of items
        :return: string, merged row
        """
        row = map(str, row)
        return ' & '.join(row) + r' \\'

    def gen_rows(self):
        rows = self._rows
        gen_row = self.__gen_row
        return (gen_row(i) for i in rows)

    def to_latex(self, sep=' '):
        """ Function combines all parts of table.

        :param sep: separator between rows
        :return: string, merged table
        """
        hline = self.__hline
        begin_tabular = self.__begin_tabular()
        gen_rows = self.gen_rows()
        end = self.__end

        rows = [begin_tabular, *gen_rows, end]
        return '{0}{1}{0}'.format(sep, hline).join(rows)

    def to_csv(self, sep=','):
        rows = self._rows
        return '\n'.join(sep.join(map(str, i)) for i in rows)


def multicolumn(width: int, value=''):
    """ Function merges n columns and fills it with value.

    :param width: number of merged columns
    :param value: text in merged columns
    :return: string in Latex syntax
    """
    return r'\multicolumn{{{}}}{{|c|}}{{{}}}'.format(width, value)
