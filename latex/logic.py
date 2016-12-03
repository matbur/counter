""" Module contains logic to create latex file.
"""

from minimization import D, J, JK, K, Minimization, T, to_bin
from .common import gen_fields, gen_gray, split
from .document import Document
from .table import Table

indent, minipage, overline, subscript, subsection, vspace = Document.indent, Document.minipage, Document.overline, Document.subscript, Document.subsection, Document.vspace
gen_header = Document.gen_header


def gen_flip_flop_content(moves, f_f, num):
    """ Function generates interior table to minimize for flip-flop.

    :param moves: list of movements
    :param f_f: flip-flop function
    :param num: number of column
    :return: list with table
    """

    used_moves = set(sum(moves, ()))
    n = len(max(to_bin(i) for i in used_moves))

    content = list(gen_fields(2, 2))
    for i, (*_, t, u) in zip(content[:], moves):
        t_n = to_bin(t, n)[n - 1 - num]
        u_n = to_bin(u, n)[n - 1 - num]
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
    return Table(rows).gen_tabular()


def gen_output_table():
    """ Function generates table with output signals.

    :return: string in Latex syntax
    """
    rows = (
        ('', '$Y$'),
        (subscript('y', '0'), 0),
        (subscript('y', '1'), 1),
    )
    return Table(rows).gen_tabular()


def gen_states_table(moves):
    """ Function generates table with states.

    :param moves: list of used states
    :return: string in Latex syntax
    """
    moves = sorted(set(moves))
    n = len(max(to_bin(i) for i in moves))
    rows = (
        [subscript('Q', n - i) for i in range(n)],
        *[(subscript('q', i), *to_bin(i, n)) for i in moves]
    )
    rows[0].insert(0, '')

    return Table(rows).gen_tabular()


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

    return Table(rows).gen_tabular()


def gen_bin_moves_table(moves):
    """ Function generates table of moves in binary system with 2 or 3 column.

    :param moves: list of moves
    :return: string containing whole table
    """
    n = len(moves[0])
    used_moves = sorted(set(sum(moves, ())))
    n2 = len(max(to_bin(i) for i in used_moves))
    c = ('QQ', 'XY')[n2 == 4]
    rows = [
        sum([[subscript(c[j], n2 - i) for i in range(n2)] for j in range(2)], []),
        *[(*z, *to_bin(t, n2), *to_bin(u, n2)) for *z, t, u in moves]
    ]

    if n == 3:
        rows.insert(0, ['', Table.multicolumn(n2, 't'), Table.multicolumn(n2, 't+1')])
        rows[1].insert(0, '$Z$')

    return Table(rows).gen_tabular()


def gen_jk_flip_flops_table(moves):
    """ Function generates table of JK flip-flops.

    :param moves: list of moves
    :return: string containing whole table
    """
    rows = [
        [Table.multicolumn(6, 'Przerzutniki')],
        [subscript(i, j) for j in '210' for i in 'JK']
    ]

    for *_, t, u in moves:
        it = zip(to_bin(t, 3), to_bin(u, 3))
        rows.append(sum([JK(*next(it)) for _ in '210'], ()))

    return Table(rows).gen_tabular()


def gen_all_flip_flops_table(moves, f_f):
    """ Function generates table of flip-flops.

    :param moves: list of moves
    :param f_f: flip-flop function
    :return: string containing whole table
    """
    used_moves = sorted(set(sum(moves, ())))
    n = len(max(to_bin(i) for i in used_moves))
    rows = [
        [Table.multicolumn(n, 'Przerzutniki')],
        [subscript(i, n - j) for j in range(n) for i in f_f.name]
    ]

    for *_, t, u in moves:
        it = zip(to_bin(t, n), to_bin(u, n))
        rows.append([f_f(*next(it)) for _ in range(n)])

    return Table(rows).gen_tabular()


def gen_flip_flop_table(moves, f_f, num):
    """ Function generates table ready to minimize.

    :param moves: list of moves
    :param f_f: type of flip-flop
    :param num: number of column
    :return: string containing whole table
    """

    content = gen_flip_flop_content(moves, f_f, num)

    used_moves = set(sum(moves, ()))
    n = len(max(to_bin(i) for i in used_moves))

    it_gray = gen_gray()
    it_con = split(content)
    rows = [
        [Table.multicolumn(5, subscript(f_f.name, num))],
        (gen_header(), *gen_gray()),
        (next(it_gray), *next(it_con)),
        (next(it_gray), *next(it_con)),
    ]

    if len(moves[0]) == 3 or n == 4:
        rows.append((next(it_gray), *next(it_con)))
        rows.append((next(it_gray), *next(it_con)))

    return Table(rows).gen_tabular()


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
    # minterms, dontcares = get_minterms(data, fields)
    signals = ['Z', *(subscript('Q', i, True) for i in '210')]
    # minimized = minimize(minterms, dontcares, signals)
    fields = gen_fields(2, 2)
    minimized = Minimization.from_data(fields, data, signals).get()
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
        indent, '',
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
        indent, '',
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
        indent, '',
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


def gen_none_tables(sorted_moves, full_moves):
    """ Function generates all tables with no flip-flops.

    :param sorted_moves: list of sorted moves
    :param full_moves: complete list of moves
    :return: string in Latex syntax
    """
    return '\n'.join((
        subsection('Tabela przejsc'),
        gen_bin_moves_table(sorted_moves),
        # gen_all_flip_flops_table(sorted_moves, D),
        vspace(), '',
        subsection('Minimalizacja metoda Karnough'),
        minipage((
            gen_flip_flop_table(full_moves, D, 3),
            vspace(.3), '',
            gen_boolean_function(full_moves, D, 3),
        )),
        minipage((
            gen_flip_flop_table(full_moves, D, 2),
            vspace(.3), '',
            gen_boolean_function(full_moves, D, 2),
        )),
        vspace(), '',
        minipage((
            gen_flip_flop_table(full_moves, D, 1),
            vspace(.3), '',
            gen_boolean_function(full_moves, D, 1),
        )),
        minipage((
            gen_flip_flop_table(full_moves, D, 0),
            vspace(.3), '',
            gen_boolean_function(full_moves, D, 0),
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
        't': gen_t_tables,
        '': gen_none_tables
    }
    sorted_moves = sorted(moves)
    full_moves = complete_moves(moves)

    used_moves = sum([i[1:] for i in sorted_moves], ())
    print(f_f)
    print(set(used_moves))
    print(sorted(moves))

    return Document((
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
    )).generate_tex()


def complete_moves(moves):
    """ Function fills missing moves with '*'.

    :param moves: list of moves
    :return: completed, sorted list of moves
    """
    missing = set(range(8)) - set(i[-2] for i in moves)
    num = len(moves[0])

    completed = {
        2: complete_moves2,
        3: complete_moves3,
    }[num](moves, missing)

    return sorted(completed)


def complete_moves2(moves, missing_moves):
    """ Function fills missing_moves moves with '*'.

    :param moves: list of moves
    :return: completed, sorted list of moves
    """
    completed = list(moves)
    for i in missing_moves:
        completed.append((i, '*'))

    return completed


def complete_moves3(moves, missing_moves):
    """ Function fills missing moves with '*'.

    :param moves: list of moves
    :return: completed, sorted list of moves
    """
    completed = list(moves)

    for i in missing_moves:
        completed.append((0, i, '*'))
        completed.append((1, i, '*'))

    d = {i[:2] for i in completed}
    a = {(i, j) for i in range(2) for j in range(8)}
    for _, t, u in list(completed):
        for _, i in a - d:
            if t != i:
                continue
            completed.append((1, t, u))

    return completed
