from .basedrive import BaseDrive
from ctre import ControlMode
from wpilib.drive import RobotDriveBase
import ports

class SkidDrive(BaseDrive):
    '''A drive base where all wheels on each side move together.'''

    def _configureMotors(self, robot):
        if robot:
            '''Only the front motors are active in a skid system.'''
            self.activeMotors = self.motors[0:2]
            self.followerMotors = self.motors[2:4]

            '''Make the back motors follow the front.'''
            if len(self.motors) == 4:
                self.motors[2] \
                    .follow(self.motors[0])
                self.motors[3] \
                    .follow(self.motors[1])

            '''Invert encoders'''
            for motor in self.activeMotors:
                motor.setSensorPhase(True)

        else:
            self.activeMotors = self.motors[0:2]
            self.followerMotors = self.motors[2:4]

            '''Make the back motors follow the front.'''
            if len(self.motors) == 4:
                self.motors[RobotDriveBase.MotorType.kRearLeft] \
                    .follow(self.motors[RobotDriveBase.MotorType.kFrontLeft])
                self.motors[RobotDriveBase.MotorType.kRearRight] \
                    .follow(self.motors[RobotDriveBase.MotorType.kFrontRight])

            #print('configured followers')

    def _calculateSpeeds(self, x, y, rotate):
        return [y + rotate, -y + rotate]
