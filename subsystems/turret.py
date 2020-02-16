from .debuggablesubsystem import DebuggableSubsystem

import wpilib

import ports
from ctre import ControlMode, FeedbackDevice, WPI_TalonSRX, NeutralMode

import robot

class Turret(DebuggableSubsystem):
    '''Describe what this subsystem does.'''

    def __init__(self):
        super().__init__('Turret')
        self.motor = WPI_TalonSRX(ports.turret.motorID)
        self.motor.config_kP(0, .0001, 0)
        self.motor.config_kI(0, 0, 0)
        self.motor.config_kD(0, .001, 0)
        self.motor.config_kF(0, .00019, 0)
        self.motor.config_IntegralZone(0, 0, 0)
        self.max = 2300 # Dummy values
        self.min = 0 # Dummy values

        self.fieldAngle = 0

        self.motor.setNeutralMode(NeutralMode.Brake)

        self.motor.configSelectedFeedbackSensor(FeedbackDevice.CTRE_MagEncoder_Absolute)
        self.motor.setSelectedSensorPosition(0, 0, 0)
        #self.motor.setPulseWidthPosition(0, 0)  # NOTE: Temporary reset at beginning in attmept to zero the sensor.

    def rotateClockwise(self, val):
        if self.getPosition() < self.max and self.getPosition() > self.min:
            self.motor.set(val)
            return False
        else:
            self.stop()

        #if(self.motor.getSelectedSensorPosition(0)>self.max and self.motor.getSelectedSensorPosition(0)<self.min):
            #self.motor.set(ControlMode.PercentOutput, speed)
        #else:
            #print('hit turret limit')
            #self.motor.stopMotor()
        #self.motor.set(ControlMode.PercentOutput, val)<--
        #print('pulse position ' + str(self.motor.getPulseWidthPosition()))

    def move(self, val):
        if self.getPosition() < self.max and self.getPosition() > self.min:
            self.motor.set(ControlMode.PercentOutput, val)
        elif self.getPosition() > self.max and val > 0:
            self.motor.set(ControlMode.PercentOutput, val)
        elif self.getPosition() < self.min and val < 0:
            self.motor.set(ControlMode.PercentOutput, val)
        else:
            self.stop()

    def stop(self):
        self.motor.stopMotor()

    def givePosition(self):
        self.motor.setSelectedSensorPosition(1500)

    def returnZero(self):
        self.motor.set(ControlMode.Position, 0)

    def captureOrientation(self):
        self.fieldAngle = robot.drivetrain.getAngle()

    def turretFieldOriented(self): # Use for when traveling 'round the field.
        degrees = (self.fieldAngle - robot.drivetrain.getAngle()) * 0.003
        if self.getPosition() + 2 < self.max and self.getPosition() - 2 > self.min:
            self.motor.set(ControlMode.PercentOutput, degrees)
        else:
            self.stop()

    def setPosition(self, degrees):
        #degrees = degrees % 360
        ticks = ((degrees % 360) / 360) * 4096 # returns the set tick positions, keeping input under 360 (puts to ticks)

        if degrees > self.min and degrees < self.max:
            self.motor.set(ControlMode.Position, ticks)
        else:
            self.motor.stopMotor()

    def printPosition(self):
        print(str(self.motor.getSelectedSensorPosition(0)))

    def getPosition(self):
        #return (self.motor.getSelectedSensorPosition(0) % 360)
        return (self.motor.getSelectedSensorPosition(0))

    #def setZero(self):
        #self.zero = self.getPosition() % 360 # keeps below 360 degrees
        #if self.zero > 180:
            #self.zero = (self.zero - 180) * -1 # sets a zero between -180 and 180. IT WORKS.

    def setZero(self):
        self.motor.setSelectedSensorPosition(0, 0, 0)

    def initDefaultCommand(self):
        '''
        By default, unless another command is running that requires this
        subsystem, we will drive via joystick using the max speed stored in
        Config.
        '''
        from commands.turret.turretmovecommand import TurretMoveCommand

        self.setDefaultCommand(TurretMoveCommand())

