""" Module contains functions to run Petrick's method.
    more information: https://en.wikipedia.org/wiki/Petrick%27s_method
"""

from .common import to_bin


def gen_numbers(implicant):
    """ Generator yields all possible numbers from given implicant.

    :param implicant: implicant to spread
    """
    num = implicant.count('-')
    for i in range(1 << num):
        imp = implicant
        for bit in to_bin(i, num):
            imp = imp.replace('-', bit, 1)
        yield imp


def join(this, other):
    """ Function changes 2 lists into list of sets.

    :param this: 1st implicant or set of implicants
    :param other: 2nd implicant or set of implicants
    :return: list of joined implicants
    """
    joined = []
    for i in this:
        for j in other:
            k = {i, j} if isinstance(i, str) else i | j
            if k in joined:
                continue
            joined.append(k)
    return joined


def group_implicants(imp_num, minterms):
    """ Function groups implicants to corresponding minterms.

    :param imp_num: list of tuples (implicant, number)
    :param minterms: list of minterms
    :return: list of grouped minterms
    """
    grouped = {}
    for term in minterms:
        grouped[term] = []
        for imp, num in imp_num:
            if num != to_bin(term, 4):
                continue
            grouped[term].append(imp)
    return grouped.values()


def pair_implicants(implicants):
    """ Generator yields pairs of implicant with matching number.

    :param implicants: list of implicants
    """
    for imp in implicants:
        for num in gen_numbers(imp):
            yield imp, num


def Petricks_method(unused, minterms):
    """ Function runs algorithm.

    :param unused: set of unused implicants
    :param minterms: list of minterms
    :return: set of minimized implicants
    """
    pairs = tuple(pair_implicants(unused))
    results = list(group_implicants(pairs, minterms))

    while len(results) != 1:
        results = [join(i, j) for i, j in zip(results, results[1:])]

    result = results[0]
    if isinstance(result[0], str):
        return result
    return min(result, key=len)
