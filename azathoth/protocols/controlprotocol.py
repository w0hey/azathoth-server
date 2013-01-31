from twisted.python import log
from twisted.protocols.basic import NetstringReceiver

class ControlProtocol(NetstringReceiver):

    def connectionMade(self):
        log.msg("Got connection")
        self.factory.clients.append(self)
        self.robot = self.factory.robot
        self.statusHandler = self.robot.addHandler('DRV_STATUS', self.send_status)
        self.sonarHandler = self.robot.addHandler('SONAR_RANGE', self.send_sonar)

    def connectionLost(self, reason):
        log.msg(format="Lost connection, reason: %(reason)s", reason=reason.getErrorMessage())
        self.robot.delHandler('DRV_STATUS', self.statusHandler)
        self.robot.delHandler('SONAR_RANGE', self.sonarHandler)
        self.factory.clients.remove(self)

    def stringReceived(self, string):
        log.msg(format="String received: %(string)s", string=string)
        if string[0] == 'c':
            # calibration value request
            d = self.robot.drive.getCalibration()
            d.addCallback(self.send_calibration)

        elif string[0] == 'C':
            # calibration set command
            log.msg("got calibration command")
            x = ord(string[1])
            y = ord(string[2])
            self.robot.drive.setCalibration(x, y)

        elif string[0] == 'J':
            # Joystick position command
            xpos = ord(string[1])
            ypos = ord(string[2])
            self.robot.drive.directJoystick(xpos, ypos)

        elif string[0] == 'D':
            # Drive select command
            if string[1] == '\x00':
                self.robot.drive.driveSelect(False)
            elif string[1] == '\x01':
                self.robot.drive.driveSelect(True)

        elif string[0] == 'E':
            # E-stop
            self.robot.drive.estop()

        elif string[0] == 'R':
            # Reset E-stop
            self.robot.drive.reset()
        
        elif string[0] == 'S':
            # soft stop command
            self.robot.drive.stop()

        elif string[0] == 'W':
            # calibration store command
            self.robot.drive.storeCalibration()
        
    def send_calibration(self, d):
        log.msg(system="ControlProtocol", format="send_calibration, data=%(data)s", data=d)
        cur_x = d['current_x']
        cur_y = d['current_y']
        eeprom_x = d['eeprom_x']
        eeprom_y = d['eeprom_y']
        data = 'c' + chr(cur_x) + chr(cur_y) + chr(eeprom_x) + chr(eeprom_y)
        self.sendString(data)

    def send_status(self, status, xpos, ypos, xvalue, yvalue):
        data = 's' + chr(status) + chr(xpos) + chr(ypos) +chr(xvalue) + chr(yvalue)
        self.sendString(data)

    def send_sonar(self, sonar_range):
        #data = 'r' + chr(sonar_range)
        self.sendString(data)

    def send_error(self, source, error):
        # TODO
        pass

