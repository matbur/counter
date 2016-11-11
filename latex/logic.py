from minimization import JK, get_minterms, minimize, to_bin
from .parts import gen_header, gen_tabular, multicolumn, overline, split, subscript

fields = [0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10]


def gen_gray(width=2):
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

    content = fields[:]
    for i, (*_, t, u) in zip(content[:], moves):
        t_n = to_bin(t)[2 - num]
        u_n = to_bin(u)[2 - num]
        content[i] = f_f(t_n, u_n)
    return content


def gen_moves(moves):
    """ Function generates table of moves with 2 or 3 column

    :param moves: list of moves
    :return: string containing whole table
    """
    n = len(moves[0])
    rows = (
        [multicolumn(n, '')],
        ['t', 't+1'],
        *moves
    )

    if n == 3:
        rows[1].insert(0, 'Z')

    return gen_tabular(rows)


def gen_bin_moves(moves):
    """ Function generates table of moves in binary system with 2 or 3 column

    :param moves: list of moves
    :return: string containing whole table
    """
    n = len(moves[0])
    rows = (
        [multicolumn(3, 't'), multicolumn(3, 't+1')],
        [subscript('Q', i) for i in '210'] * 2,
        *[(*z, *to_bin(t), *to_bin(u)) for *z, t, u in moves]
    )

    if n == 3:
        rows[0].insert(0, '')
        rows[1].insert(0, 'Z')

    return gen_tabular(rows)


def gen_flip_flops(moves):
    """ Function generates table of JK flip-flops according to moves

    :param moves: list of moves
    :return: string containing whole table
    """
    rows = [
        [multicolumn(6, 'Przerzutniki')],
        [subscript(i, j) for j in '210' for i in 'JK']
    ]

    for *_, t, u in moves:
        it = zip(to_bin(t), to_bin(u))
        rows.append(sum([JK(*next(it)) for _ in '210'], ()))

    return gen_tabular(rows)


def gen_flip_flop(moves, f_f, num):
    """ Function generates table ready to minimize

    :param moves: list of moves
    :param f_f: type of flip-flop
    :param num: number of column
    :return: string containing whole table
    """

    content = gen_flip_flop_content(moves, f_f, num)

    it_gray = gen_gray()
    it_con = split(content)
    rows = [
        [multicolumn(5, subscript(f_f.name, num))],
        (gen_header(), *gen_gray()),
        (next(it_gray), *next(it_con)),
        (next(it_gray), *next(it_con)),
    ]

    if len(moves[0]) == 3:
        rows.append((next(it_gray), *next(it_con)))
        rows.append((next(it_gray), *next(it_con)))

    return gen_tabular(rows)


def change_negation(function):
    l = function.split('/')
    for i, v in enumerate(l[1:], 1):
        l[i] = overline(v[0], True) + v[1:]
    return ''.join(l)


def generate_function(moves, f_f, num):
    data = gen_flip_flop_content(moves, f_f, num)
    minterms, dontcares = get_minterms(data)
    signals = ['Z', *(subscript('Q', i, True) for i in '210')]
    minimized = minimize(minterms, dontcares, signals)
    changed = change_negation(minimized)
    function = '${} = {}$'.format(subscript(f_f.name, num, True), changed)
    return function
