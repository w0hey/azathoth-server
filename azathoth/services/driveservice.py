from twisted.application import service
from twisted.internet import reactor, defer
from twisted.internet.serialport import SerialPort
from twisted.python import log

from azathoth.protocols.driveprotocol import DriveProtocol

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
        self.protocol.register_callback(0x01, self._onHandshake)
        self.protocol.register_callback(0x41, self._onReceiveCalibration)
        self.protocol.register_callback(0x42, self._onReceiveStatus)
        self.protocol.register_callback(0xee, self._onDriveError)
        service.Service.startService(self)
    
    def stopService(self):
        log.msg(system='DriveService', format="service stopping")
        self.serial.loseConnection()
        service.Service.stopService(self)

    def setMode(self, mode):
        self.protocol.cmd_mode(mode)

    def directJoystick(self, xpos, ypos):
        self.protocol.cmd_joystick(xpos, ypos)

    def setCalibration(self, xvalue, yvalue):
        self.protocol.cmd_calibrate_set(xvalue, yvalue)

    def storeCalibration(self):
        self.protocol.cmd_calibrate_store()

    def driveSelect(self, enable):
        self.protocol.cmd_driveselect(enable)

    def stop(self):
        self.protocol.cmd_joystick(0, 0)

    def estop(self):
        self.protocol.cmd_estop()

    def reset(self):
        self.protocol.cmd_reset()

    def getCalibration(self):
        self.protocol.req_calibration()
        self.calibration_d = defer.Deferred()
        return self.calibration_d

    def _onHandshake(self, data):
        log.msg(system='DriveService', format="Controller is alive")
        self.parent.triggerEvent('DRV_HANDSHAKE')

    def _onDriveError(self, data):
        log.msg(system='DriveService', format="Controller error, code %(code)#x", code=data[0])
        self.parent.triggerEvent('DRV_ERROR', data[0])

    def _onReceiveStatus(self, data):
        status = data[0];
        xpos = data[1];
        ypos = data[2];
        xval = data[3];
        yval = data[4];
        self.parent.triggerEvent('DRV_STATUS', status, xpos, ypos, xval, yval)

    def _onReceiveCalibration(self, data):
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
