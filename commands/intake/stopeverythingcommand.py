from wpilib.command import InstantCommand

import robot

class StopEverythingCommand(InstantCommand):

    def __init__(self):
        super().__init__('Stop Everything')

        self.requires(robot.shooter)
        self.requires(robot.ballsystem)
        self.requires(robot.ledsystem)

    def initialize(self):
        robot.ballsystem.stopAll()
        robot.shooter.stop()

        robot.ledsystem.turnOff()
