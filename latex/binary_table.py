from minimization import to_bin
from .common import flatten
from .document import subscript
from .table import Table, multicolumn


class BinaryTable(Table):
    def __init__(self, moves, signals='QQ'):
        self.__moves = moves
        self.__signals = signals
        self.__width = None
        self._rows = None

        self.__calc_width()
        self.__fill_rows()

    def __calc_width(self):
        moves = self.__moves
        used_moves = set(flatten(moves))
        self.__width = len(to_bin(max(used_moves)))

    def __gen_header(self, arg=('t', 't+1')):
        width = self.__width
        return [multicolumn(width, i) for i in arg]

    def __gen_signals(self):
        signals = self.__signals
        width = self.__width
        return [subscript(j, width - 1 - i) for j in signals for i in range(width)]

    def __gen_content(self):
        moves = self.__moves
        width = self.__width
        return [(*z, *to_bin(t, width), *to_bin(u, width)) for *z, t, u in moves]

    def __fill_rows(self):
        """ Function generates table of moves in binary system with 2 or 3 column.

        :return: string containing whole table
        """
        moves = self.__moves

        header = self.__gen_header()
        signals = self.__gen_signals()
        content = self.__gen_content()

        rows = [header, signals, *content]

        if len(moves[0]) == 3:
            rows[0].insert(0, '')
            rows[1].insert(0, '$Z$')

        self._rows = rows
