from twisted.python import log

from azathoth.protocols.linkprotocol import LinkProtocol

class ControllerProtocol
    def __init__(self, service):
        self.service = service
        self.callbacks = {}
        LinkProtocol.__init__(self)

    def register_callback(self, cmd, callback):
        self.callbacks[cmd] = callback

    def unregister_callback(self, packet):
        del self.callbacks[cmd]

    def handle_packet(self, packet):
        data = map(ord, packet)
        #TODO: log call goes here
        cmd = data[0]
        if cmd in self.callbacks:
            self.callbacks[cmd](data[1:])
        else:
            #TODO: log/raise error, whatever
            pass

    def handle_badframe(self, data):
        #TODO: log/raise error, whatever
        
