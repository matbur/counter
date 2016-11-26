from petricks import Petricks
from quine_mccluskey import QuineMcCluskey


class Minimization:
    def __init__(self, minterms, dontcares=(), signals=''):
        self.minterms = minterms
        self.dontcares = dontcares
        self.signals = signals
        self.function = None

        self.__minimized = None

        self.__run()

    @classmethod
    def from_data(cls, order, data, signals):
        """ Method creates object from list of signals.

        :param order: order in which the data come
        :param data: input signals
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
        for ind, value in zip(order, data):
            list_map[value].append(ind)

        return cls(minterms, dontcares, signals)

    def get(self):
        """ Method returns minimized function.

        :return: string
        """
        return self.function

    def __run(self):
        """ Method runs minimization.
        """
        minterms = self.minterms
        dontcares = self.dontcares
        signals = self.signals

        if not minterms:
            self.function = '0'
            return

        if len(minterms) + len(dontcares) == 1 << len(signals):
            self.function = '1'
            return

        qmc = QuineMcCluskey(minterms, dontcares, signals).get()
        ptr = Petricks(qmc, minterms).get()

        self.__minimized = ptr
        self.__get_function()

    def __get_function(self):
        """ Function generates whole boolean function.
        """
        implicants = self.__minimized
        get_implicant = self.__get_implicant
        sort_key = self.__sort_key

        implicants = sorted(implicants, key=sort_key)
        function = ' + '.join(get_implicant(i) for i in implicants)

        self.function = function

    @staticmethod
    def __sort_key(implicant):
        """ Function provides key for sorting implicants.

        :param implicant: string
        :return: list with indexes
        """
        return ['10-'.index(sign) for sign in implicant]

    def __get_implicant(self, implicant):
        """ Function generates positive, negative or none signal.

        :param implicant: string
        :return: string
        """
        signals = self.signals
        get_signal = self.__get_signal

        return ''.join(get_signal(implicant, *i)
                       for i in enumerate(signals))

    @staticmethod
    def __get_signal(implicant, index, signal):
        """ Function generates positive, negative or none signal.

        :param implicant: string
        :param index: index of signal
        :param signal: name of signal
        :return: string
        """
        return {
            '-': '',
            '0': '/' + signal,
            '1': signal
        }[implicant[index]]

    def __str__(self):
        return 'M: m={minterms}, d={dontcares}, s={signals!r}, f={function!r}'.format_map(vars(self))


if __name__ == '__main__':
    m = [4, 8, 10, 11, 12, 15]
    d = [9, 14]
    s = 'abcd'
    mi = Minimization(m, d, s)
    print(mi)
    print(mi.get())

    mi = Minimization.from_data(range(4), [0, 0, 0, 1], 'ab')
    print(mi)
    print(mi.get())
