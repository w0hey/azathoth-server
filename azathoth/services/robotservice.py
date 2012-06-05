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
        self.hId = 1

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
        """register an event handler

        event -- a string naming the event to handle
        handler -- a function to call when this event fires

        returns an integer handler id which can be used
        to unregister the event
        """
        id = self.hId
        self.handlers[event].append((id, handler))
        self.hId = self.hId + 1
        return id

    def delHandler(self, event, id):
        """deregister an event handler

        event -- a string naming the event this handler is watching
        id -- the integer id of the handler to remove
        """
        for h in self.handlers[event]:
            if h[0] == id:
                del h

    def triggerEvent(self, event, *args):
        """fire event handlers for a given event

        event -- a string naming the event to fire
        
        all remaining arguments are passed to the event handler
        """
        if event in self.handlers:
            for h in self.handlers[event]:
                h[1](*args)
        else:
            return
