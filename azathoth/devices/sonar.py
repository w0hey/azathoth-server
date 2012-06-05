class Sonar:
    def __init__(self, ioservice):
        self.ioservice = ioservice
        ioservice.protocol.register_callback(0x40, self._onReceiveRange)

    def _onReceiveRange(self, data):
        self.lastRange = data[0]
        self.ioservice.parent.triggerEvent('SONAR_RANGE', self.lastRange)
