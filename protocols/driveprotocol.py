from twisted.python import log
from protocols.linkprotocol import LinkProtocol

class DriveProtocol(LinkProtocol):
    def __init__(self, service):
        self.service = service
        LinkProtocol.__init__(self)

    def handle_packet(self, packet):
        if packet[0] = '\x41':
            # calibration response
            x_cur = packet[1]
            y_cur = packet[2]
            x_eeprom = packet[3]
            y_eeprom = packet[4]
            self.service.receive_calibration(x_cur, y_cur, x_eeprom, y_eeprom)

    def handle_badframe(self, data):
        log.err(system='DriveProtocol', format="bad frame received: %(data)s", data=data)
