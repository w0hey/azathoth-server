from twisted.application import service
from twisted.python import log

from devices.drive import Drive
from devices.lcd import Lcd

class RobotService(service.Service):
    name = "robotservice"
    
    def __init__(self, top_service):
        self.top_service = top_service

    def startService(self):
        log.msg(system='RobotService', format="service starting")
        service.Service.startService(self)
        self.driveservice = self.top_service.getServiceNamed('driveservice')
        self.ioservice = self.top_service.getServiceNamed('ioservice')
        self.controlservice = self.top_service.getServiceNamed('controlservice')
        self.shellservice = self.top_service.getServiceNamed('shellservice')
        self.drive = Drive(self)
        self.lcd = Lcd(self)

    def stopService(self):
        log.msg(system='RobotService', format="service stopping")
        service.Service.stopService(self)
