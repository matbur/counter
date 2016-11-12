""" Module contains functions to run Quine-McCluskey algorithm.
    more information:  https://en.wikipedia.org/wiki/Quine-McCluskey_algorithm
"""


def merge(this, other):
    """ Functions merges two minters to one similar.

    :param this: 1st minterm
    :param other: 2nd minterm
    :return: merged minterm
    """
    merged = (('-', i)[i == j] for i, j in zip(this, other))
    return ''.join(merged)


def like(this, other):
    """ Function checks if two given implicants differ in one position.

    :param this: 1st minterm
    :param other: 2nd minterm
    :return: bool
    """
    differences = (i != j for i, j in zip(this, other))
    return sum(differences) == 1


def get_unused(implicants, used):
    """ Function finds unused implicants from whole list.

    :param implicants: list of all implicants
    :param used: set of implicants which were used
    :return: set of unused implicants
    """
    implicants_set = set(sum(implicants, []))
    return implicants_set - used


def step(minterms):
    """ Function implements one step im minimization.

    :param minterms: list of implicants
    :return: tuple containing list of implicants and used implicants
    """
    result = []
    used = set()
    for i, j in zip(minterms, minterms[1:]):
        for x in i:
            for y in j:
                if not like(x, y):
                    continue
                result.append(merge(x, y))
                used.add(x)
                used.add(y)
    return result, (minterms, used)


def group(minterms):
    """ Function groups items by number of 1s.

    :param minterms: list of items to group
    :return: grouped list of lists
    """
    if not minterms:
        return []

    first = minterms[0]
    size = len(first) - first.count('-') + 1
    grouped = [[] for _ in range(size)]
    for minterm in minterms:
        num = minterm.count('1')
        if minterm in grouped[num]:
            continue
        grouped[num].append(minterm)
    return grouped


def quine_mccluskey_algorithm(minterms):
    """ Function runs algorithm.

    :param minterms: list of minterms
    :return: set of unused minterms
    """
    unused = set()
    for _ in range(5):
        minterms = group(minterms)
        minterms, used = step(minterms)
        unused |= get_unused(*used)
    return unused
