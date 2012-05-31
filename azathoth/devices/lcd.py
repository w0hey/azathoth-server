class Lcd:
    def __init__(self, ioservice):
        self.ioservice = ioservice
    
    def clear(self):
        self.ioservice.protocol.lcd_cmd_clear()

    def setEnabled(self, enabled):
        self.ioservice.protocol.lcd_cmd_set_enabled(enabled)

    def setBacklight(self, value):
        self.ioservice.protocol.lcd_cmd_set_backlight(value)

    def setPos(self, line, column):
        self.ioservice.protocol.lcd_cmd_set_position(line, column)

    def writeChars(self, chars):
        self.ioservice.protocol.lcd_cmd_write(chars)
