from wpilib.command import Command
from custom import driverhud
from custom.config import MissingConfigError
import robot

class GyroMoveCommand(Command):

    def __init__(self, distance, avoidCollisions=False, name=None):
        '''
        Takes a distance in inches and stores it for later. We allow overriding
        name so that other autonomous driving commands can extend this class.
        '''

        if name is None:
            name = 'Move %f inches' % distance

        super().__init__(name, 0.2)

        self.distance = distance
        self.blocked = False
        self.avoidCollisions = avoidCollisions
        self.requires(robot.drivetrain)


    def _initialize(self):
        super()._initialize()
        self.precision = robot.drivetrain.inchesToUnits(1)

    def initialize(self):
        #print('began Move command \n\n')
        self.obstacleCount = 0
        self.blocked = False
        self.onTarget = 0
        self.targetPositions = []
        offset = robot.drivetrain.inchesToUnits(self.distance)
        sign = 1
        for position in robot.drivetrain.getPositions():
            self.targetPositions.append(position + (offset * sign))
            sign *= -1

        #print('target: ' + str(self.targetPositions))

        robot.drivetrain.gyroSetPositon(self.targetPositions)

    def execute(self):
        if self.avoidCollisions:
            try:
                if self.distance < 0:
                    clearance = robot.drivetrain.getRearClearance()
                else:
                    clearance = robot.drivetrain.getFrontClearance()

                if not self.blocked:
                    if clearance < 10:
                        if self.obstacleCount >= 10:
                            self.blocked = True
                            self.obstacleCount = 0
                            robot.drivetrain.stop()
                            robot.drivetrain.move(0, 0, 0)
                            driverhud.showAlert('Obstacle Detected')
                        else:
                            self.obstacleCount += 1
                    else:
                        self.obstacleCount = 0

                else:
                    if clearance >= 20:
                        if self.obstacleCount >= 10:
                            self.blocked = False
                            self.obstacleCount = 0
                            robot.drivetrain.setPositions(self.targetPositions)
                        else:
                            self.obstacleCount += 1
                    else:
                        self.obstacleCount = 0

            except NotImplementedError:
                pass

        robot.drivetrain.gyroSetPositon(self.targetPositions)

    def isFinished(self):
        if self.blocked:
            return False

        if self.isTimedOut() and robot.drivetrain.atPosition(self.targetPositions, self.precision):
            self.onTarget += 1
        else:
            self.onTarget = 0

        return self.onTarget > 5
