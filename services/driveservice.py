from twisted.application import service
from twisted.internet import reactor, defer
from twisted.internet.serialport import SerialPort
from twisted.python import log

from protocols.driveprotocol import DriveProtocol

class DriveService(service.Service):
    name = "driveservice"
    def __init__(self, robotservice, port, speed=115200):
        self.port = port
        self.speed = speed
        self.robot = robotservice

    def startService(self):
        log.msg("driveservice starting")
        self.protocol = DriveProtocol(self)
        log.msg(format="driveservice opening serial port %(port)s", port=self.port)
        self.serial = SerialPort(self.protocol, self.port, reactor, baudrate=self.speed)
        service.Service.startService(self)
    
    def stopService(self):
        log.msg("driveservice stopping")
        self.serial.loseConnection()
        service.Service.stopService(self)

    def request_calibration(self):
        data = '\x41'
        self.protocol.send(data)
        self.calibration_d = defer.Deferred()
        return self.calibration_d

    def receive_calibration(self, x_cur, y_cur, x_eeprom, y_eeprom):
        calibration = {}
        calibration['current_x'] = x_cur
        calibration['current_y'] = y_cur
        calibration['eeprom_x'] = x_eeprom
        calibration['eeprom_y'] = y_eeprom
        self.calibration_d(calibration)
