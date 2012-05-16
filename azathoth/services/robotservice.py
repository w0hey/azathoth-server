from collections import defaultdict
from twisted.application import service
from twisted.python import log

from azathoth.devices.lcd import Lcd

class RobotService(service.MultiService):
    name = "robotservice"
    
    def __init__(self, top_service):
        self.top_service = top_service
        service.MultiService.__init__(self)
        self.handlers = defaultdict(list)

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

    def addHandler(self, event, handler):
        # this is sub-optimal, because we have no real way
        # to remove a handler once it's added.
        self.handlers[event].append(handler)

    def delHandler(self, event):
        #TODO
        pass

    def getHandlers(self, event):
        # Hey look, I found a way to make this even less elegant!
        # this returns a list of handlers to be called for a given event
        # calling those handlers with appropriate arguments is up to the
        # emitter of the event
        return self.handlers[event]

