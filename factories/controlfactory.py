from twisted.internet import protocol

from protocols.controlprotocol import ControlProtocol

class ControlFactory(protocol.ServerFactory):
    protocol = ControlProtocol
    def __init__(self, service):
        self.clients = []
        self.service = service
