file_header = r"""
\documentclass[11pt]{article}

\usepackage[margin=1in]{geometry}

\begin{document}
"""
file_footer = r'\end{document}'

hline = r'\hline'
end_tabular = r'\end{tabular}'


# TODO: write tests and docstring
def overline(text, isinside=False):
    result = r'\overline{{{}}}'.format(text)
    if isinside:
        return result
    return '$' + result + '$'


def gen_header():
    """ Function generates header for flip-flop table.

    :return: common table header
    """
    return 'Z' + subscript('Q', 2) + ' / ' + subscript('Q', 1) + subscript('Q', 0)


def split(lst, width=4):
    """ Generator yields lst in parts.

    :param lst: list of elements
    :param width: length of each part
    """
    for i in range(len(lst) // width):
        yield lst[width * i:width * (i + 1)]


def begin_tabular(width: int):
    """ Function returns opening tag for table.

    :param width: number of column in table
    :return: string which starts table
    """
    return r'\begin{tabular}{|' + 'c|' * width + '}'


def subscript(big, small, isinside=False):
    """ Function returns proper syntax for subscript.

    :param big: value which should be up and big
    :param small: value which should be down and small
    :return: string in Latex syntax
    """
    result = '{}_{{{}}}'.format(big, small)
    if isinside:
        return result
    return '$' + result + '$'


def multicolumn(width: int, value=''):
    """ Function merges n columns and fills it with value.

    :param width: number of merged columns
    :param value: text in merged columns
    :return: string
    """
    return r'\multicolumn{{{}}}{{|c|}}{{{}}}'.format(width, value)


def gen_row(row):
    """ Function transforms list of items to one row from Latex.

    :param row: list of items
    :return: string, merged row
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
    s = [begin_tabular(n)]

    for row in rows:
        s.append(gen_row(row))

    s.append(end_tabular)
    # sep = '\n'
    return '{0}{1}{0}'.format(sep, hline).join(s)
