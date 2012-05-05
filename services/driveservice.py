from twisted.application import service
from twisted.internet import reactor
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
