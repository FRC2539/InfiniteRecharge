from wpilib.command import Command

import robot

from controller import logicalaxes

logicalaxes.registerAxis('turretX')

class TurretMoveCommand(Command):

    def __init__(self):
        super().__init__('turret Move')

        self.requires(robot.turret)

    def execute(self):
        robot.turret.testMove(logicalaxes.turretX.get() * -0.75)
        #print(robot.turret.getPosition())
        #print(robot.turret.getPosition())

    def end(self):
        robot.turret.stop()
