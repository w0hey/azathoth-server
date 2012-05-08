from twisted.application import service
from twisted.internet import reactor, defer
from twisted.internet.serialport import SerialPort
from twisted.python import log

from protocols.driveprotocol import DriveProtocol

class DriveService(service.Service):
    name = "driveservice"
    def __init__(self, topservice, port, speed=115200):
        self.port = port
        self.speed = speed
        self.topservice = topservice

    def startService(self):
        log.msg("driveservice starting")
        self.protocol = DriveProtocol(self)
        log.msg(format="driveservice opening serial port %(port)s", port=self.port)
        self.serial = SerialPort(self.protocol, self.port, reactor, baudrate=self.speed)
        self.robotservice = self.topservice.getServiceNamed('robotservice')
        service.Service.startService(self)
    
    def stopService(self):
        log.msg("driveservice stopping")
        self.serial.loseConnection()
        service.Service.stopService(self)

    def command_calibrate_x(self, value):
        data = '\x40\x00' + chr(value)
        self.protocol.send(data)

    def command_calibrate_y(self, value):
        data = '\x40\x01' + chr(value)
        self.protocol.send(data)

    def command_store_calibration(self):
        data = '\x40\x10'
        self.protocol.send(data)

    def command_joystick(self, x, y):
        data = '\x30' + chr(x) + chr(y)
        self.protocol.send(data)

    def command_softstop(self):
        self.protocol.send('\xf0')

    def request_calibration(self):
        data = '\x41'
        self.protocol.send(data)
        self.calibration_d = defer.Deferred()
        return self.calibration_d

    def receive_calibration(self, x_cur, y_cur, x_eeprom, y_eeprom):
        log.msg("receivied calibration")
        calibration = {}
        calibration['current_x'] = x_cur
        calibration['current_y'] = y_cur
        calibration['eeprom_x'] = x_eeprom
        calibration['eeprom_y'] = y_eeprom
        self.calibration_d.callback(calibration)
