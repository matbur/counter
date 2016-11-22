""" Package to generate latex and pdf files.
"""

from minimization import D, J, K, T, complete_moves
from .logic import *
from .parts import *


def create_tex_file_content(moves, f_f):
    """ Function generates content of tex file from given moves.

    :param moves: list of tuples (Z, from, to)
    :param f_f: type of flip-flop
    """
    print(f_f)
    ff_map = {
        'jk': jk,
        'd': d,
        't': t
    }
    sorted_moves = sorted(moves)
    full_moves = complete_moves(moves)

    used_moves = [i[1] for i in sorted_moves]
    print(used_moves)

    to_write = (
        file_header,
        '',
        subsection('Zakodowane wejsc, wyjsc i stanow'),
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
    )

    return '\n'.join(to_write)


def jk(sorted_moves, full_moves):
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


def d(sorted_moves, full_moves):
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


def t(sorted_moves, full_moves):
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


def create_tex_file(moves, ff_type, file='file.tex'):
    """ Function creates tex file from given moves.

    :param file: name of the tex file
    :param ff_type: type of flip-flop
    :param moves: list of tuples (Z, from, to)
    """

    to_write = create_tex_file_content(moves, ff_type)

    with open(file, 'w') as f:
        f.write(to_write)


def create_pdf_file(file='file.tex'):
    """ Function creates pdf file from given tex file.

    :param file: tex file to compile
    """
    import subprocess

    command = 'pdflatex -output-directory $(dirname {0}) {0} 1>/dev/null'.format(file)
    subprocess.call(command, shell=True)
