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
        self.clients = []
        self.service = service
        self.driveservice = service.getServiceNamed('driveservice')
        self.ioservice = service.getServiceNamed('ioservice')
        self.driveservice.controlfactory = self

class DriveProtocol(linkprotocol.LinkProtocol):
    def __init__(self, service):
        self.service = service
        linkprotocol.LinkProtocol.__init__(self)

    def handle_packet(self, packet):
        log.msg(format="Got packet: %(data)s", data=packet)
        if packet[0] == '\x41':
            # calibration request response
            x_current = packet[1]
            y_current = packet[2]
            x_eeprom = packet[3]
            y_eeprom = packet[4]
            self.service.update_calibration(x_current, y_current, x_eeprom, y_eeprom)

    def handle_badframe(self, packet):
        log.msg(format="Got bad frame: %(data)s", data=packet)

class IoProtocol(linkprotocol.LinkProtocol):
    def __init__(self, service):
        self.service = service
        linkprotocol.LinkProtocol.__init__(self)

    def handle_packet(self, packet):
        pass


class DriveService(service.Service):
    name = "driveservice"
    def __init__(self):
        self.cal_x_current = 0
        self.cal_y_current = 0
        self.cal_x_eeprom = 0
        self.cal_y_eeprom = 0
        self.controlfactory = None
        self.wait_for_cal_data = False
    
    def startService(self):
        log.msg("driveservice starting")
        self.protocol = DriveProtocol(self)
        log.msg(format="opening serial connection on %(port)s", port=driveport)
        self.serial = SerialPort(self.protocol, driveport, reactor)
        service.Service.startService(self)

    def stopService(self):
        log.msg("driveservice stopping")
        service.Service.stopService(self)

    def request_calibration(self):
        """
        Asks the drive interface to send us it's current calibration values.
        """
        data = '\x41'
        self.protocol.send(data)
        self.wait_for_cal_data = True

    def command_joystick(self, xpos, ypos):
        """
        Commands the drive interface to simulate the joystick position
        specified by xpos and ypos.
        """
        data = '\x30' + chr(xpos) + chr(ypos)
        self.protocol.send(data)

    def command_calibrate_x(self, xval):
        """
        Sets the "center" value for the simulated joystick X axis
        """
        data = '\x40\x00' + chr(xval)
        self.protocol.send(data)

    def command_calibrate_y(self, yval):
        """
        Sets the "center" value for the simulated joystick Y axis
        """
        data = '\x40\x01' + chr(yval)
        self.protocol.send(data)

    def update_calibration(self, x_current, y_current, x_eeprom, y_eeprom):
        self.cal_x_current = x_current
        self.cal_y_current = y_current
        self.cal_x_eeprom = x_eeprom
        self.cal_y_eeprom = y_eeprom
        if self.wait_for_cal_data:
            string = 'c' + x_current + y_current + x_eeprom + y_eeprom
            for client in self.controlfactory.clients:
                client.sendString(string)
            self.wait_for_cal_data = False
            


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

# we pass top_service into our factories so they can lookup other services
# when needed. It feels like there should be a better way to do this.
telnetfactory = TelnetFactory(top_service)
telnet_service = internet.TCPServer(telnet_port, telnetfactory)
telnet_service.setName('telnetservice')
telnet_service.setServiceParent(top_service)

controlfactory = ControlFactory(top_service)
control_service = internet.TCPServer(control_port, controlfactory)
control_service.setName('controlservice')
control_service.setServiceParent(top_service)

application = service.Application('azathoth')

top_service.setServiceParent(application)
for srvice in top_service.__iter__():
    print srvice.name
print vars(control_service)
