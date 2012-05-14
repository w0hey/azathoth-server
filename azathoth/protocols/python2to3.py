def byteToInt(byte):
    if hasattr(byte, 'bit_length'):
        return byte
    return ord(byte) if hasattr(byte, 'encode') else byte[0]

def intToByte(i):
    return chr(i) if hasattr(bytes(), 'encode') else bytes([i])

def stringToBytes(s):
    return s.encode('ascii')
