from .common import flatten, gen_fields, gen_gray, split, to_bin
from .document import gen_header, subscript
from .table import Table


class KarnoughTable(Table):
    def __init__(self, moves, f_f, num, cnum):
        self._rows = None
        self.__moves = moves
        self.__f_f = f_f
        self.__num = num
        self.__cnum = cnum
        self.__width = None
        self.__is_z = len(moves[0]) == 3
        self.__content = None

        self.__calc_width()
        self.__gen_karnough_content()
        self.__gen_karnough_table()

    def __calc_width(self):
        moves = self.__moves
        used_moves = set(flatten(moves)) - {'*'}
        self.__width = len(to_bin(max(used_moves))) + int(self.__is_z)

    def __gen_karnough_content(self):
        """ Function generates interior table to minimize for flip-flop.
        """
        moves = self.__moves
        f_f = self.__f_f
        n = self.__width
        num = self.__num
        cnum = self.__cnum
        rnum = n - cnum

        content = list(gen_fields(rnum, cnum))
        # print(['{:>2}'.format(i) for i in content])

        for i in content[:]:
            (*_, t, u) = moves[content[i]]
            t_n = to_bin(t, n)[n - 1 - num]
            u_n = to_bin(u, n)[n - 1 - num]
            content[i] = f_f(t_n, u_n)
        # print(['{:>2}'.format(i) for i in content])
        self.__content = content

    def __gen_karnough_table(self):
        """ Function generates table ready to minimize.
        """
        gen_karnough_header = self.__gen_karnough_header
        is_z = self.__is_z
        cnum = self.__cnum
        num = self.__num
        n = self.__width
        rnum = n - cnum

        content = self.__content
        # it_gray = gen_gray(rnum, False)
        it_gray = gen_gray(rnum)
        it_con = split(content, 1 << cnum)
        # rows = [
        #     gen_karnough_header(num, cnum),
        #     (gen_header(rnum, cnum, is_z), *gen_gray(cnum, False)),
        #     *([next(it_gray) * (1 << cnum), *next(it_con)] for _ in range(1 << rnum))
        # ]
        rows = [
            gen_karnough_header(num, cnum),
            (gen_header(rnum, cnum, is_z), *gen_gray(cnum)),
            *([next(it_gray), *next(it_con)] for _ in range(1 << rnum))
        ]

        self._rows = rows

    def __gen_karnough_header(self, num, cnum):
        f_f = self.__f_f
        return [Table.multicolumn((1 << cnum) + 1, subscript(f_f.name, num))]
