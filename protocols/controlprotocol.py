from twisted.python import log
from twisted.protocols.basic import NetstringReceiver

class ControlProtocol(NetstringReceiver):

    def connectionMade(self):
        log.msg("Got connection")
        self.factory.clients.append(self)
        self.robot = self.factory.robot

    def connectionLost(self, reason):
        log.msg(format="Lost connection, reason: %(reason)s", reason=reason)
        self.factory.clients.remove(self)

    def stringReceived(self, string):
        log.msg(format="String received: %(string)s", string=string)
        if string[0] == 'c':
            # calibration value request
            d = self.robot.drive.request_calibration()
            d.addCallback(self.send_calibration)

        elif string[0] == 'C':
            # calibration set command
            log.msg("got calibration command")
            x = ord(string[1])
            y = ord(string[2])
            self.robot.drive.command_calibrate_x(x)
            self.robot.drive.command_calibrate_y(y)
        
        elif string[0] == 'J':
            # Joystick position command
            xpos = ord(string[1])
            ypos = ord(string[2])
            self.robot.drive.command_joystick(xpos, ypos)
        
    def send_calibration(self, d):
        log.msg(system="ControlProtocol", format="send_calibration, data=%(data)s", data=d)
        cur_x = d['current_x']
        cur_y = d['current_y']
        eeprom_x = d['eeprom_x']
        eeprom_y = d['eeprom_y']
        data = chr(cur_x) + chr(cur_y) + chr(eeprom_x) + chr(eeprom_y)
        self.sendString(data)

