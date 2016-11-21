""" Module contains latex parts which are used to create latex file.
"""

file_header = r"""
\documentclass[11pt]{article}

\usepackage[margin=1in]{geometry}

\begin{document}
"""
file_footer = r'\end{document}'

hline = r'\hline'
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
    """ Function returns proper syntax for subscript.

    :param big: value which should be up and big
    :param small: value which should be down and small
    :return: string in Latex syntax
    """
    result = '{}_{{{}}}'.format(big, small)
    return ('${}$', '{}')[isinside].format(result)


def gen_header():
    """ Function generates header for flip-flop table.

    :return: common table header
    """
    return 'Z{} / {}{}'.format(subscript('Q', 2), subscript('Q', 1), subscript('Q', 0))


def begin_tabular(width: int):
    """ Function returns opening tag for table.

    :param width: number of column in table
    :return: string which starts table
    """
    return r'\begin{tabular}{|' + 'c|' * width + '}'


def multicolumn(width: int, value=''):
    """ Function merges n columns and fills it with value.

    :param width: number of merged columns
    :param value: text in merged columns
    :return: string
    """
    return r'\multicolumn{{{}}}{{|c|}}{{{}}}'.format(width, value)


def vspace(value=1.):
    """

    :param value:
    """
    return r'\vspace{{{:.1f}em}}'.format(value)


def minipage(content=()):
    """

    :param content:
    """
    return '\n'.join((
        r'\begin{minipage}[ht]{.5\textwidth}',
        *content,
        r'\end{minipage}'
    ))
