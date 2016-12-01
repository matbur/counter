""" Module contains functions to minimize boolean function
    with Quine-McCluskey algorithm and Petrick's method.
"""

from .minimization import *
from .common import *
from .flip_flops import *
from .quine_mccluskey import *
from .petricks import *




# def minimize(minterms, dontcares, signals):
#     """ Function generates boolean function.
#
#     :param minterms: list of __flattened for which output function will be 1
#     :param dontcares: list of __flattened for which we don't care about the output
#     :param signals: names of signals
#     :return: boolean function
#     """
#     if not minterms:
#         return '0'
#     if len(minterms) + len(dontcares) == 16:
#         return '1'
#
#     united_minterms = [to_bin(i, 4) for i in minterms + dontcares]
#     unused_implicants = quine_mccluskey(united_minterms)
#     minimized = Petricks_method(unused_implicants, minterms)
#     return get_function(minimized, signals)
