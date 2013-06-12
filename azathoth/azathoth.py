from twisted.application import service, internet
from twisted.python import log, usage

from services.driveservice import DriveService
from services.ioservice import IoService
from services.robotservice import RobotService
from factories.shellfactory import ShellFactory
from factories.controlfactory import ControlFactory


def makeService(options):
    top_service = service.MultiService()

    robot_service = RobotService(top_service)
    robot_service.setServiceParent(top_service)

    drive_service = DriveService(options['drivedevice'], 115200)
    drive_service.setServiceParent(robot_service)

    io_service = IoService(options['iodevice'], 115200)
    io_service.setServiceParent(robot_service)

    shell_factory = ShellFactory(top_service)
    shell_service = internet.TCPServer(int(options['telnetport']), shell_factory)
    shell_service.setName('shellservice')
    shell_service.setServiceParent(top_service)

    control_factory = ControlFactory(robot_service)
    control_service = internet.TCPServer(int(options['port']), control_factory)
    control_service.setName('controlservice')
    control_service.setServiceParent(top_service)
    
    return top_service
