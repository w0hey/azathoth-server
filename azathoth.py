from twisted.application import service, internet
from twisted.python import log

from services.driveservice import DriveService
from services.ioservice import IoService
from factories.shellfactory import ShellFactory
from factories.controlfactory import ControlFactory

telnet_port = 2023
control_port = 2024
driveport = '/dev/arduino_A9007MiE'
ioport = '/dev/arduino_A900ae1d'

top_service = service.MultiService()

drive_service = DriveService(top_service, driveport, 115200)
drive_service.setServiceParent(top_service)

io_service = IoService(top_service, ioport, 115200)
io_service.setServiceParent(top_service)

shell_factory = ShellFactory(top_service)
shell_service = internet.TCPServer(telnet_port, shell_factory)
shell_service.setName('shellservice')
shell_service.setServiceParent(top_service)

control_factory = ControlFactory(top_service)
control_service = internet.TCPServer(control_port, control_factory)
control_service.setName('controlservice')
control_service.setServiceParent(top_service)

application = service.Application('azathoth')

top_service.setServiceParent(application)
