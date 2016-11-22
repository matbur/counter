""" Module contains latex parts which are used to create latex file.
"""

file_header = r"""
\documentclass[11pt]{article}

\usepackage[margin=1in]{geometry}

\begin{document}
"""
file_footer = r'\end{document}'

hline = r'\hline'
qquad = r'$\qquad$'
end_tabular = r'\end{tabular}'


def overline(text, isinside=False):
    """ Function generates syntax for overline.

    :param text: value which should be overlined
    :param isinside: if set don't add dollars signs
    :return: string in Latex syntax
    """
    result = r'\overline{{{}}}'.format(text)
    return ('${}$', '{}')[isinside].format(result)


def subscript(big, small, isinside=False):
    """ Function generatex syntax for subscript.

    :param big: value which should be up and big
    :param small: value which should be down and small
    :return: string in Latex syntax
    """
    result = '{}_{{{}}}'.format(big, small)
    return ('${}$', '{}')[isinside].format(result)


def gen_header():
    """ Function generates header for flip-flop table.

    :return: string in Latex syntax
    """
    return 'Z{} / {}{}'.format(subscript('Q', 2), subscript('Q', 1), subscript('Q', 0))


def begin_tabular(width: int):
    """ Function generates opening tag for table.

    :param width: number of column in table
    :return: string in Latex syntax
    """
    return r'\begin{tabular}{|' + 'c|' * width + '}'


def multicolumn(width: int, value=''):
    """ Function merges n columns and fills it with value.

    :param width: number of merged columns
    :param value: text in merged columns
    :return: string in Latex syntax
    """
    return r'\multicolumn{{{}}}{{|c|}}{{{}}}'.format(width, value)


def vspace(width=1.):
    """ Function generates syntax for vertical space.

    :param width: numerical value of space
    :return: string in Latex syntax
    """
    return r'\vspace{{{:.1f}em}}'.format(width)


def minipage(content=(), num=2):
    """ Function generates syntax for minipage.

    :param content: text inside minipage
    :param num: number of minipages
    :return: string in Latex syntax
    """
    return '\n'.join((
        r'\begin{{minipage}}[ht]{{{:.2f}\textwidth}}'.format(1. / num),
        *content,
        r'\end{minipage}'
    ))


def subsection(text=''):
    """ Function generates syntax for subsection.

    :param text: content of subsection
    :return: string in Latex syntax
    """
    return r'\subsection{{{}}}'.format(text)
