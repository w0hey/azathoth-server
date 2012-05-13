from twisted.application import service
from twisted.internet import reactor, defer
from twisted.internet.serialport import SerialPort
from twisted.python import log

from protocols.driveprotocol import DriveProtocol

class DriveService(service.Service):
    name = "driveservice"
    def __init__(self, port, speed=115200):
        self.port = port
        self.speed = speed
        self.cal_x_cur = 0
        self.cal_y_cur = 0
        self.cal_x_eeprom = 0
        self.cal_y_eeprom = 0

    def startService(self):
        log.msg(system='DriveService', format="service starting")
        self.protocol = DriveProtocol(self)
        log.msg(system='DriveService', format="opening serial port %(port)s", port=self.port)
        self.serial = SerialPort(self.protocol, self.port, reactor, baudrate=self.speed)
        self.protocol.register_callback(0x01, self.onHandshake)
        self.protocol.register_callback(0x41, self.onReceiveCalibration)
        self.protocol.register_callback(0x42, self.onReceiveStatus)
        self.protocol.register_callback(0xee, self.onDriveError)
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

    def onHandshake(self, data):
        log.msg(system='DriveService', format="Controller is alive")

    def onDriveError(self, data):
        log.msg(system='DriveService', format="Controller error, code %(code)#x", code=data[0])

    def onReceiveStatus(self, data):
        status = data[0];
        xpos = data[1];
        ypos = data[2];
        xval = data[3];
        yval = data[4];

    def onReceiveCalibration(self, data):
        log.msg(system='DriveService', format="receivied calibration values")
        calibration = {}
        calibration['current_x'] = data[0]
        calibration['current_y'] = data[1]
        calibration['eeprom_x'] = data[2]
        calibration['eeprom_y'] = data[3]
        self.cal_x_cur = data[0]
        self.cal_y_cur = data[1]
        self.cal_x_eeprom = data[2]
        self.cal_y_eeprom = data[3]
        if self.calibration_d is not None:
            self.calibration_d.callback(calibration)
            self.calibration_d = None
