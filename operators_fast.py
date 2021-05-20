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
    return int(all(l))


def XOR(l):
    return int(sum(l)%2)


def OR(l):
    return int(any(l))


def NOR(l):
    return int(not any(l))


def XNOR(l):
    return int((sum(l)+1)%2)


def NAND(l):
    return int(not all(l))


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
def impl_0000(x, y):
    return 0


def impl_0001(x, y):
    return int(not x and y)

def impl_0010(x, y):
    return int(x and y)


def impl_0011(x, y):
    return int(y)


def impl_0100(x, y):
    return int(x and not y)

def impl_0101(x, y):
    return int(x^y)


def impl_0110(x, y):
    return int(x)

def impl_0111(x, y):
    return int(x or y)

def impl_1000(x, y):
    return int(not(x or y))

def impl_1001(x, y):
    return int(not(x))

def impl_1010(x, y):
    return int(not(x^y))


def impl_1011(x, y):
    return int(y or not x)


def impl_1100(x, y):
    return int(not(y))

def impl_1101(x, y):
    return int(not(x and y))


def impl_1110(x, y):
    return int(x or not y)

def impl_1111(x, y):
    return 1

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

    x, y = 1, 1
    for i in range(16):
        print(impl[i], ": \t\t", impl[i](x, y))