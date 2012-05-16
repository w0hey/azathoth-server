from twisted.python import log

from azathoth.protocols.linkprotocol import LinkProtocol

class IoProtocol(LinkProtocol):
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
        log.msg(system='IoProtocol', format="Got packet: %(data)s", data=map(hex,data))
        cmd = data[0]
        if cmd in self.callbacks:
            self.callbacks[cmd](data[1:])
        else:
            log.msg(system='IoProtocol', format="No callback for command: %(cmd)s", cmd=cmd)

    def handle_badframe(self, data):
        log.err(system="IoProtocol", format="bad frame received: %(data)s", data=data)

