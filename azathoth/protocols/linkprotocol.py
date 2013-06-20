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
        for c in data:
            # this is, essentially, a state machine. Unfortunately,
            # a decent amount of it's logic is actually in the
            # LinkFrame itself.
            if (self._frame and c == LinkFrame.START_BYTE):
                # We're already in a frame, but we got a start byte,
                # something got trashed.
                log.msg(system='LinkProtocol', format="Unexpected start byte")
                self.handle_badframe(self._frame.raw_data)
                self._frame = None
            if self._frame:
                # We are in a frame, add this byte to it
                self._frame.fill(c)
                if self._frame.remaining_bytes() == 0:
                    # We're at the last byte, according to the frame's length
                    # field
                    try:
                        # try to parse and return result
                        self._frame.parse()
                        self.handle_packet(self._split_response(self._frame.data))
                    except ValueError:
                        # Any number of things could have gone wrong,
                        # it'd be nice to know what, but fuckit,
                        # let's hand the error up a level and start over!
                        # most likely this means we tried to parse() a frame
                        # before receiving it's full header, which shouldn't
                        # happen.
                        self.handle_badframe(self._frame.raw_data)
                    self._frame = None
            else:
                if c == LinkFrame.START_BYTE:
                    # This is the start of a new frame, so
                    # create a LinkFrame to hold it and start
                    # packing it in.
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
        # If this were python3, the preceding line would be even worse.
        frame = LinkFrame(data).output()
        self.transport.write(frame)
