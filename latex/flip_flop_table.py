""" Module contains class which represents table with flip-flop moves.
"""

from typing import Iterable

from .common import flatten, to_bin
from .document import subscript
from .table import Table, multicolumn


class FlipFlopTable(Table):
    def __init__(self, moves, width, f_f):
        super().__init__([], moves, width)
        self.__f_f = f_f

        self.__fill_header()
        self.__fill_sub_header()
        self.__fill_content()
        self.__fill_rows()

    def __fill_header(self):
        """ Method fills header in table.
        """
        f_f = self.__f_f
        width = self._width
        self._header = [multicolumn(width * len(f_f.name), 'Przerzutniki')]

    def __fill_sub_header(self):
        """ Method fills sub header in table.
        """
        f_f = self.__f_f
        width = self._width
        self._sub_header = [subscript(i, width - 1 - j) for j in range(width) for i in f_f.name]

    def __fill_content(self):
        """ Method fills content of table.
        """
        f_f = self.__f_f
        moves = self._moves
        width = self._width

        content = []
        for *_, t, u in moves:
            it = zip(to_bin(t, width), to_bin(u, width))
            l = [f_f(*next(it)) for _ in range(width)]

            if isinstance(l[0], Iterable):
                l = flatten(l)

            content.append(l)

        self._content = content

    def __fill_rows(self):
        """ Method fills rows in table.
        """
        header = self._header
        sub_header = self._sub_header
        content = self._content

        self._rows = [header, sub_header, *content]
