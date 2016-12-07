# from latex import Table, subscript, to_bin
from .common import to_bin, flatten
from .document import subscript
from .table import Table


class FlipFlopTable(Table):
    def __init__(self, moves, f_f):
        self.__moves = moves
        self.__f_f = f_f
        self._rows = None

        self.fill_rows()

    def fill_rows(self):
        """ Function generates table of flip-flops.

        :param moves: list of moves
        :param f_f: flip-flop function
        :return: string containing whole table
        """
        moves = self.__moves
        f_f = self.__f_f
        # used_moves = sorted(set(sum(moves, ())))
        used_moves = sorted(set(flatten(moves)))
        # n = max(len(to_bin(i)) for i in used_moves)
        n = len(to_bin(max(used_moves)))
        rows = [
            [Table.multicolumn(n, 'Przerzutniki')],
            [subscript(i, n - 1 - j) for j in range(n) for i in f_f.name]
        ]

        for *_, t, u in moves:
            it = zip(to_bin(t, n), to_bin(u, n))
            rows.append([f_f(*next(it)) for _ in range(n)])

        self._rows = rows


if __name__ == '__main__':
    t = FlipFlopTable([
        [1, 2],
        [3, 4]
    ])

    print(t.gen_tabular())
    print(t.to_csv())
