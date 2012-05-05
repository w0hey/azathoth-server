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
