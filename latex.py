""" Module contains all necessary functions to generate complete
    minimization method Karnaugh.
"""

from flip_flops import JK
from minimization import gen_Gray, gen_flip_flop_content, get_minterms, minimize, to_bin

file_header = r"""
\documentclass[11pt]{article}

\usepackage[margin=1in]{geometry}

\begin{document}
"""
file_footer = r'\end{document}'

hline = r'\hline'
end_tabular = r'\end{tabular}'


# TODO: write tests and docstring
def overline(text, isinside=False):
    result = r'\overline{{{}}}'.format(text)
    if isinside:
        return result
    return '$' + result + '$'


def gen_header():
    """ Function generates header for flip-flop table.

    :return: common table header
    """
    return 'Z' + subscript('Q', 2) + ' / ' + subscript('Q', 1) + subscript('Q', 0)


def split(lst, width=4):
    """ Generator yields lst in parts.

    :param lst: list of elements
    :param width: length of each part
    """
    for i in range(len(lst) // width):
        yield lst[width * i:width * (i + 1)]


def begin_tabular(width: int):
    """ Function returns opening tag for table.

    :param width: number of column in table
    :return: string which starts table
    """
    return r'\begin{tabular}{|' + 'c|' * width + '}'


def subscript(big, small, isinside=False):
    """ Function returns proper syntax for subscript.

    :param big: value which should be up and big
    :param small: value which should be down and small
    :return: string in Latex syntax
    """
    result = '{}_{{{}}}'.format(big, small)
    if isinside:
        return result
    return '$' + result + '$'


def multicolumn(width: int, value=''):
    """ Function merges n columns and fills it with value.

    :param width: number of merged columns
    :param value: text in merged columns
    :return: string
    """
    return r'\multicolumn{{{}}}{{|c|}}{{{}}}'.format(width, value)


def gen_row(row):
    """ Function transforms list of items to one row from Latex.

    :param row: list of items
    :return: string, merged row
    """
    row = map(str, row)
    return ' & '.join(row) + r' \\'


def gen_tabular(rows, sep=' '):
    """ Function combines all parts of table.

    :param rows: list of rows
    :param sep: separator between rows
    :return: string, merged table
    """
    n = max(len(row) for row in rows)
    s = [begin_tabular(n)]

    for row in rows:
        s.append(gen_row(row))

    s.append(end_tabular)
    # sep = '\n'
    return '{0}{1}{0}'.format(sep, hline).join(s)


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

    it_gray = gen_Gray()
    it_con = split(content)
    rows = [
        [multicolumn(5, subscript(f_f, num))],
        (gen_header(), *gen_Gray()),
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
    signals = ['Z', subscript('Q', 2, True), subscript('Q', 1, True), subscript('Q', 0, True)]
    minimized = minimize(minterms, dontcares, signals)
    changed = change_negation(minimized)
    function = '${} = {}$'.format(subscript(f_f, num, True), changed)
    return function


if __name__ == '__main__':
    pass
