""" Module contains class which represents boolean function.
"""

from minimization import Minimization, to_bin
from .document import overline, subscript


class BooleanFunction(Minimization):
    def __init__(self, minterms, dontcares, signals, f_f, num):
        super().__init__(minterms, dontcares, signals)
        self.changed = None
        self.__f_f = f_f
        self.__num = num

        self.__change_negation()

    @classmethod
    def from_moves(cls, moves, width, f_f, num, signals=None):
        """ Method creates instance of class from given moves.

        :param moves: list of moves
        :param width: width of max move
        :param f_f: type of flip-flop
        :param num: number of flip-flop
        :param signals: names of signals
        :return: class instance
        """
        minterms = []
        dontcares = []

        list_map = {
            1: minterms,
            '*': dontcares,
            0: []
        }

        is_z = len(moves[0]) == 3

        for i, (*_, t, u) in enumerate(moves):
            tt = to_bin(t, width)[width - 1 - num]
            uu = to_bin(u, width)[width - 1 - num]
            ii = f_f(tt, uu)
            list_map[ii].append(i)

        if signals is None:
            signals = [subscript('Q', width - 1 - i, True) for i in range(width)]
            if is_z:
                signals.insert(0, 'Z')

        return cls(minterms, dontcares, signals, f_f, num)

    def get(self):
        """ Method returns boolean function in Latex syntax.

        :return: string with function
        """
        f_f = self.__f_f
        num = self.__num
        changed = self.changed
        return '${} = {}$'.format(subscript(f_f.name, num, True), changed)

    def __change_negation(self):
        """ Function changes sign / to overline.
        """
        function = self.function.split('/')

        for i, v in enumerate(function[1:], 1):
            function[i] = overline(v[0], True) + v[1:]

        self.changed = ''.join(function)
