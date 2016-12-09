""" Module contains class which represents table with binary moves.
"""

from minimization import to_bin
from .document import subscript
from .table import Table, multicolumn


class BinaryTable(Table):
    def __init__(self, moves, width, signals='QQ'):
        super().__init__([], moves, width)
        self.__signals = signals

        self.__fill_header()
        self.__fill_sub_header()
        self.__fill_content()
        self.__fill_rows()

    def __fill_header(self, arg=('t', 't+1')):
        """ Method fills header in table.

        :param arg: content of two multi columns
        """
        width = self._width

        self._header = [multicolumn(width, i) for i in arg]

    def __fill_sub_header(self):
        """ Method fills sub header in table.
        """
        signals = self.__signals
        width = self._width

        self._sub_header = [subscript(j, width - 1 - i) for j in signals for i in range(width)]

    def __fill_content(self):
        """ Method fills content of table.
        """
        moves = self._moves
        width = self._width

        self._content = [(*z, *to_bin(t, width), *to_bin(u, width)) for *z, t, u in moves]

    def __fill_rows(self):
        """ Method fills rows in table.
        """
        header = self._header
        sub_header = self._sub_header
        content = self._content
        moves = self._moves

        rows = [header, sub_header, *content]

        if len(moves[0]) == 3:
            rows[0].insert(0, '')
            rows[1].insert(0, '$Z$')

        self._rows = rows
