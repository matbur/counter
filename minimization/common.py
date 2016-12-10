""" Module contains common functions for both minimization methods.
"""


def to_bin(value, width=0):
    """ Function generates formatted int to bin.

    :param value: value to transform
    :param width: number of bits
    :return: formatted bin number
    """
    if value == '*':
        return '*' * width
    return '{0:0>{1}b}'.format(value, width)


def bin_len(num):
    """ Function calculates number of bits in number.

    :param num: int
    :return: int
    """
    return len(to_bin(num))
