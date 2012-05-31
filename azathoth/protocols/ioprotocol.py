from twisted.python import log

from azathoth.protocols.controllerprotocol import ControllerProtocol

class IoProtocol(ControllerProtocol):
    def __init__(self, service):
        ControllerProtocol.__init__(self, service)

    def lcd_cmd_clear(self):
        """
        Clear the LCD screen
        """
        data = '\x03\x00'
        self.send(data)

    def lcd_cmd_set_enabled(self, enabled):
        """
        Enable/disable the lcd display
        Does not affect the backlight
        """
        if enabled:
            data = '\x03\x01\x01'
        else:
            data = '\x03\x01\x00'
        self.send(data)

    def lcd_cmd_set_backlight(self, value):
        """
        Set the LCD backlight brightness
        Value: See serial LCD datasheet
        """
        # TODO: Interpret the value in some usable way
        data = '\x03\x02' + chr(value)
        self.send(data)

    def lcd_cmd_set_position(self, line, column):
        """
        Move the LCD cursor to a new position
        line: 0-1
        column: 0-15
        """
        data = '\x03\x03' + chr(line) + chr(column)
        self.send(data)

    def lcd_cmd_write(self, chars):
        """
        Write the provided characters to the LCD
        """
        data = '\x03\x04' + chars
        self.send(data)
