""" Module contains class which represents table in Latex syntax.
"""


class Table:
    __end = r'\end{tabular}'
    __hline = r'\hline'

    def __init__(self, rows, moves=(), width=0):
        self._rows = rows
        self._moves = moves
        self._width = width

        self._header = None
        self._sub_header = None
        self._content = None

    def __begin_tabular(self):
        """ Function generates opening tag for table.

        :return: string in Latex syntax
        """
        rows = self._rows
        c_num = max(len(i) for i in rows) or 1
        return r'\begin{tabular}{|' + 'c|' * c_num + '}'

    def __fill_header(self):
        pass

    def __fill_sub_header(self):
        pass

    def __fill_content(self):
        pass

    def __fill_rows(self):
        pass

    @staticmethod
    def __gen_row(row):
        """ Function transforms list of items to one row from Latex.

        :param row: list of items
        :return: string, merged row
        """
        row = map(str, row)
        return ' & '.join(row) + r' \\'

    def __gen_rows(self):
        """ Method merges each row to one string.

        :return: generated rows
        """
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
        rows = self.__gen_rows()
        end = self.__end

        tab = [begin_tabular, *rows, end]
        return '{0}{1}{0}'.format(sep, hline).join(tab)

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
