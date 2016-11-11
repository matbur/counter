""" Module contains functions to minimize boolean function
    with method Quine-McCluskey.
"""

from flip_flops import J, K

fields = [0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10]


def to_bin(value, width=3):
    """ Function generates formatted int to bin.

    :param value: value to transform
    :param width: number of bits
    :return: formatted bin number
    """
    if value == '*':
        return '***'
    return '{0:0>{1}b}'.format(value, width)


def complete_moves(moves):
    """ Function fills missing moves with '*'.

    :param moves: list of moves
    :return: completed, sorted list of moves
    """
    filled = list(moves)
    missing = set(range(8)) - set(i[-2] for i in filled)
    if len(moves[0]) == 3:
        for i in missing:
            filled.append((0, i, '*'))
            filled.append((1, i, '*'))
    else:
        for i in missing:
            filled.append((i, '*'))
    return sorted(filled)


def gen_Gray(width=2):
    """ Generator yields successive Gray numbers.

    :param width: number of bits
    """
    for i in range(1 << width):
        g = i ^ (i >> 1)
        yield '{0:0>{1}b}'.format(g, width)


def gen_flip_flop_content(moves, f_f, num):
    """ Function generates interior table to minimize for flip-flop.

    :param moves: list of movements
    :param f_f: type of flip-flop
    :param num: number of column
    :return: list with table
    """
    ff_map = {
        'J': J,
        'K': K,
    }

    content = fields[:]
    for i, (*_, t, u) in zip(content[:], moves):
        t_n = to_bin(t)[2 - num]
        u_n = to_bin(u)[2 - num]
        content[i] = ff_map[f_f](t_n, u_n)
    return content


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


def get_signal(implicant, index, signal):
    """

    :param implicant:
    :param index: index of signal
    :param signal: name of signal
    :return: proper signal symbol
    """
    # print('get_signal')
    # print('\timplicant', implicant)
    # print('\tindex', index)
    # print('\tsignal', signal)
    if implicant[index] == '-':
        return ''
    if implicant[index] == '0':
        return '/' + signal
    return signal


def get_minterm(implicant, signals):
    """

    :param implicant:
    :param signals: names of signals
    :return:
    """
    # print('get_minterm')
    # print('\timplicant', implicant)
    # print('\tsignals', signals)
    return ''.join(get_signal(implicant, i, v) for i, v in enumerate(signals))


def get_function(implicants, signals):
    """ Function generates whole boolean function.

    :param implicants: list of minimized implicants
    :param signals: names of signals
    :return: boolean function
    """

    # print('get_function')
    # print('\timplicants', implicants)
    # print('\tsignals', signals)

    def sort_key(x):
        return ['10-'.index(i) for i in x]

    sorted_implicants = sorted(implicants, key=sort_key)
    return ' + '.join(get_minterm(i, signals) for i in sorted_implicants)


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


def minimize(minterms, dontcares, signals):
    """ Function generates boolean function.

    :param minterms: list of minterms for which output function will be 1
    :param dontcares: list of minterms for which we don't care about the output
    :param signals: names of signals
    :return: boolean function
    """
    if not minterms:
        return '0'
    if len(minterms) + len(dontcares) == 16:
        return '1'

    united_minterms = [to_bin(i, 4) for i in minterms + dontcares]
    unused_implicants = Quine_McCluskey_method(united_minterms)
    minimized = Petricks_method(unused_implicants, minterms)
    return get_function(minimized, signals)


def get_minterms(data):
    minterms = []
    dontcares = []
    list_map = {
        1: minterms,
        '*': dontcares,
        0: []
    }
    for i, v in zip(fields, data):
        list_map[v].append(i)

    return minterms, dontcares


if __name__ == '__main__':
    minterms = [0, 1, 2, 4, 5, 6, 8, 9, 12, 13, 14]
    dontcares = []

    signals = 'abcd'

    minterms = [2,3,7]
    dontcares = [4,1,9]
    print(minimize(minterms, dontcares, signals))
