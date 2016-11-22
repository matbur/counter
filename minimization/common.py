def to_bin(value, width=3):
    """ Function generates formatted int to bin.

    :param value: value to transform
    :param width: number of bits
    :return: formatted bin number
    """
    if value == '*':
        return '*' * width
    return '{0:0>{1}b}'.format(value, width)


# TODO: what if we do not have Z signal?
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

    d = {i[:2] for i in filled}
    a = {(i, j) for i in range(2) for j in range(8)}
    for _, t, u in list(filled):
        for _, i in a - d:
            if t != i:
                continue
            filled.append((1, t, u))
    return sorted(filled)


def get_signal(implicant, index, signal):
    """ Function generates positive, negative or none signal.

    :param implicant:
    :param index: index of signal
    :param signal: name of signal
    :return: proper signal symbol
    """
    return {
        '-': '',
        '0': '/' + signal,
        '1': signal
    }[implicant[index]]


def get_implicant(implicant, signals):
    """ Function generates positive, negative or none signal.

    :param implicant:
    :param signals: names of signals
    :return: implicant with names of signals
    """
    return ''.join(get_signal(implicant, i, v)
                   for i, v in enumerate(signals))


def get_function(implicants, signals):
    """ Function generates whole boolean function.

    :param implicants: list of minimized implicants
    :param signals: names of signals
    :return: boolean function
    """

    def sort_key(text):
        return ['10-'.index(sign) for sign in text]

    sorted_implicants = sorted(implicants, key=sort_key)
    return ' + '.join(get_implicant(i, signals)
                      for i in sorted_implicants)


def get_minterms(data, order):
    """ Function divides list of signals into minterms and dontcares.

    :param data: input signals
    :param order: order in which the data come
    :return: lists of minterms and dontcares
    """
    minterms = []
    dontcares = []
    lists = {
        1: minterms,
        '*': dontcares,
        0: []
    }
    for ind, value in zip(order, data):
        lists[value].append(ind)

    return minterms, dontcares
