from twisted.application import service
from twisted.internet import reactor
from twisted.internet.serialport import SerialPort
from twisted.python import log

from protocols.ioprotocol import IoProtocol

class IoService(service.Service):
    name = "ioservice"
    def __init__(self, robotservice, port, speed=115200):
        self.robot = robotservice
        self.port = port
        self.speed = speed
    
    def startService(self):
        log.msg("ioservice starting")
        self.protocol = IoProtocol(self)
        log.msg(format="ioservice opening serial port %(port)s", port=self.port)
        self.serial = SerialPort(self.protocol, self.port, reactor, baudrate=self.speed)
        service.Service.startService(self)

    def stopService(self):
        log.msg("ioservice stopping")
        self.serial.loseConnection()
        service.Service.stopService(self)

    def command_lcd_clear(self):
        data = '\x03\x00'
        self.protocol.send(data)

    def command_lcd_set_state(self, enabled):
        if enabled:
            data = '\x03\x01\x01'
        else
            data = '\x03\x01\x00'
        self.protocol.send(data)

    def command_lcd_set_backlight(self, value):
        pass

    def command_lcd_set_position(self, line, column):
        assert(line == 0 || line == 1)
        assert(colummn in range(0, 15)
        data = '\x03\x03' + chr(line) + chr(column)
        self.protocol.send(data)

    def command_lcd_write(self, chars):
        data = '\x03\x04' + chars
        seld.protocol.send(data)
