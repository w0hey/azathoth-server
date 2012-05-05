from twisted.application import service
from twisted.python import log

class RobotService(service.Service):
    name = "robotservice"
    
    def __init__(self, top_service):
        self.top_service = top_service

    def startService(self):
        log.msg("robotservice starting")
        self.driveservice = top_service.getServiceNamed('driveservice')
        self.ioservice = top_service.getServiceNamed('ioservice')
        self.controlservice = top_service.getServiceNamed('controlservice')
        self.shellservice = top_service.getServiceNamed('shellservice')
        service.Service.startService(self)

    def stopService(self):
        log.msg("robotservice stopping")
        service.Service.stopService(self)
