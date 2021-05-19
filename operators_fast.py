'''
Custom boolean functions to be used for data processing on nodes.
'''
from functools import reduce

'''
Following are the implementation of symmetrical gates of the form:
    \ X 0    1
   Y \ ---------|
   0  | a  | b  |
      |---------|
   1  | b  | c  |
      |---------|
'''

def ZERO(l):
    return 0


def AND(l):
    return int(reduce(lambda x, y: x and y, l))


def XOR(l):
    return int(reduce(lambda x, y: x^y, l))


def OR(l):
    return int(reduce(lambda x, y: x or y, l))


def NOR(l):
    return int(not(reduce(lambda x, y: x or y, l)))


def XNOR(l):
    return int(not(reduce(lambda x, y: x^y, l)))


def NAND(l):
    return int(not(reduce(lambda x, y: x and y, l)))


def ONE(l):
    return 1

half_symm_impl = {
    'ZERO': ZERO,
    'AND': AND,
    'XOR': XOR,
    'OR': OR
}

symm_impl = {
    'ZERO': ZERO,
    'AND': AND,
    'XOR': XOR,
    'OR': OR,
    'NOR': NOR,
    'XNOR': XNOR,
    'NAND': NAND,
    'ONE': ONE
}

'''
Following are the implementation of symmetrical gates of the form:
    \ X 0    1
   Y \ ---------|
   0  | a  | b  |
      |---------|
   1  | d  | c  |
      |---------|
Eight of the symmetrical forms from above can be reused and only other eight require implementation.
'''
impl_0000 = ZERO


def impl_0001(l):
    return int(reduce(lambda x, y: not x and y, l))

impl_0010 = AND


def impl_0011(l):
    return int(l[-1])


def impl_0100(l):
    return int(reduce(lambda x, y: x and not y, l))

impl_0101 = XOR


def impl_0110(l):
    return int(l[0])

impl_0111 = OR

impl_1000 = NOR


def impl_1001(l):
    return int(not(l[0]))

impl_1010 = XNOR


def impl_1011(l):
    return int(reduce(lambda x, y: y or not x, l))


def impl_1100(l):
    return int(not l[-1])

impl_1101 = NAND


def impl_1110(l):
    return int(reduce(lambda x, y: x or not y, l))

impl_1111 = ONE

impl = {
    0: impl_0000,
    1: impl_0001,
    2: impl_0010,
    3: impl_0011,
    4: impl_0100,
    5: impl_0101,
    6: impl_0110,
    7: impl_0111,
    8: impl_1000,
    9: impl_1001,
    10: impl_1010,
    11: impl_1011,
    12: impl_1100,
    13: impl_1101,
    14: impl_1110,
    15: impl_1111
}

if __name__ == '__main__':

    l = [1, 0]
    for i in range(16):
        print(impl[i], ": \t\t", impl[i](l))