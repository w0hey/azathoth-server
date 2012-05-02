import struct
from protocols.python2to3 import byteToInt, intToByte


class LinkFrame:
    """
    Represents a frame of data to be sent, or which was received
    via Azathoth's Link protocol.
    Code in this class is modified from python-xbee by Paul Malmsten.
    """

    START_BYTE = b'\x7e'
    ESCAPE_BYTE = b'\x7d'
    XON_BYTE = b'\x11'
    XOFF_BYTE = b'\x13'
    ESCAPE_BYTES = (START_BYTE, ESCAPE_BYTE, XON_BYTE, XOFF_BYTE)
    
    def __init__(self, data=b''):
        self.data = data
        self.raw_data = b''
        self._unescape_next_byte = False

    def len_bytes(self):
        """
        Originally this function returned the two-byte length
        of the frame's data as a packed struct.
        Now, it only needs to return one byte as we use only one byte
        for our length field.
        """
        #TODO: this is probably spurious code, if we're only returning
        # one byte.
        count = len(self.data)
        return struct.pack("> B", count)
    
    def output(self):
        """
        output: None -> valid Link frame (binary data)

        output will produce a valid Link frame for transmission
        on the wire.
        """
        data = self.len_bytes() + self.data

        if len(self.raw_data) < 1:
            self.raw_data = LinkFrame.escape(data)

        data = self.raw_data

        return LinkFrame.START_BYTE + data

    @staticmethod
    def escape(data):
        """
        escape: byte string -> byte string

        When the 'special' byte is found in the data string,
        it must be preceded by an escape byte and XOR'd with 0x20
        """

        escaped_data = b""
        for byte in data:
            if intToByte(byteToInt(byte)) in LinkFrame.ESCAPE_BYTES:
                escaped_data += LinkFrame.ESCAPE_BYTE
                escaped_data += intToByte(0x20 ^ byteToInt(byte))
            else:
                escaped_data += intToByte(byteToInt(byte))

        return escaped_data

    def fill(self, byte):
        """
        fill: byte -> None

        Adds the given byte to this LinkFrame. If this byte is an escape
        byte, the next byte in a call to fill() will be unescaped.
        """
        if self._unescape_next_byte:
            byte = intToByte(byteToInt(byte) ^ 0x20)
            self._unescape_next_byte = False
        elif byte == LinkFrame.ESCAPE_BYTE:
            self._unescape_next_byte = True
            return

        self.raw_data += intToByte(byteToInt(byte))
    
    def remaining_bytes(self):
        remaining = 2

        if len(self.raw_data) >= 2:
            raw_len = self.raw_data[1:2]
            data_len = struct.unpack("> B", raw_len)[0]

            remaining += data_len

        return remaining - len(self.raw_data)

    def parse(self):
        """
        parse: None -> None

        Given a valid Link frame, parse extracts the data contained
        inside it.
        """
        if len(self.raw_data) < 2:
            ValueError("parse() may only be called on a frame containing at least 2 bytes of raw data")
        
        # First byte is the length of the data
        raw_len = self.raw_data[1:2]

        # Unpack it
        data_len = struct.unpack("> B", raw_len)[0]
        
        # Read the data
        data = self.raw_data[2:2 + data_len]
        self.data = data

