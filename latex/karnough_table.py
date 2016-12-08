"""
"""

from .common import flatten, gen_fields, gen_gray, split, to_bin
from .document import gen_header, subscript
from .table import Table, multicolumn


class KarnoughTable(Table):
    def __init__(self, moves, f_f, num, c_num):
        self._rows = None
        self.__moves = moves
        self.__f_f = f_f
        self.__num = num
        self.__c_num = c_num
        self.__width = None
        self.__is_z = len(moves[0]) == 3
        self.__content = None

        self.__calc_width()
        self.__gen_karnough_content()
        self.__gen_karnough_table()

    def __calc_width(self):
        moves = self.__moves
        is_z = self.__is_z
        used_moves = set(flatten(moves)) - {'*'}
        self.__width = len(to_bin(max(used_moves))) + int(is_z)

    def __gen_karnough_content(self):
        """ Function generates interior table to minimize for flip-flop.
        """
        moves = self.__moves
        f_f = self.__f_f
        n = self.__width
        num = self.__num
        c_num = self.__c_num
        r_num = n - c_num

        content = list(gen_fields(r_num, c_num))

        for i in content[:]:
            (*_, t, u) = moves[content[i]]
            t_n = to_bin(t, n)[n - 1 - num]
            u_n = to_bin(u, n)[n - 1 - num]
            content[i] = f_f(t_n, u_n)

        self.__content = content

    def __gen_karnough_table(self):
        """ Function generates table ready to minimize.
        """
        gen_karnough_header = self.__gen_karnough_header
        is_z = self.__is_z
        c_num = self.__c_num
        num = self.__num
        n = self.__width
        content = self.__content
        r_num = n - c_num

        it_gray = gen_gray(r_num)
        it_con = split(content, 1 << c_num)

        rows = [
            gen_karnough_header(num, c_num),
            (gen_header(r_num, c_num, is_z), *gen_gray(c_num)),
            *([next(it_gray), *next(it_con)] for _ in range(1 << r_num))
        ]

        self._rows = rows

    def __gen_karnough_header(self, num, c_num):
        f_f = self.__f_f
        return [multicolumn((1 << c_num) + 1, subscript(f_f.name, num))]
