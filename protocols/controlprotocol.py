from twisted.python import log
from twisted.protocols.basic import NetstringReceiver

class ControlProtocol(NetstringReceiver):

    def connectionMade(self):
        log.msg("Got connection")

    def connectionLost(self, reason):
        log.msg(format="Lost connection, reason: %(reason)s", reason=reason)

    def stringReceived(self, string):
        log.msg(format="String received: %(string)s", string=string)
