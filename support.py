
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

def logger_to_file(filename, logged_str):
    '''
    :param logged_str: List of str that is formed of 0's and 1;s
    :return:
    '''
    f = open(filename, 'a+b')
    for str in logged_str:
        all_bytes = []
        for char in str:
            if char == '0':
                all_bytes.append(226)
                all_bytes.append(150)
                all_bytes.append(136)
            else:
                all_bytes.append(32)
        all_bytes.append(10)
        binary_format = bytearray(all_bytes)
        f.write(binary_format)
    f.close()
    return

def logger_to_file_impl2(filename, logged_str):
    '''
    :param logged_str: List of str that is formed of 0's and 1;s
    :return:
    '''
    f = open(filename, 'a+b')
    for str in logged_str:
        for char in str:
            if char == '0':
                f.write(b'\xe2\x96\x88')
            else:
                f.write(b' ')
        f.write(b'\n')
    f.close()
    return

def write_bytes_to_file(filename, byte_seq):
    f = open(filename, 'a+b')
    binary_format = bytearray(byte_seq)
    f.write(binary_format)
    f.close()

def dict_str(d):
    d_str = "{\n"
    for k, v in d.items():
        d_str += k.__str__() + " : " + v.__str__() +",\n"
    d_str = d_str[:-2]
    d_str += "\n}\n"
    return d_str