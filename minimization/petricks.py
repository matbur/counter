""" Module contains class which runs Petrick's method.
    more information: https://en.wikipedia.org/wiki/Petrick%27s_method
"""

from .common import to_bin


class Petricks:
    """ Class implements minimization with Petrick's method.
    """

    def __init__(self, implicants, minterms=()):
        self.implicants = implicants
        self.minterms = minterms
        self.minimized = None

        self.__width = None
        self.__paired = None
        self.__grouped = None

        self.__run()

    def get(self):
        """ Method returns minimized implicants.

        :return: set
        """
        return self.minimized

    def __run(self):
        """ Function runs algorithm.
        """
        self.__prepare()

        while len(self.__grouped) != 1:
            self.__step()

        minimized = self.__grouped[0]

        if isinstance(minimized[0], str):
            minimized = [{*minimized}]

        sort_key = self.__sort_key
        self.minimized = min(minimized, key=sort_key)

    @staticmethod
    def __sort_key(implicant):
        """ Function provides key to sort implicants

        :param implicant: string
        :return: tuple
        """
        return len(implicant), sorted(implicant)

    def __prepare(self):
        """ Method runs necessary methods in order to prepare data for algorithm.
        """
        self.__calc_width()
        self.__pair()
        self.__group()

    def __calc_width(self):
        """ Method calculates width of the implicants.
        """
        implicants = self.implicants

        self.__width = len(max(implicants))

    def __pair(self):
        """ Method creates pairs of implicant with matching number.
        """
        implicants = self.implicants
        gen_numbers = self.__gen_numbers

        paired = []
        for imp in implicants:
            for num in gen_numbers(imp):
                paired.append((imp, num))

        self.__paired = paired

    def __group(self):
        """ Method groups implicants by number.
        """
        width = self.__width
        minterms = self.minterms
        paired = self.__paired

        grouped = {}
        for term in minterms:
            grouped[term] = []
            for imp, num in paired:
                if num != to_bin(term, width):
                    continue
                grouped[term].append(imp)

        self.__grouped = list(grouped.values())

    def __step(self):
        """ Method runs one step in algorithm.
        """
        grouped = self.__grouped
        join = self.__join

        self.__grouped = [join(*i) for i in zip(grouped, grouped[1:])]

    @staticmethod
    def __gen_numbers(implicant):
        """ Generator yields all possible numbers from given implicant.

        :param implicant: implicant to spread
        """
        num = implicant.count('-')
        for i in range(1 << num):
            imp = implicant
            for bit in to_bin(i, num):
                imp = imp.replace('-', bit, 1)
            yield imp

    @staticmethod
    def __join(this, other):
        """ Function changes 2 lists into list of sets.

        :param this: 1st implicant or set of implicants
        :param other: 2nd implicant or set of implicants
        :return: list of joined implicants
        """
        parse = Petricks.__parse

        joined = []
        for i in this:
            for j in other:
                k = parse(i, j)
                if k in joined:
                    continue
                joined.append(k)
        return joined

    @staticmethod
    def __parse(this, other):
        """ Function parses two objects.

        :param this: 1st implicant or set of implicants
        :param other: 2nd implicant or set of implicants
        :return: set
        """
        if isinstance(this, set):
            return this | other
        return {this, other}

    def __str__(self):
        return 'P: i={} m={} d={}'.format(self.implicants, self.minterms, self.minimized)


if __name__ == '__main__':
    im = {'10--', '1-1-', '1--0', '-100'}
    mi = [4, 8, 10, 11, 12, 15]
    p = Petricks(im, mi)
    print(p)
    print(p.get())
