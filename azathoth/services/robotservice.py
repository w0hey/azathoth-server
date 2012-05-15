from twisted.application import service
from twisted.python import log

from azathoth.devices.lcd import Lcd

class RobotService(service.MultiService):
    name = "robotservice"
    
    def __init__(self, top_service):
        self.top_service = top_service
        service.MultiService.__init__(self)

    def startService(self):
        log.msg(system='RobotService', format="service starting")
        service.MultiService.startService(self)
        self.drive = self.getServiceNamed('driveservice')
        self.io = self.getServiceNamed('ioservice')
        self.controlservice = self.top_service.getServiceNamed('controlservice')
        self.shellservice = self.top_service.getServiceNamed('shellservice')

    def stopService(self):
        log.msg(system='RobotService', format="service stopping")
        service.MultiService.stopService(self)
