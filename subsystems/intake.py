import ports

from .debuggablesubsystem import DebuggableSubsystem

from rev import CANSparkMax, MotorType

class Intake(DebuggableSubsystem):
    def __init__(self):
        super().__init__('Intake')

        self.intakeMotor = CANSparkMax(ports.IntakePorts.motorID, MotorType.kBrushed)

        self.intakeMotor.setInverted(False)

        self.ballCount = 0

    def intake(self):
        print(self.intakeMotor.getDeviceId())
        self.intakeMotor.set(1)

    def outake(self):
        self.intakeMotor.set(-1.0)

    def stop(self):
        self.intakeMotor.stopMotor()

    def monitorIntake(self): # Experimental
        # Gets output current, puts it in milliamperes. The free current (of a bag) at top speed is about 1.8 amps, will spike if more resistance (ball) - see motor chart.
        current = self.intakeMotor.getOutputCurrent()
        print(current)
        if current * 1000 > 1800:
            self.ballCount += 1

    def maintainBalls(self):
        self.intakeMotor.set(0.4)
