from twisted.internet import protocol
from twisted.python import log

from azathoth.protocols.linkframe import LinkFrame

class LinkProtocol(protocol.Protocol):
    """
    A twisted protocol object handling serial communication via
    Azathoth's Link protocol. The protocol is based around a stripped-
    down version of the XBee API mode protocol.
    Code in this class borrows heavily from txXBee by Wagner Sartori Junior,
    and code from python-xbee by Paul Malmsten.
    """

    def __init__(self):
        self._frame = None

    def dataReceived(self, data):
        #log.msg("dataReceived: " + data)
        for c in data:
            if (self._frame and c == LinkFrame.START_BYTE):
                # Bad frame, restart
                log.err(system='LinkProtocol', format="Unexpected start byte")
                self.handle_badframe(self._frame.raw_data)
                self._frame = None
            if self._frame:
                self._frame.fill(c)
                if self._frame.remaining_bytes() == 0:
                    try:
                        # try to parse and return result
                        self._frame.parse()
                        self.handle_packet(self._split_response(self._frame.data))
                    except ValueError:
                        # Bad frame, restart
                        self.handle_badframe(self._frame.raw_data)
                    self._frame = None
            else:
                if c == LinkFrame.START_BYTE:
                    self._frame = LinkFrame()
                    self._frame.fill(c)

    def handle_packet(self, packet):
        """
        This method should be overridden in a subclass.
        It will be called whenever the protocol has a complete packet
        to handle
        """
        pass

    def handle_badframe(self, packet):
        """
        This method can be overridden in a subclass.
        It will be called whenever the protocol receives a bad frame.
        """
        pass

    def _write(self, data):
        # TODO: This method is spurious, in txXBee is overrides
        # the underlying ZigBee class's _write method.
        # all this code can safely be added to our send() method.
        frame = LinkFrame(data).output()
        self.transport.write(frame)

    def _split_response(self, data):
        # TODO: This method is spurious. Unlike python-xbee, we
        # only need to handle one type of data packet (so far).
        return data

    def send(self, data):
        """
        This method passes the provided data to _write() to be framed
        as a packet and sent over the wire.
        """
        log.msg(system='LinkProtocol', format="Sending frame: %(data)s", data=map(hex,map(ord,list(data)))) #yikes
        self._write(data)
