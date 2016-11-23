""" Module contains logic to create latex file.
"""

from minimization import D, J, JK, K, T, complete_moves, get_minterms, minimize, to_bin
from .parts import begin_tabular, end_tabular, file_footer, file_header, gen_header, hline, minipage, multicolumn, \
    overline, subscript, subsection, vspace

fields = (0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10)


def split(lst, width=4):
    """ Generator yields lst in parts.

    :param lst: list of elements
    :param width: length of each part
    """
    for i in range(len(lst) // width):
        yield lst[width * i:width * (i + 1)]


def gen_gray(width=2):
    """ Generator yields successive Gray numbers.

    :param width: number of bits
    """
    for i in range(1 << width):
        gray = i ^ (i >> 1)
        yield '{0:0>{1}b}'.format(gray, width)


def gen_row(row):
    """ Function transforms list of items to one row from Latex.

    :param row: list of items
    :return: merged row
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
    s = [begin_tabular(n),
         *(gen_row(row) for row in rows),
         end_tabular]
    # sep = '\n'
    return '{0}{1}{0}'.format(sep, hline).join(s)


def gen_flip_flop_content(moves, f_f, num):
    """ Function generates interior table to minimize for flip-flop.

    :param moves: list of movements
    :param f_f: type of flip-flop
    :param num: number of column
    :return: list with table
    """

    content = list(fields)
    for i, (*_, t, u) in zip(content[:], moves):
        t_n = to_bin(t)[2 - num]
        u_n = to_bin(u)[2 - num]
        content[i] = f_f(t_n, u_n)
    return content


def gen_input_table():
    """ Function generates table with input signals.

    :return: string in Latex syntax
    """
    rows = (
        ('', '$Z$'),
        (subscript('z', '0'), 0),
        (subscript('z', '1'), 1),
    )
    return gen_tabular(rows)


def gen_output_table():
    """ Function generates table with output signals.

    :return: string in Latex syntax
    """
    rows = (
        ('', '$Y$'),
        (subscript('y', '0'), 0),
        (subscript('y', '1'), 1),
    )
    return gen_tabular(rows)


def gen_states_table(moves):
    """ Function generates table with states.

    :param moves: list of used states
    :return: string in Latex syntax
    """
    moves = sorted(set(moves))
    rows = (
        [subscript('Q', i) for i in '210'],
        *[(subscript('q', i), *to_bin(i)) for i in moves]
    )

    rows[0].insert(0, '')

    return gen_tabular(rows)


def gen_moves_table(moves):
    """ Function generates table of moves with 2 or 3 column.

    :param moves: list of moves
    :return: string containing whole table
    """
    n = len(moves[0])
    rows = (
        ['t', 't+1'],
        *moves
    )

    if n == 3:
        rows[0].insert(0, '$Z$')

    return gen_tabular(rows)


def gen_bin_moves_table(moves):
    """ Function generates table of moves in binary system with 2 or 3 column.

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
        rows[1].insert(0, '$Z$')

    return gen_tabular(rows)


def gen_jk_flip_flops_table(moves):
    """ Function generates table of JK flip-flops according to moves.

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


def gen_all_flip_flops_table(moves, f_f):
    """ Function generates table of JK flip-flops according to moves.

    :param moves: list of moves
    :return: string containing whole table
    """
    rows = [
        [multicolumn(3, 'Przerzutniki')],
        [subscript(i, j) for j in '210' for i in f_f.name]
    ]

    for *_, t, u in moves:
        it = zip(to_bin(t), to_bin(u))
        rows.append([f_f(*next(it)) for _ in '210'])

    return gen_tabular(rows)


def gen_flip_flop_table(moves, f_f, num):
    """ Function generates table ready to minimize.

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


def change_negation(expression):
    """ Function changes sign / to overline.

    :param expression: boolean expression as string
    :return: changed expression
    """
    l = expression.split('/')
    for i, v in enumerate(l[1:], 1):
        l[i] = overline(v[0], True) + v[1:]
    return ''.join(l)


def gen_boolean_function(moves, f_f, num):
    """ Function generates boolean function from given moves.

    :param moves: list of movements
    :param f_f: flip-flop function
    :param num: number of flip-flop
    :return: minimized boolean function in Latex syntax
    """
    data = gen_flip_flop_content(moves, f_f, num)
    minterms, dontcares = get_minterms(data, fields)
    signals = ['Z', *(subscript('Q', i, True) for i in '210')]
    minimized = minimize(minterms, dontcares, signals)
    changed = change_negation(minimized)
    function = '${} = {}$'.format(subscript(f_f.name, num, True), changed)
    return function


def gen_jk_tables(sorted_moves, full_moves):
    """ Function generates all tables with JK flip-flops.

    :param sorted_moves: list of sorted moves
    :param full_moves: complete list of moves
    :return: string in Latex syntax
    """
    return '\n'.join((
        subsection('Tabela przejsc dla przerzutnikow JK'),
        gen_bin_moves_table(sorted_moves),
        gen_jk_flip_flops_table(sorted_moves),
        vspace(), '',
        subsection('Minimalizacja metoda Karnough dla przerzutkow JK'),
        minipage((
            gen_flip_flop_table(full_moves, J, 2),
            vspace(.3), '',
            gen_boolean_function(full_moves, J, 2),
        )),
        minipage((
            gen_flip_flop_table(full_moves, K, 2),
            vspace(.3), '',
            gen_boolean_function(full_moves, K, 2),
        )),
        vspace(), '',
        minipage((
            gen_flip_flop_table(full_moves, J, 1),
            vspace(.3), '',
            gen_boolean_function(full_moves, J, 1),
        )),
        minipage((
            gen_flip_flop_table(full_moves, K, 1),
            vspace(.3), '',
            gen_boolean_function(full_moves, K, 1),
        )),
        vspace(), '',
        minipage((
            gen_flip_flop_table(full_moves, J, 0),
            vspace(.3), '',
            gen_boolean_function(full_moves, J, 0),
        )),
        minipage((
            gen_flip_flop_table(full_moves, K, 0),
            vspace(.3), '',
            gen_boolean_function(full_moves, K, 0),
        )),
    ))


def gen_d_tables(sorted_moves, full_moves):
    """ Function generates all tables with D flip-flops.

    :param sorted_moves: list of sorted moves
    :param full_moves: complete list of moves
    :return: string in Latex syntax
    """
    return '\n'.join((
        subsection('Tabela przejsc dla przerzutkow D'),
        gen_bin_moves_table(sorted_moves),
        gen_all_flip_flops_table(sorted_moves, D),
        vspace(), '',
        subsection('Minimalizacja metoda Karnough dla przerzutkow D'),
        minipage((
            gen_flip_flop_table(full_moves, D, 2),
            vspace(.3), '',
            gen_boolean_function(full_moves, D, 2),
        )),
        minipage((
            gen_flip_flop_table(full_moves, D, 1),
            vspace(.3), '',
            gen_boolean_function(full_moves, D, 1),
        )),
        vspace(), '',
        minipage((
            gen_flip_flop_table(full_moves, D, 0),
            vspace(.3), '',
            gen_boolean_function(full_moves, D, 0),
        )),
    ))


def gen_t_tables(sorted_moves, full_moves):
    """ Function generates all tables with T flip-flops.

    :param sorted_moves: list of sorted moves
    :param full_moves: complete list of moves
    :return: string in Latex syntax
    """
    return '\n'.join((
        subsection('Tabela przejsc dla przerzutkow T'),
        gen_bin_moves_table(sorted_moves),
        gen_all_flip_flops_table(sorted_moves, T),
        vspace(), '',
        subsection('Minimalizacja metoda Karnough dla przerzutkow T'),
        minipage((
            gen_flip_flop_table(full_moves, T, 2),
            vspace(.3), '',
            gen_boolean_function(full_moves, T, 2),
        )),
        minipage((
            gen_flip_flop_table(full_moves, T, 1),
            vspace(.3), '',
            gen_boolean_function(full_moves, T, 1),
        )),
        vspace(), '',
        minipage((
            gen_flip_flop_table(full_moves, T, 0),
            vspace(.3), '',
            gen_boolean_function(full_moves, T, 0),
        )),
    ))


def gen_tex_file_content(moves, f_f):
    """ Function generates content of tex file from given moves.

    :param moves: list of tuples (Z, from, to)
    :param f_f: type of flip-flop
    :return: string in Latex syntax
    """
    ff_map = {
        'jk': gen_jk_tables,
        'd': gen_d_tables,
        't': gen_t_tables
    }
    sorted_moves = sorted(moves)
    full_moves = complete_moves(moves)

    used_moves = sum([i[1:] for i in sorted_moves], ())
    print(f_f)
    print(set(used_moves))
    print(sorted(moves))

    return '\n'.join((
        file_header,
        '',
        subsection('Zakodowane wejsc, wyjsc i stanow wewnetrznych'),
        minipage((
            gen_input_table(),
        ), 3),
        minipage((
            gen_output_table(),
        ), 3),
        minipage((
            gen_states_table(used_moves),
        ), 3),
        vspace(), '',

        subsection('Zakodowane przejscia stanow'),
        gen_moves_table(sorted_moves),
        vspace(2), '',

        ff_map[f_f](sorted_moves, full_moves),
        vspace(2), '',

        file_footer
    ))
