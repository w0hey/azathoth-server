#!/usr/bin/env python

from twisted.internet import reactor
from twisted.protocols import telnet
from twisted.python import log

class TelnetProtocol(telnet.Telnet):
   #FIXME don't get to attached to this code; protocols.telnet is deprecated
   # this should be re-written using twisted.conch
    def connectionMade(self):
        log.msg(system="TelnetProtocol", format="Incoming connection")
        self.factory.clients.append(self)
        telnet.Telnet.connectionMade(self)

    def connectionLost(self, reason):
        log.msg(system="TelnetProtocol", format="Connection lost, reason: %(reason)s", reason=reason.getErrorMessage())
        self.factory.clients.remove(self)
        telnet.Telnet.connectionLost(self)

    def checkUserAndPass(self, user, passwd):
        if user == 'robot' and passwd == 'robot':
            self.write("> ")
            return True
        return False

    def telnet_Command(self, line):
        if line == "lcd":
            self.write("lcd > ")
            return "Lcd"
        if line == "exit":
            self.transport.loseConnection()
        if line == "kill":
            reactor.stop()
        else:
            self.write("lcd exit kill\r\n")
        self.write("> ")
        return "Command"

    def telnet_Lcd(self, line):
        if line == "exit":
            self.write("> ")
            return "Command"
        if line == "clear":
           self.factory.robot.io.lcd.clear()
        else:
            self.write("clear exit\r\n")
        self.write("lcd > ")
        return "Lcd"
    
    def logPrefix(self):
        return "TelnetProtocol"
