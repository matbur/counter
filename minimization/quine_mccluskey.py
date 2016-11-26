""" Module contains class which runs Quine-McCluskey algorithm.
    more information:  https://en.wikipedia.org/wiki/Quine-McCluskey_algorithm
"""
import itertools

from common import bin_len, to_bin


class QuineMcCluskey:
    """ Class implements minimization with Quine-McCluskey algorithm.
    """

    def __init__(self, minterms, dontcares=(), signals=0):
        self.minterms = minterms
        self.dontcares = dontcares
        self.unused = set()

        self.__signals = signals
        self.__width = None
        self.__grouped = None
        self.__flattened = None
        self.__used = None

        self.__parse_signals()
        self.__calc_width()
        self.__parse_minterms()
        self.__run()

    def get(self):
        """ Method returns minimized implicants.

        :return: set
        """
        return self.unused

    def __parse_signals(self):
        """ Method changes signals to its length.
        """
        signals = self.__signals

        if not isinstance(signals, int):
            signals = len(signals)

        self.__signals = signals

    def __calc_width(self):
        """ Method calculates width of the minterms.
        """
        minterms = self.minterms
        dontcares = self.dontcares
        signals = self.__signals

        len_max = bin_len(max((*minterms, *dontcares)))

        self.__width = max(len_max, signals)

    def __parse_minterms(self):
        """ Method changes minterms and dontcares to binary value.
        """
        width = self.__width
        minterms = itertools.chain(self.minterms, self.dontcares)

        self.__flattened = [to_bin(i, width) for i in minterms]

    def __run(self):
        """ Method runs algorithm.
        """
        while self.__flattened:
            self.__group()
            self.__flat()
            self.__find_unused()

    def __group(self):
        """ Method groups items by number of 1s.
        """
        flattened = self.__flattened

        first = flattened[0]
        size = len(first) - first.count('-') + 1
        grouped = [[] for _ in range(size)]
        for minterm in flattened:
            num = minterm.count('1')
            # if minterm in grouped[num]:
            #     continue
            grouped[num].append(minterm)

        self.__grouped = grouped

    def __flat(self):
        """ Method flattens list of minterms and supplements set of used minterms.
        """
        grouped = self.__grouped
        are_similar = self.__are_similar
        merge = self.__merge

        used = set()
        minterms = []
        for group1, group2 in zip(grouped, grouped[1:]):
            for mint1 in group1:
                for mint2 in group2:
                    if not are_similar(mint1, mint2):
                        continue
                    minterms.append(merge(mint1, mint2))
                    used.add(mint1)
                    used.add(mint2)

        self.__used = used
        self.__flattened = minterms

    def __find_unused(self):
        """ Method supplements set of unused minterms.
        """
        grouped = self.__grouped
        used = self.__used

        self.unused |= {i for j in grouped for i in j} - used

    @staticmethod
    def __merge(this, other):
        """ Functions merges two minters to one similar.

        :param this: 1st minterm
        :param other: 2nd minterm
        :return: string
        """
        merged = (('-', i)[i == j] for i, j in zip(this, other))
        return ''.join(merged)

    @staticmethod
    def __are_similar(this, other):
        """ Function checks if two given implicants differ in one position.

        :param this: 1st minterm
        :param other: 2nd minterm
        :return: bool
        """
        differences = (i != j for i, j in zip(this, other))
        return sum(differences) == 1

    def __str__(self):
        return 'QMc: m={minterms}, d={dontcares}, u={unused}'.format_map(vars(self))


if __name__ == '__main__':
    m = [4, 8, 10, 11, 12, 15]
    d = [9, 14]
    s = 4
    qmc = QuineMcCluskey(m, d, s)
    print(qmc)
    print(qmc.get())
