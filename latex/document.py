""" Module contains latex parts which are used to create Latex file.
"""


class Document:
    __begin = '\n'.join((r'\documentclass[11pt]{article}',
                         r'\usepackage[margin=1in]{geometry}',
                         r'\begin{document}'
                         ))
    __footer = r'\end{document}'

    def __init__(self, items):
        self.__items = items

    def generate_tex(self, sep='\n'):
        """ Method generates whole Latex document.

        :param sep: separator between items
        :return: string in Latex syntax
        """
        begin = self.__begin
        items = self.__items
        footer = self.__footer

        return sep.join((begin, *items, footer))


indent = r'\indent'
qquad = r'$\qquad$'


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


def vspace(width=1.):
    """ Function generates syntax for vertical space.

    :param width: numerical value of space
    :return: string in Latex syntax
    """
    return r'\vspace{{{:.1f}em}}'.format(width)


def subsection(text=''):
    """ Function generates syntax for subsection.

    :param text: content of subsection
    :return: string in Latex syntax
    """
    return r'\subsection{{{}}}'.format(text)


def overline(text, is_inside=False):
    """ Function generates syntax for overline.

    :param text: value which should be overlined
    :param is_inside: if set don't add dollars signs
    :return: string in Latex syntax
    """
    result = r'\overline{{{}}}'.format(text)
    return ('${}$', '{}')[is_inside].format(result)


def gen_header(r_num: int, c_num: int, is_z=False):
    """ Function generates header for flip-flop table.

    :param r_num: number of rows
    :param c_num: number of columns
    :param is_z: bool, if True add Z signal
    :return: string in Latex syntax
    """
    n = r_num + c_num - is_z

    s = '{} / {}'.format('{}' * r_num, '{}' * c_num)
    header = [subscript('Q', n - 1 - i) for i in range(n)]
    if is_z:
        header.insert(0, 'Z')
    return s.format(*header)


def subscript(big, small, is_inside=False):
    """ Function generates syntax for subscript.

    :param big: value which should be up and big
    :param small: value which should be down and small
    :param is_inside: bool, if True add $ at begin and end
    :return: string in Latex syntax
    """
    result = '{}_{{{}}}'.format(big, small)
    return ('${}$', '{}')[is_inside].format(result)
