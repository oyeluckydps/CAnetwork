
def binary(x, n):
    bin_x = bin(x).replace('0b', '')
    bin_x = '0' * (n - len(bin_x)) + bin_x
    return bin_x