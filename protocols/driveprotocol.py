from twisted.python import log
from protocols.linkprotocol import LinkProtocol

class DriveProtocol(LinkProtocol):
    def __init__(self, service):
        self.service = service
        LinkProtocol.__init__(self)

    def handle_packet(self, packet):
        pass

    def handle_badframe(self, data):
        log.err(system='DriveProtocol', format="bad frame received: %(data)s", data=data)
