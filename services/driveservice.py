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
        log.msg(system='DriveService', format="service starting")
        self.protocol = DriveProtocol(self)
        log.msg(system='DriveService', format="opening serial port %(port)s", port=self.port)
        self.serial = SerialPort(self.protocol, self.port, reactor, baudrate=self.speed)
        self.robotservice = self.topservice.getServiceNamed('robotservice')
        self.protocol.register_callbacks('0x41', self.onReceiveCalibration)
        service.Service.startService(self)
    
    def stopService(self):
        log.msg(system='DriveService', format="service stopping")
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

    def onReceiveCalibration(self, data):
        log.msg(system='DriveService', format="receivied calibration values")
        calibration = {}
        calibration['current_x'] = data[0]
        calibration['current_y'] = data[1]
        calibration['eeprom_x'] = data[2]
        calibration['eeprom_y'] = data[3]
        self.calibration_d.callback(calibration)
