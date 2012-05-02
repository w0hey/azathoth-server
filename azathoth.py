#!/usr/bin/env python

from twisted.application import service, internet
from twisted.internet import protocol, reactor
from twisted.python import log
from twisted.internet.serialport import SerialPort
from twisted.protocols.basic import NetstringReceiver
from protocols import telnetprotocol
from protocols import controlprotocol
from protocols import linkprotocol


class TelnetFactory(protocol.ServerFactory):
    protocol = telnetprotocol.TelnetProtocol
    def __init__(self, service):
        self.service = service
    
    def logPrefix(self):
        return "TelnetFactory"

class ControlFactory(protocol.ServerFactory):
    protocol = controlprotocol.ControlProtocol
    def __init__(self, service):
        self.service = service

class DriveProtocol(linkprotocol.LinkProtocol):
    def __init__(self, service):
        self.service = service
        linkprotocol.LinkProtocol.__init__(self)

    def handle_packet(self, packet):
        pass

class IoProtocol(linkprotocol.LinkProtocol):
    def __init__(self, service):
        self.service = service
        linkprotocol.LinkProtocol.__init__(self)

    def handle_packet(self, packet):
        pass


class DriveService(service.Service):
    name = "driveservice"
    def __init__(self):
        pass
    
    def startService(self):
        log.msg("driveservice starting")
        self.protocol = DriveProtocol(self)
        log.msg(format="opening serial connection on %(port)s", port=driveport)
        self.serial = SerialPort(self.protocol, driveport, reactor)
        service.Service.startService(self)

    def stopService(self):
        log.msg("driveservice stopping")
        service.Service.stopService(self)

    def command_joystick(self, xpos, ypos):
        """
        Commands the drive interface to simulate the joystick position
        specified by xpos and ypos.
        """
        data = '\x30' + chr(xpos) + chr(ypos)
        self.protocol.send(data)


class IoService(service.Service):
    name = "ioservice"
    def __init__(self):
        pass

    def startService(self):
        log.msg("ioservice starting")
        self.protocol = IoProtocol(self)
        log.msg(format="opening serial connection on %(port)s", port=ioport)
        #self.serial = SerialPort(self.protocol, ioport, reactor)
        service.Service.startService(self)

    def stopService(self):
        log.msg("ioservice stopping")
        service.Service.stopService(self)

telnet_port = 2023
control_port = 2024
driveport = '/home/steve/COM1'
ioport = '/home/steve/COM1'

top_service = service.MultiService()

drive_service = DriveService()
drive_service.setServiceParent(top_service)

io_service = IoService()
io_service.setServiceParent(top_service)

telnetfactory = TelnetFactory(drive_service)
telnet_service = internet.TCPServer(telnet_port, telnetfactory)
telnet_service.setServiceParent(top_service)

controlfactory = ControlFactory(drive_service)
control_service = internet.TCPServer(control_port, controlfactory)
control_service.setServiceParent(top_service)

application = service.Application('azathoth')

top_service.setServiceParent(application)
