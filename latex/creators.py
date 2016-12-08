""" Module contains function which creates files: tex, pdf and jpg.
"""

import subprocess

from .logic import gen_tex_file_content


def create_tex_file(moves, ff_type, c_num, file='file.tex'):
    """ Function creates tex file from given moves.

    :param moves: list of tuples (Z, from, to)
    :param ff_type: type of flip-flop
    :param c_num: number of columns
    :param file: name of the tex file
    :return: error or None
    """

    to_write = gen_tex_file_content(moves, ff_type, c_num)

    try:
        with open(file, 'w') as f:
            f.write(to_write)
    except FileNotFoundError as err:
        return err


def create_pdf_file(file='file.tex'):
    """ Function creates pdf file from given tex file.

    :param file: tex file to compile
    :return: error or None
    """
    # directory = os.path.dirname(file)
    # command = 'pdflatex -halt-on-error -output-directory {} {} 1>/dev/null'.format(directory, file)
    command = 'pdflatex -halt-on-error -output-directory $(dirname {0}) {0} 1>/dev/null'.format(file)
    return subprocess.call(command, shell=True)


def create_jpg_file(file='file'):
    """ Function creates jpg file from given pdf file.

    :param file: jpg file to convert
    :return: error code or None
    """
    command = 'convert -density 150 {0}.pdf -append {0}.jpg'.format(file)
    return subprocess.call(command, shell=True)
