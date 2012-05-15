from twisted.internet import protocol

from azathoth.protocols.telnetprotocol import TelnetProtocol

class ShellFactory(protocol.ServerFactory):
    protocol = TelnetProtocol
    def __init__(self, service):
        self.service = service
        self.robot = service.getServiceNamed('robotservice')
        self.clients = []

