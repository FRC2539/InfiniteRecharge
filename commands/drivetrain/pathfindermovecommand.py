# Everything in meters!

from wpilib.command import Command

from ctre import ControlMode

import robot

import math

import pathfinder as pf

from pathfinder.followers import EncoderFollower

class PathfinderMoveCommand(Command):

    def __init__(self):
        super().__init__('Pathfinder Move')

        self.requires(robot.drivetrain)

    def initialize(self):
        points = [
        pf.Waypoint(-4, -1, 0),   # Waypoint @ x=-4, y=-1, exit angle=-45 degrees
        pf.Waypoint(0, 0, 0),                       # Waypoint @ x=0, y=0,   exit angle=0 radians
        ]

        info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH,
                                    dt=0.02, # 20ms
                                    max_velocity=5,
                                    max_acceleration=6,
                                    max_jerk=120.0)

        modifier = pf.modifiers.TankModifier(trajectory).modify(2.0)

        self.left = EncoderFollower(modifier.getLeftTrajectory())
        self.right = EncoderFollower(modifier.getRightTrajectory())

        robot.drivetrain.resetEncoders()

        self.left.configureEncoder(robot.drivetrain.getPositions()[0], 2048, 0.5)
        self.right.configureEncoder(robot.drivetrain.getPositions()[1], 2048, 0.5)

        self.left.configurePIDVA(1.0, 0.0000, 0, (1 / 5), 0)
        self.right.configurePIDVA(1.0, 0.0000, 0, (1 / 5), 0)

        robot.drivetrain.resetGyro()

        self.heading = robot.drivetrain.getAngle()

    def execute(self):
        pos = robot.drivetrain.getPositions()

        self.leftOutput = self.left.calculate(pos[0])
        self.rightOutput = self.right.calculate(pos[1])

        self.heading = robot.drivetrain.getAngle()

        self.desiredHeading = pf.r2d(self.left.getHeading())

        angleDifference = pf.boundHalfDegrees(self.desiredHeading - self.heading)
        turn = 5 * (-1.0 / 80.0) * angleDifference

        robot.drivetrain.activeMotors[0].set(ControlMode.PercentOutput, -(self.leftOutput + turn))
        robot.drivetrain.activeMotors[1].set(ControlMode.PercentOutput, -(self.rightOutput - turn))

        print('LEFT: ' + str(self.leftOutput + turn))
        print('RIGHT: ' + str(self.rightOutput - turn))

    def end(self):
        robot.drivetrain.stop()