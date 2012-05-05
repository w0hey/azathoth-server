from twisted.internet import defer
from twisted.python import log

class Drive:
    def __init__(self, robotservice):
        self.robotservice = robotservice
        self.driveservice = robotservice.driveservice
        self.cal_x_cur = 0
        self.cal_y_cur = 0
        self.cal_x_eeprom = 0
        self.cal_y_eeprom = 0
    
    def command_calibrate_x(self, value):
        self.driveservice.command_calibrate_x(value)

    def command_calibrate_y(self, value):
        self.driveservice.command_calibrate_y(value)

    def command_store_calibration(self):
        self.driveservice.command_store_calibration()

    def command_joystick(self, x, y):
        self.driveservice.command_joystick(x, y)

    def command_softstop(self):
        self.driveservice.command_softstop(self)
        
    def request_calibration(self):
        d = self.driveservice.request_calibration()
        d.addCallback(self.update_calibration)
        return d

    def update_calibration(self, d):
        log.msg(system="Drive", format="update_calibration")
        self.cal_x_cur = d['current_x']
        self.cal_y_cur = d['current_y']
        self.cal_x_eeprom = d['eeprom_x']
        self.cal_y_eeprom = d['eeprom_y']
        return d
