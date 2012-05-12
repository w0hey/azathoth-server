from twisted.python import log
from protocols.linkprotocol import LinkProtocol

class DriveProtocol(LinkProtocol):
    def __init__(self, service):
        self.service = service
        self.callbacks = {}
        LinkProtocol.__init__(self)

    def register_callback(self, cmd, callback):
        self.callbacks[cmd] = callback

    def unregister_callback(self, cmd):
        del self.callbacks[cmd]

    def handle_packet(self, packet):
        log.msg(system='DriveProtocol', format="Got packet: %(data)s", data=list(packet))
        # let's fix this data here and now.
        data = map(ord, packet)
        cmd = data[0]
        if cmd in self.callbacks:
            self.callbacks[cmd](packet[1:])
        else:
            log.msg(system='DriveProtocol', format="No callback for command: %(cmd)s", cmd=cmd)
        #if packet[0] == '\x41':
            # calibration response
        #    x_cur = ord(packet[1])
        #    y_cur = ord(packet[2])
        #    x_eeprom = ord(packet[3])
        #    y_eeprom = ord(packet[4])
        #    self.service.receive_calibration(x_cur, y_cur, x_eeprom, y_eeprom)

    def handle_badframe(self, data):
        log.err(system='DriveProtocol', format="bad frame received: %(data)s", data=data)
