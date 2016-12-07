from minimization import Minimization, to_bin
from .common import flatten
from .document import overline, subscript


class BooleanFunction(Minimization):
    def __init__(self, minterms, dontcares, signals, f_f, num):
        super().__init__(minterms, dontcares, signals)
        self.changed = None
        self.__f_f = f_f
        self.__width = None
        self.__num = num

        self.change_negation()

    @classmethod
    def foo(cls, moves, f_f, num, signals=None):
        minterms = []
        dontcares = []

        list_map = {
            1: minterms,
            '*': dontcares,
            0: []
        }
        used_moves = set(flatten(moves)) - {'*'}
        n = len(to_bin(max(used_moves)))

        is_z = len(moves[0]) == 3

        for i, (*_, t, u) in enumerate(moves):
            tt = to_bin(t, n)[n - 1 - num]
            uu = to_bin(u, n)[n - 1 - num]
            ii = f_f(tt, uu)
            list_map[ii].append(i)

        if signals is None:
            signals = [subscript('Q', n - 1 - i, True) for i in range(n)]
            if is_z:
                signals.insert(0, 'Z')
        return cls(minterms, dontcares, signals, f_f, num)

    def __calc_width(self):
        moves = self.minterms + self.dontcares
        used_moves = set(moves) - {'*'}
        self.__width = len(to_bin(max(used_moves))) + int(len(moves[0]) == 3)

    def get(self):
        return '${} = {}$'.format(subscript(self.__f_f.name, self.__num, True), self.changed)

    def change_negation(self):
        """ Function changes sign / to overline.

        :param expression: boolean expression as string
        :return: changed expression
        """

        l = self.function.split('/')
        for i, v in enumerate(l[1:], 1):
            l[i] = overline(v[0], True) + v[1:]

        self.changed = ''.join(l)
