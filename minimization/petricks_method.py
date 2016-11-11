from .common import to_bin


def gen_numbers(implicant):
    """

    :param implicant:
    """
    num = implicant.count('-')
    for i in range(1 << num):
        imp = implicant
        for bit in to_bin(i, num):
            imp = imp.replace('-', bit, 1)
        yield imp


def join(this, other):
    """

    :param this:
    :param other:
    :return:
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
    """

    :param imp_num:
    :param minterms:
    :return:
    """
    grouped = {}
    for term in minterms:
        grouped[term] = []
        for imp, num in imp_num:
            if num != to_bin(term, 4):
                continue
            grouped[term].append(imp)
    return list(grouped.values())


def pair_implicants(implicants):
    """

    :param implicants:
    """
    for imp in implicants:
        for num in gen_numbers(imp):
            yield imp, num


def Petricks_method(unused, minterms):
    """

    :param unused:
    :param minterms:
    :return:
    """
    # print('Petricks_method')
    # print('\tunused =', unused)
    # print('\tminterms =', minterms)

    pairs = tuple(pair_implicants(unused))
    # print('pairs =', pairs)

    results = group_implicants(pairs, minterms)
    # print('results', results)

    while len(results) != 1:
        results = [join(i, j) for i, j in zip(results, results[1:])]

    result = results[0]
    if isinstance(result[0], str):
        return result
    return min(result, key=len)
