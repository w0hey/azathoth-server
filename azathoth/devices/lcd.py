class Lcd:
    def __init__(self, ioservice):
        self.ioservice = ioservice
    
    def clear(self):
        data = '\x03\x00'
        self.ioservice.protocol.send(data)

    def set_display_enabled(self, enabled):
        if enabled:
            data = '\x03\x01\x01'
        else:
            data = '\x03\x01\x00'
        self.ioservice.protocol.send(data)

    def set_backlight(self, value):
        pass

    def set_pos(self, line, column):
        data = '\x03\x03' + chr(line) + chr(column)
        self.ioservice.protocol.send(data)

    def write(self, chars):
        data = '\x03\x04' + chars
        self.ioservice.protocol.send(data)
