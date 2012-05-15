from twisted.internet import protocol

from azathoth.protocols.controlprotocol import ControlProtocol

class ControlFactory(protocol.ServerFactory):
    protocol = ControlProtocol
    def __init__(self, robotservice):
        self.clients = []
        self.robot = robotservice
