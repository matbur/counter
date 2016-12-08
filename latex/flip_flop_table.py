"""
"""

from typing import Iterable

from .common import flatten, to_bin
from .document import subscript
from .table import Table, multicolumn


class FlipFlopTable(Table):
    def __init__(self, moves, f_f):
        self.__moves = moves
        self.__f_f = f_f
        self._rows = None
        self.__width = None

        self.__calc_width()
        self.__fill_rows()

    def __calc_width(self):
        moves = self.__moves
        used_moves = set(flatten(moves))
        self.__width = len(to_bin(max(used_moves)))

    def __gen_header(self):
        f_f = self.__f_f
        n = self.__width
        return [multicolumn(n * len(f_f.name), 'Przerzutniki')]

    def __gen_signals(self):
        f_f = self.__f_f
        n = self.__width
        return [subscript(i, n - 1 - j) for j in range(n) for i in f_f.name]

    def __fill_rows(self):
        """ Function generates table of flip-flops.
        """
        moves = self.__moves
        f_f = self.__f_f
        n = self.__width
        header = self.__gen_header()
        signals = self.__gen_signals()

        rows = [header, signals]

        for *_, t, u in moves:
            it = zip(to_bin(t, n), to_bin(u, n))
            l = [f_f(*next(it)) for _ in range(n)]

            if isinstance(l[0], Iterable):
                l = flatten(l)

            rows.append(l)

        self._rows = rows
