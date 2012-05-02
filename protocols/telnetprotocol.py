#!/usr/bin/env python

from twisted.internet import reactor
from twisted.protocols import telnet
from twisted.python import log

class TelnetProtocol(telnet.Telnet):
   #FIXME don't get to attached to this code; protocols.telnet is deprecated
   # this should be re-written using twisted.conch
    def connectionMade(self):
        log.msg("Incoming connection")
        telnet.Telnet.connectionMade(self)


    def checkUserAndPass(self, user, passwd):
        if user == 'robot' and passwd == 'robot':
            return True
        return False

    def telnet_Command(self, line):
        if line == "js":
            self.factory.service.command_joystick(128, 128)
        if line == "exit":
            self.transport.loseConnection()
        if line == "kill":
            reactor.stop()
        else:
            self.write(line + "\r\n")
        return "Command"
    
    def logPrefix(self):
        return "TelnetProtocol"
