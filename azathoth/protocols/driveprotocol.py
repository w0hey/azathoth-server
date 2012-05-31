from twisted.python import log

from azathoth.protocols.controllerprotocol import ControllerProtocol

class DriveProtocol(ControllerProtocol):
    def __init__(self, service):
        ControllerProtocol.__init__(self, service)

    def cmd_mode(self, mode):
        """Change the drive mode. Mode:
        0x00: Local "Wheelchair" mode.
        0x01: Remote "Robot" mode.
        """

    def cmd_joystick(self, xpos, ypos):
        """
        Command movement by directly simulating a joystick position
        xpos, ypos: the commanded position as a signed value relative to center
        """
        data = '\x30' + chr(xpos) + chr(ypos)
        self.send(data)
        
    def cmd_calibrate_set(self, xvalue, yvalue):
        """
        Set the drive controller's joystick center position
        xvalue, yvalue: new center position, raw PWM values
        """
        data = '\x40\x00' + chr(xvalue) + chr(yvalue)
        self.send(data)
    
    def cmd_calibrate_store(self):
        """
        Writes the current calibration values to the drive controller's
        EEPROM
        """
        data = '\x40\x10'
        self.send(data)

    def cmd_driveselect(self, enable):
        """
        Enables/disables "remote" control of the drive system
        enable: True - Electronics have control. False - Onboard joystick
        has control.
        """
        if enable:
            data = '\x43\x01'
        else:
            data = '\x43\x00'
        self.send(data)

    def cmd_reset(self):
        """
        Instructs the controller to pull in the e-stop relay,
        resetting the emergency stop
        """
        self.send('\xfe')

    def cmd_estop(self):
        """
        Instructs the controller to release the e-stop relay,
        causing an emergency stop
        """
        self.send('\xff')

    def req_calibration(self):
        """
        Asks the drive controller to send its current calibration
        values. Will result in a 0x41 response
        """
        self.send('\x41')
