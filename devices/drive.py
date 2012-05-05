from twisted.internet import defer

class Drive:
    def __init__(self, robotservice):
        self.robotservice = robotservice
        self.driveservice = robotservice.driveservice
        self.cal_x_cur = 0
        self.cal_y_cur = 0
        self.cal_x_eeprom = 0
        self.cal_y_eeprom = 0
    
    def request_calibration(self):
        d = self.driveservice.request_calibration()
        d.addCallBack(self.update_calibration)
        return d

    def update_calibration(self, d):
        self.cal_x_cur = d['current_x']
        self.cal_y_cur = d['current_y']
        self.cal_x_eeprom = d['eeprom_x']
        self.cal_y_eeprom = d['eeprom_y']
