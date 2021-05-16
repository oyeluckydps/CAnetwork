
def binary(x, n):
    bin_x = bin(x).replace('0b', '')
    bin_x = '0' * (n - len(bin_x)) + bin_x
    return bin_x

def df_to_bianryFile(df):
    all_bytes = []
    for _, row in df.iterrows():
        row_list = list(row)
        byte_list = [[32] if i else [226, 150, 136] for i in row_list]
        flatten_list = [byte for sublist in byte_list for byte in sublist]
        flatten_list.append(10)
        all_bytes.extend(flatten_list)
    return all_bytes

def write_bytes_to_file(filename, byte_seq):
    f = open(filename, 'a+b')
    binary_format = bytearray(byte_seq)
    f.write(binary_format)
    f.close()