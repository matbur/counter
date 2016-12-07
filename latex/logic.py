""" Module contains logic to create latex file.
"""
from minimization import D, J, JK, K, to_bin
from .boolean_function import BooleanFunction
from .common import flatten
from .document import Document, indent, minipage, subscript, subsection, vspace
from .flip_flop_table import FlipFlopTable
from .karnough_table import KarnoughTable
from .table import Table


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
    n = max(len(to_bin(i)) for i in moves)
    rows = (
        [subscript('Q', n - 1 - i) for i in range(n)],
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


def gen_bin_moves_header(width, arg=('t', 't+1')):
    return [Table.multicolumn(width, i) for i in arg]


def gen_bin_moves_signals(signals, width):
    return [subscript(j, width - 1 - i) for j in signals for i in range(width)]


def gen_bin_moves_content(moves, width):
    return [(*z, *to_bin(t, width), *to_bin(u, width)) for *z, t, u in moves]


def gen_bin_moves_table(moves, signals='QQ'):
    """ Function generates table of moves in binary system with 2 or 3 column.

    :param moves: list of moves
    :return: string containing whole table
    """
    n = len(moves[0])
    used_moves = sorted(set(sum(moves, ())))
    n2 = max(len(to_bin(i)) for i in used_moves)

    rows = [
        gen_bin_moves_header(n2),
        gen_bin_moves_signals(signals, n2),
        *gen_bin_moves_content(moves, n2)
    ]

    if n == 3:
        rows[0].insert(0, '')
        rows[1].insert(0, '$Z$')

    return Table(rows).gen_tabular()


def gen_jk_flip_flops_table(moves):
    """ Function generates table of JK flip-flops.

    :param moves: list of moves
    :return: string containing whole table
    """
    used_moves = sorted(set(sum(moves, ())))
    n = max(len(to_bin(i)) for i in used_moves)
    rows = [
        [Table.multicolumn(2 * n, 'Przerzutniki')],
        [subscript(i, n - 1 - j) for j in range(n) for i in 'JK']
    ]

    for *_, t, u in moves:
        it = zip(to_bin(t, n), to_bin(u, n))
        rows.append(flatten(JK(*next(it)) for _ in range(n)))

    return Table(rows).gen_tabular()


def gen_jk_tables(sorted_moves, full_moves, cnum):
    """ Function generates all tables with JK flip-flops.

    :param sorted_moves: list of sorted moves
    :param full_moves: complete list of moves
    :return: string in Latex syntax
    """
    used_moves = set(sum(sorted_moves, ()))
    n = max(len(to_bin(i)) for i in used_moves)

    return '\n'.join((
        subsection('Tabela przejsc dla przerzutkow JK'),
        gen_bin_moves_table(sorted_moves),
        FlipFlopTable(sorted_moves, JK).gen_tabular(),
        vspace(), '',
        subsection('Minimalizacja metoda Karnough dla przerzutnikow JK'),
        indent,
        *[minipage((
            KarnoughTable(full_moves, ff, n - 1 - i, cnum).gen_tabular(),
            vspace(.3), '',
            BooleanFunction.foo(full_moves, ff, n - 1 - i).get(),
            vspace(), '',
        )) for i in range(n) for ff in (J, K)]
    ))


def gen_d_tables(sorted_moves, full_moves, cnum):
    """ Function generates all tables with D flip-flops.

    :param sorted_moves: list of sorted moves
    :param full_moves: complete list of moves
    :return: string in Latex syntax
    """
    used_moves = set(sum(sorted_moves, ()))
    n = max(len(to_bin(i)) for i in used_moves)

    return '\n'.join((
        subsection('Tabela przejsc dla przerzutkow D'),
        gen_bin_moves_table(sorted_moves),
        FlipFlopTable(sorted_moves, D).gen_tabular(),
        vspace(), '',
        subsection('Minimalizacja metoda Karnough dla przerzutnikow D'),
        indent,
        *[minipage((
            KarnoughTable(full_moves, D, n - 1 - i, cnum).gen_tabular(),
            vspace(.3), '',
            BooleanFunction.foo(full_moves, D, n - 1 - i).get(),
            vspace(), '',
        )) for i in range(n)]
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
        # 't': gen_t_tables,
        # '': gen_none_tables
    }
    sorted_moves = sorted(moves)
    full_moves = complete_moves(moves)

    used_moves = sum([i[1:] for i in sorted_moves], ())

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

        ff_map[f_f](sorted_moves, full_moves, 2),
        vspace(2), '',
    )).generate_tex()


def complete_moves(moves):
    """ Function fills missing moves with '*'.

    :param moves: list of moves
    :return: completed, sorted list of moves
    """

    used_moves = set(sum(moves, ()))
    n = len(to_bin(max(used_moves)))

    missing = set(range(1 << n)) - set(i[-2] for i in moves)
    num = len(moves[0])
    # print(num)

    completed = {
        2: complete_moves2,
        3: complete_moves3,
    }[num](moves, missing)

    return sorted(completed)


def complete_moves2(moves, missing_moves):
    """ Function fills missing_moves moves with '*'.

    :param missing_moves:
    :param moves: list of moves
    :return: completed, sorted list of moves
    """
    completed = list(moves)
    for i in missing_moves:
        completed.append((i, '*'))

    return completed


def complete_moves3(moves, missing_moves):
    """ Function fills missing moves with '*'.

    :param missing_moves:
    :param moves: list of moves
    :return: completed, sorted list of moves
    """
    completed = list(moves)

    used_moves = set(sum(moves, ()))
    n = len(to_bin(max(used_moves)))

    for i in missing_moves:
        completed.append((0, i, '*'))
        completed.append((1, i, '*'))

    d = {i[:2] for i in completed}
    a = {(i, j) for i in range(2) for j in range(1 << n)}
    for _, t, u in list(completed):
        for _, i in a - d:
            if t != i:
                continue
            completed.append((1, t, u))

    return completed
