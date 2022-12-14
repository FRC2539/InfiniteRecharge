from .movecommand import MoveCommand

import robot
from custom.config import Config

import math


class TurnCommand(MoveCommand):
    '''Allows autonomous turning using the drive base encoders.'''

    def __init__(self, degrees, name=None):
        if name is None:
            name = 'Turn %f degrees' % degrees

        super().__init__(degrees, False, name)

        self.degrees = degrees
        self.fDegrees = abs(self.degrees)
        self.drivetrainWidth = 27.75

    def initialize(self):
        '''Calculates new positions by offseting the current ones.'''

        robot.drivetrain.resetGyro()
        robot.drivetrain.setProfile(2)

        offset = math.copysign(self._calculateDisplacement(), self.degrees)

        print('offset ' + str(offset))

        self.targetPositions = []

        for position in robot.drivetrain.getPositions():
            self.targetPositions.append(position + offset)

        print('target ' + str(self.targetPositions))

        robot.drivetrain.setPositions(self.targetPositions, False)

    def isFinished(self):
        ''' Get the current angle to the desired position, and stop it if it's nearby. '''
        #print(robot.drivetrain.getAngle())
        return abs(robot.drivetrain.getAngleTo(self.degrees)) <= 1


    def end(self):
        robot.drivetrain.stop()
        robot.drivetrain.setProfile(0)

    def _calculateDisplacement(self):
        '''
        In order to avoid having a separate ticksPerDegree, we calculate it
        based on the width of the robot base.
        '''

        inchesPerDegree = math.pi * self.drivetrainWidth / 360 #Config('DriveTrain/width') / 360 # 24.5 degrees to radians
        totalDistanceInInches = self.distance * inchesPerDegree
        units = robot.drivetrain.inchesToUnits(totalDistanceInInches)

        return units

        #return units #* Config('DriveTrain/slip', 1.2)
