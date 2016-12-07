# from latex import Table, subscript, to_bin
from .common import flatten, to_bin
from .document import subscript
from .table import Table


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
        self.__width = len(to_bin(max(used_moves))) + int(len(moves[0]) == 3)

    def __fill_rows(self):
        """ Function generates table of flip-flops.
        """
        moves = self.__moves
        f_f = self.__f_f
        n = self.__width

        rows = [
            [Table.multicolumn(n, 'Przerzutniki')],
            [subscript(i, n - 1 - j) for j in range(n) for i in f_f.name]
        ]

        for *_, t, u in moves:
            it = zip(to_bin(t, n), to_bin(u, n))
            rows.append([f_f(*next(it)) for _ in range(n)])

        self._rows = rows
