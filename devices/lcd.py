class Lcd:
    def __init__(self, robotservice):
        self.robotservice = robotservice
        self.ioservice = robotservice.ioservice
    
    def clear(self):
        self.ioservice.command_lcd_clear()

    def set_display_enabled(self, enabled):
        self.ioservice.command_lcd_set_state(enabled)

    def set_backlight(self, value):
        pass

    def set_pos(self, line, column):
        self.ioservice.command_lcd_set_position(line, column)

    def write(self, chars):
        self.ioservice.command_lcd_write(chars)
