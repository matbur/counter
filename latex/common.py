from itertools import repeat

from minimization import to_bin


def split(lst, width=4):
    """ Generator yields list in parts.

    :param lst: list
    :param width: length of each part
    """
    for i in range(len(lst) // width):
        yield lst[width * i:width * (i + 1)]


def gen_gray(width=2, isbin=True):
    """ Generator yields successive Gray numbers.

    :param width: number of bits
    """
    for i in range(1 << width):
        gray = i ^ (i >> 1)
        bin_gray = to_bin(gray, width)
        yield (gray, bin_gray)[isbin]


def gen_fields(r_num, c_num):
    """ Generator yields order in table for flip-flops.

    :param r_num: number of rows
    :param c_num: number of cols
    """
    rows = gen_gray(r_num, False)
    factor = repeat(1 << c_num)

    for fac, row in zip(factor, rows):
        cols = gen_gray(c_num, False)

        for col in cols:
            yield fac * row + col
