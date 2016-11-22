""" Package to generate latex and pdf files.
"""

from .logic import *
from .parts import *


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
