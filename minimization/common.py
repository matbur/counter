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
