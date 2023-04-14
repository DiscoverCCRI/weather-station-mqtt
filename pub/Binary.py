import sys

def twos(val_str):
    bytes = int(len(val_str) / 8)
    val = int(val_str, 2)
    b = val.to_bytes(bytes, byteorder=sys.byteorder, signed=False)
    return int.from_bytes(b, byteorder=sys.byteorder, signed=True)


def fill(databin, lenhex):
    if len(databin) < 4 * lenhex:
        str_list = list(databin)
        n = 4 * lenhex - len(databin)
        for x in range(1, n):
            str_list.insert(0, "0")
        data = "".join(str_list)
    return data


def tobin(datahex):
    databin = bin(int(datahex, 16))[2:-1]
    return fill(databin, len(datahex))
