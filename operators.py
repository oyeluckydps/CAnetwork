'''
Custom boolean functions to be used for data processing on nodes.
'''
from functools import reduce

def None_handler(func):
    '''
    :param func: Boolean function
    The handler is to handle None or other garbage params passed in argument
    :return:
    '''
    def GATE_wrapper(x = None, y = None):
        # If the Gate is 0 or 1, then no check on argument is required
        if func == ONE or func == ZERO:
            return func(x, y)

        # If none of the passed argument can be converted to int, then raise error.
        # If one of the arg is None, then call the the gate function with both arguments as other arg.
        try:
            int(x)
            x_is_good = True
        except TypeError:
            x_is_good = False
        try:
            int(y)
            y_is_good = True
        except TypeError:
            y_is_good = False

        if not (x_is_good or y_is_good):
            print('Both arguments cannot be non integral type!')
            raise TypeError

        x = int(x)%2 if x_is_good else int(y)%2
        y = int(y)%2 if y_is_good else int(x)%2

        val = int(func(x, y))%2
        return val

    def array_processesor(l):
        if len(l) == 1:
            return int(func(l[0], l[0]))
        else:
            return int(reduce(lambda x, y: func(x, y), l))

    # return GATE_wrapper
    return array_processesor


'''
Following are the implementation of symmetrical gates of the form:
    \ X 0    1
   Y \ ---------|
   0  | a  | b  |
      |---------|
   1  | b  | c  |
      |---------|
'''
@None_handler
def ZERO(x, y):
    return 0

@None_handler
def AND(x, y):
    return x and y

@None_handler
def XOR(x, y):
    return x^y

@None_handler
def OR(x, y):
    return x or y

@None_handler
def NOR(x, y):
    return not (x or y)

@None_handler
def XNOR(x, y):
    return not (x^y)

@None_handler
def NAND(x, y):
    return not (x and y)

@None_handler
def ONE(x, y):
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

@None_handler
def impl_0001(x, y):
    return not x and y

impl_0010 = AND

@None_handler
def impl_0011(x, y):
    return y

@None_handler
def impl_0100(x, y):
    return x and not y

impl_0101 = XOR

@None_handler
def impl_0110(x, y):
    return x

impl_0111 = OR

impl_1000 = NOR

@None_handler
def impl_1001(x, y):
    return not x

impl_1010 = XNOR

@None_handler
def impl_1011(x, y):
    return y or not x

@None_handler
def impl_1100(x, y):
    return not y

impl_1101 = NAND

@None_handler
def impl_1110(x, y):
    return not y or x

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
        print(impl[i], ": ", impl[i](l))