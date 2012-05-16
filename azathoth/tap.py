from twisted.python import usage
import azathoth

DEFAULT_TELNETPORT = 2023
DEFAULT_CONTROLPORT = 2024
DEFAULT_DRIVEDEVICE = '/dev/arduino_A9007MiE'
DEFAULT_IODEVICE = '/dev/arduino_A900ae1d'

class Options(usage.Options):
    optParameters = [["port", "p", DEFAULT_CONTROLPORT,
                      "The port number to listen on."],
                     ["telnetport", "t", DEFAULT_TELNETPORT,
                      "The port number to bind the telnet shell server to."],
                     ["drive", "d", DEFAULT_DRIVEDEVICE,
                      "The serial port connected to the drive controller"],
                     ["io", "i", DEFAULT_IODEVICE,
                      "The serial port connected to the IO controller"]
                     ]


def makeService(options):
    return azathoth.makeService(options)
