""" Module contains class which represents Karnough table.
"""

from .common import gen_fields, gen_gray, split, to_bin
from .document import gen_header, subscript
from .table import Table, multicolumn


class KarnoughTable(Table):
    def __init__(self, moves, width, f_f, num, c_num):
        super().__init__([], moves, width)
        self.__is_z = len(moves[0]) == 3
        self._width += self.__is_z
        self.__f_f = f_f
        self.__num = num
        self.__c_num = c_num

        self.__fill_header()
        self.__fill_content()
        self.__fill_rows()

    def __fill_header(self):
        """ Method fills header in table.
        """
        f_f = self.__f_f
        num = self.__num
        c_num = self.__c_num

        self._header = [multicolumn((1 << c_num) + 1, subscript(f_f.name, num))]

    def __fill_content(self):
        """ Method fills content of table.
        """
        moves = self._moves
        f_f = self.__f_f
        width = self._width
        num = self.__num
        c_num = self.__c_num

        r_num = width - c_num
        content = list(gen_fields(r_num, c_num))

        for i in content[:]:
            (*_, t, u) = moves[content[i]]
            t_n = to_bin(t, width)[width - 1 - num]
            u_n = to_bin(u, width)[width - 1 - num]
            content[i] = f_f(t_n, u_n)

        self._content = content

    def __fill_rows(self):
        """ Method fills rows in table.
        """
        header = self._header
        is_z = self.__is_z
        c_num = self.__c_num
        n = self._width
        content = self._content

        r_num = n - c_num
        it_gray = gen_gray(r_num)
        it_con = split(content, 1 << c_num)

        rows = [
            header,
            (gen_header(r_num, c_num, is_z), *gen_gray(c_num)),
            *([next(it_gray), *next(it_con)] for _ in range(1 << r_num))
        ]

        self._rows = rows
