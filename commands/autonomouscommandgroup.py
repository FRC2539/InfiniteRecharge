from wpilib.command import CommandGroup, PrintCommand
from wpilib import DriverStation as _ds

from networktables import NetworkTables

import commandbased.flowcontrol as fc
from custom.config import Config

#from commands.network.alertcommand import AlertCommand

from commands.drivetrain.movecommand import MoveCommand
from commands.drivetrain.turncommand import TurnCommand
from commands.drivetrain.gyromovecommand import GyroMoveCommand
from commands.drivetrain.curvecommand import CurveCommand

class AutonomousCommandGroup(fc.CommandFlow):
    def __init__(self):
        super().__init__('Autonomous')

        #establish the auto modes for dashboard and use these values in auto if string check
        table = NetworkTables.getTable('Autonomous')
        autoNames = ['Turn','Move','Move Turn Move']
        autoString = ''
        for auto in autoNames:
            autoString += str(auto + '$')
        autoString = autoString[:-1]
        table.putString('autoModes', autoString)

        startingBalls = 3#Config('Autonomous/NumberOfBallsAtStart', 3)

        @fc.IF(lambda: str(Config('Autonomous/autoModeSelect')) == 'Turn')
        def Turn(self):#should be good for now
            ##self.addSequential(MoveCommand(80))
            ##self.addSequential(PrintCommand("turn 90"))
            self.addSequential(TurnCommand(90))
            ##self.addSequential(CurveCommand(-125, 30, False))
            ##self.addSequential(CurveCommand(-130, 30, True))
            #self.addSequential(MoveCommand(45))
            ##self.addSequential(MoveCommand(-45))



        @fc.IF(lambda: str(Config('Autonomous/autoModeSelect')) == 'Move')
        def Move(self):#should be good for now
            self.addSequential(MoveCommand(120))
            #self.addSequential(TurnCommand(90))
            self.addSequential(MoveCommand(-120))


        @fc.IF(lambda: str(Config('Autonomous/autoModeSelect')) == 'Move Turn Move')
        def MTM(self):
            pass
            #self.addSequential(PrintCommand("SafetyHazard"))
            self.addSequential(MoveCommand(40), 2)
            self.addSequential(TurnCommand(90), 2)
            self.addSequential(MoveCommand(-40), 2)

        @fc.IF(lambda: str(Config('Autonomous/autoModeSelect')) == 'Auto 1')
        def auto1(self):#should be good for now
            self.addSequential(MoveCommand(80))
            ##self.addSequential(PrintCommand("turn 90"))
            ##self.addSequential(TurnCommand(90))
            self.addSequential(CurveCommand(-125, 30, False))
            ##self.addSequential(CurveCommand(-130, 30, True))
            #self.addSequential(MoveCommand(45))
            ##self.addSequential(MoveCommand(-45))


