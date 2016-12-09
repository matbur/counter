""" Module contains logic to create latex file.
"""

from minimization import D, J, JK, K, to_bin
from .binary_table import BinaryTable
from .boolean_function import BooleanFunction
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
    return Table(rows).to_latex()


def gen_output_table():
    """ Function generates table with output signals.

    :return: string in Latex syntax
    """
    rows = (
        ('', '$Y$'),
        (subscript('y', '0'), 0),
        (subscript('y', '1'), 1),
    )
    return Table(rows).to_latex()


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

    return Table(rows).to_latex()


def gen_moves_table(moves):
    """ Function generates table of moves with 2 or 3 column.

    :param moves: list of moves
    :return: string containing whole table
    """
    rows = (
        ['t', 't+1'],
        *moves
    )

    if len(moves[0]) == 3:
        rows[0].insert(0, '$Z$')

    return Table(rows).to_latex()


def gen_jk_tables(sorted_moves, full_moves, width, c_num):
    """ Function generates all tables with JK flip-flops.

    :param sorted_moves: list of sorted moves
    :param full_moves: complete list of moves
    :param width: width of max move
    :param c_num: number of columns in Karnough tables
    :return: string in Latex syntax
    """
    return '\n'.join((
        subsection('Tabela przejsc dla przerzutnikow JK'),
        BinaryTable(sorted_moves, width).to_latex(),
        FlipFlopTable(sorted_moves, width, JK).to_latex(),
        vspace(), '',
        subsection('Minimalizacja metoda Karnough dla przerzutnikow JK'),
        indent,
        *[minipage((
            KarnoughTable(full_moves, width, f_f, width - 1 - i, c_num).to_latex(),
            vspace(.3), '',
            BooleanFunction.from_moves(full_moves, width, f_f, width - 1 - i).get(),
            vspace(), '',
        )) for i in range(width) for f_f in (J, K)]
    ))


def gen_d_tables(sorted_moves, full_moves, width, c_num):
    """ Function generates all tables with D flip-flops.

    :param sorted_moves: list of sorted moves
    :param full_moves: complete list of moves
    :param width: width of max move
    :param c_num: number of columns in Karnough tables
    :return: string in Latex syntax
    """

    return '\n'.join((
        subsection('Tabela przejsc dla przerzutnikow D'),
        BinaryTable(sorted_moves, width).to_latex(),
        FlipFlopTable(sorted_moves, width, D).to_latex(),
        vspace(), '',
        subsection('Minimalizacja metoda Karnough dla przerzutnikow D'),
        indent,
        *[minipage((
            KarnoughTable(full_moves, width, D, width - 1 - i, c_num).to_latex(),
            vspace(.3), '',
            BooleanFunction.from_moves(full_moves, width, D, width - 1 - i).get(),
            vspace(), '',
        )) for i in range(width)]
    ))


def gen_tex_file_content(moves, f_f, c_num):
    """ Function generates content of tex file from given moves.

    :param moves: list of tuples (Z, from, to)
    :param f_f: type of flip-flop
    :param c_num: number of columns in Karnough tables
    :return: string in Latex syntax
    """
    ff_map = {
        'jk': gen_jk_tables,
        'd': gen_d_tables,
        # 't': gen_t_tables,
        # '': gen_none_tables
    }
    sorted_moves = sorted(moves)
    used_moves = sum([i[1:] for i in sorted_moves], ())
    width = len(to_bin(max(used_moves)))
    full_moves = complete_moves(moves, width)

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

        ff_map[f_f](sorted_moves, full_moves, width, c_num),
        vspace(2), '',
    )).generate_tex()


def complete_moves(moves, width):
    """ Function fills missing moves with '*'.

    :param moves: list of moves
    :param width: width of max move
    :return: completed, sorted list of moves
    """

    missing = set(range(1 << width)) - set(i[-2] for i in moves)
    num = len(moves[0])

    completed = {
        2: complete_moves2,
        3: complete_moves3,
    }[num](moves, missing, width)

    return sorted(completed)


def complete_moves2(moves, missing_moves, _=None):
    """ Function fills missing_moves moves with '*'.

    :param moves: list of moves
    :param missing_moves: set with missing moves
    :return: completed list of moves
    """
    completed = list(moves)
    for i in missing_moves:
        completed.append((i, '*'))

    return completed


def complete_moves3(moves, missing_moves, width):
    """ Function fills missing moves with '*'.

    :param moves: list of moves
    :param missing_moves: set with missing moves
    :param width: width of max move
    :return: completed list of moves
    """
    completed = list(moves)

    for i in missing_moves:
        completed.append((0, i, '*'))
        completed.append((1, i, '*'))

    d = {i[:2] for i in completed}
    a = {(i, j) for i in range(2) for j in range(1 << width)}
    for _, t, u in list(completed):
        for _, i in a - d:
            if t != i:
                continue
            completed.append((1, t, u))

    return completed
