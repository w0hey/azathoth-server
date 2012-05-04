from twisted.internet import protocol

from protocols.telnetprotocol import TelnetProtocol

class ShellFactory(protocol.ServerFactory):
    protocol = TelnetProtocol
    def __init__(self, service):
        self.service = service
        self.clients = []

