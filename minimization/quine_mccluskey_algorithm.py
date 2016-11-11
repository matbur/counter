def merge(this, other):
    """ Functions merges two minters to one similar.

    :param this: 1st minterm
    :param other: 2nd minterm
    :return: merged minterm
    """
    merged = []
    for i, j in zip(this, other):
        merged.append(('-', i)[i == j])
    return ''.join(merged)


def like(this, other):
    """ Function checks if two given implicants differ in one position.

    :param this: 1st minterm
    :param other: 2nd minterm
    :return: bool
    """
    return sum(i != j for i, j in zip(this, other)) == 1


def get_unused(implicants, used):
    """ Function finds unused implicants from whole list.

    :param implicants: list of all implicants
    :param used: set of implicants which were used
    :return: set of unused implicants
    """
    # print('gen_numbers')
    # print('\timplicants', implicants)
    # print('\tused', used)

    implicants_set = set(sum(implicants, []))
    return implicants_set - used


def step(minterms):
    """ Function implements one step im minimization.

    :param minterms: list of implicants
    :return: tuple containing list of implicants and used implicants
    """
    # print('step')
    # print('\tminterms', minterms)

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
    # print('group')
    # print('\tminterms', minterms)

    if not minterms:
        return []

    first = minterms[0]
    size = len(first) - first.count('-') + 1
    grouped = [[] for _ in range(size)]
    for i in minterms:
        n = i.count('1')
        if i in grouped[n]:
            continue
        grouped[n].append(i)
    return grouped


def Quine_McCluskey_method(minterms):
    """

    :param minterms:
    :return:
    """
    # print('Quine_McCluskey_method')
    # print('\tminterms', minterms)

    unused = set()
    for _ in range(5):
        minterms = group(minterms)
        minterms, used = step(minterms)
        unused |= get_unused(*used)
        # print('unused', unused)
    return unused
