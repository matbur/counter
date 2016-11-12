""" Package to generate latex and pdf files.
"""

from minimization import J, K, complete_moves
from .logic import *
from .parts import *


def create_tex_file_content(moves):
    """ Function generates content of tex file from given moves.

    :param moves: list of tuples (Z, from, to)
    """
    full_moves = complete_moves(moves)

    to_write = (
        file_header,
        '',
        gen_moves_table(moves),
        gen_bin_moves_table(moves),
        gen_all_flip_flops_table(moves),
        '',
        gen_flip_flop_table(full_moves, J, 2),
        gen_flip_flop_table(full_moves, K, 2),
        '',
        gen_boolean_function(full_moves, J, 2),
        '',
        gen_boolean_function(full_moves, K, 2),
        '',
        gen_flip_flop_table(full_moves, J, 1),
        gen_flip_flop_table(full_moves, K, 1),
        '',
        gen_boolean_function(full_moves, J, 1),
        '',
        gen_boolean_function(full_moves, K, 1),
        '',
        gen_flip_flop_table(full_moves, J, 0),
        gen_flip_flop_table(full_moves, K, 0),
        '',
        gen_boolean_function(full_moves, J, 0),
        '',
        gen_boolean_function(full_moves, K, 0),
        '',
        file_footer
    )

    return '\n'.join(to_write)


def create_tex_file(moves, file='file.tex'):
    """ Function creates tex file from given moves.

    :param file: name of the tex file
    :param moves: list of tuples (Z, from, to)
    """

    to_write = create_tex_file_content(moves)

    with open(file, 'w') as f:
        f.write(to_write)


def create_pdf_file(file='file.tex'):
    """ Function creates pdf file from given tex file.

    :param file: tex file to compile
    """
    import subprocess

    command = 'pdflatex -output-directory $(dirname {0}) {0} 1>/dev/null'.format(file)
    subprocess.call(command, shell=True)
