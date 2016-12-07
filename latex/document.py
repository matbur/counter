""" Module contains latex parts which are used to create latex file.
"""


class Document:
    __begin = '\n'.join((r'\documentclass[11pt]{article}',
                         r'\usepackage[margin=1in]{geometry}',
                         r'\begin{document}'
                         ))
    __footer = r'\end{document}'
    qquad = r'$\qquad$'
    indent = r'\indent'

    def __init__(self, items):
        self.__items = items

    def generate_tex(self, sep='\n'):
        return sep.join((self.__begin, *self.__items, self.__footer))

    @staticmethod
    def overline(text, isinside=False):
        """ Function generates syntax for overline.

        :param text: value which should be overlined
        :param isinside: if set don't add dollars signs
        :return: string in Latex syntax
        """
        result = r'\overline{{{}}}'.format(text)
        return ('${}$', '{}')[isinside].format(result)

    @staticmethod
    def vspace(width=1.):
        """ Function generates syntax for vertical space.

        :param width: numerical value of space
        :return: string in Latex syntax
        """
        return r'\vspace{{{:.1f}em}}'.format(width)

    @staticmethod
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

    @staticmethod
    def subsection(text=''):
        """ Function generates syntax for subsection.

        :param text: content of subsection
        :return: string in Latex syntax
        """
        return r'\subsection{{{}}}'.format(text)


def gen_header(rnum, cnum, is_z=False):
    """ Function generates header for flip-flop table.

    :return: string in Latex syntax
    """
    n = rnum + cnum - is_z

    s = '{} / {}'.format('{}' * rnum, '{}' * cnum)
    n_ = [subscript('Q', n - 1 - i) for i in range(n)]
    if is_z:
        n_.insert(0, 'Z')
    return s.format(*n_)


def subscript(big, small, isinside=False):
    """ Function generatex syntax for subscript.

    :param big: value which should be up and big
    :param small: value which should be down and small
    :return: string in Latex syntax
    """
    result = '{}_{{{}}}'.format(big, small)
    return ('${}$', '{}')[isinside].format(result)


if __name__ == '__main__':
    d = Document(['1', '2', '3'])
    print(d.generate_tex())
