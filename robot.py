#!/usr/bin/env python3

# Monkey-patching out NetworkTables methods
import wpilib
wpilib.SmartDashboard.putData = lambda x, y: None
class MockSendableChooser:
    def addDefault(self, x, y):
        self.choice = y
    def getSelected(self):
        return self.choice
wpilib.SendableChooser = MockSendableChooser
import networktables
def mockAddTableListener(x, y, localNotify=None):
    pass
networktables.NetworkTable.addTableListener = mockAddTableListener
import wpilib.command
wpilib.command.Command.isFinished = lambda x: False

from commandbased import CommandBasedRobot
from wpilib._impl.main import run
from wpilib import RobotBase

from custom import driverhud
import controller.layout
import subsystems
import shutil, sys

from wpilib.command import Subsystem

from subsystems.monitor import Monitor as monitor
from subsystems.drivetrain import DriveTrain as drivetrain
from subsystems.colorwheel import  ColorWheel as colorwheel
from subsystems.intake import Intake as intake
from subsystems.limelight import Limelight as limelight
from subsystems.hood import Hood as hood
from subsystems.turret import Turret as turret
from subsystems.shooter import Shooter as shooter
from subsystems.ballsystem import BallSystem as ballsystem

class KryptonBot(CommandBasedRobot):
    '''Implements a Command Based robot design'''

    def robotInit(self):
        '''Set up everything we need for a working robot.'''

        if RobotBase.isSimulation():
            import mockdata

        self.subsystems()
        controller.layout.init()
        driverhud.init()

        from commands.startupcommandgroup import StartUpCommandGroup
        #StartUpCommandGroup().start()


    def autonomousInit(self):
        '''This function is called each time autonomous mode starts.'''

        # Send field data to the dashboard
        driverhud.showField()

        # Schedule the autonomous command
        auton = driverhud.getAutonomousProgram()
        auton.start()
        driverhud.showInfo("Starting %s" % auton)

    @classmethod
    def subsystems(cls):
        vars = globals()
        module = sys.modules['robot']
        for key, var in vars.items():
            try:
                print(str(key) + ' + ' + str(var) + ' & ' + str(issubclass(var, Subsystem) and var is not Subsystem))
                if issubclass(var, Subsystem) and var is not Subsystem:
                    try:
                        setattr(module, key, var())
                    except Exception as e:
                        raise ValueError(f'Could not instantiate {key}') from e
            except TypeError:
                pass


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'deploy':
        shutil.rmtree('opkg_cache', ignore_errors=True)
        shutil.rmtree('pip_cache', ignore_errors=True)

    run(KryptonBot)
