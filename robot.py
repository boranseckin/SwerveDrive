#!/usr/bin/env python3

import wpilib

import magicbot
from magicbot.magic_tunable import tunable

import ctre

from robotpy_ext.control.button_debouncer import ButtonDebouncer

from networktables import NetworkTables
from networktables.util import ntproperty

from components import swervemodule, swervedrive

class MyRobot(magicbot.MagicRobot):

    drive = swervedrive.SwerveDrive

    def createObjects(self):
        """
        Create basic components (motor controller, joysticks, etc.).
        """
        # Initialize SmartDashboard
        self.sd = NetworkTables.getTable('SmartDashboard')

        # Joysticks
        self.left_joystick = wpilib.Joystick(0)
        self.right_joystick = wpilib.Joystick(1)

        # VictorSPX Motor Controllers - Drive
        self.frontLeftMotor = ctre.WPI_VictorSPX(0)
        self.frontRightMotor = ctre.WPI_VictorSPX(2)
        self.rearLeftMotor = ctre.WPI_VictorSPX(4)
        self.rearRightMotor = ctre.WPI_VictorSPX(6)

        # VictorSPX Motor Controllers - Rotate
        self.frontLeftRotate = ctre.WPI_VictorSPX(1)
        self.frontRightRotate = ctre.WPI_VictorSPX(3)
        self.rearLeftRotate = ctre.WPI_VictorSPX(5)
        self.rearRightRotate = ctre.WPI_VictorSPX(7)

        # Absolute Encoders
        self.frontLeftEnc = wpilib.AnalogInput(0)
        self.frontRightEnc = wpilib.AnalogInput(1)
        self.rearLeftEnc = wpilib.AnalogInput(2)
        self.rearRightEnc = wpilib.AnalogInput(3)

        ####### CHANGE ZEROs and INVERTED #######
        # Drive Modules
        self.frontLeftModule = swervemodule.SwerveModule(self.frontLeftMotor, self.frontLeftRotate, self.frontLeftEnc, sd_prefix='FrontLeft_Module', zero=0.0, inverted=False)
        self.frontRightModule = swervemodule.SwerveModule(self.frontRightMotor, self.frontRightRotate, self.frontRightEnc, sd_prefix='FrontRight_Module', zero=0.0, inverted=False)
        self.rearLeftModule = swervemodule.SwerveModule(self.rearLeftMotor, self.rearLeftRotate, self.rearLeftEnc, sd_prefix='RearLeft_Module', zero=0.0, inverted=False)
        self.rearRightModule = swervemodule.SwerveModule(self.rearRightMotor, self.rearRightRotate, self.rearRightEnc, sd_prefix='RearRight_Module', zero=0.0, inverted=False)

    def robotInit(self):
        super().robotInit()

    def disabledPeriodic(self):
        self.update_sd()

    def disabledInit(self):
        """
        Empty
        """

    def autonomous(self):
        """
        Empty
        """

    def teleopInit(self):
        self.drive.flush()
        self.drive.allow_reverse = True
        self.drive.wait_for_align = False
        self.drive.squared_inputs = True
        self.drive.threshold_input_vectors = True

    def move(self, x, y, rcw):
        if self.right_joystick.getRawButton(1):
            rcw *= 0.75

        self.drive.move(x, y, rcw)

    def teleopPeriodic(self):
        # Drive System
        self.move(self.left_joystick.getY() * -1, self.left_joystick.getX() * -1, self.right_joystick.getX())
        # self.move(self.left_joystick.getRawAxis(1) * -1, self.left_joystick.getRawAxis(0), self.left_joystick.getRawAxis(2) *- 1)

        if self.left_joystick.getRawButton(2):
            self.drive.request_wheel_lock = True

        if self.right_joystick.getRawButton(4):
            self.drive.set_raw_strafe(0.25)
        elif self.right_joystick.getRawButton(5):
            self.drive.set_raw_strafe(-0.25)
        if self.right_joystick.getRawButton(3):
            self.drive.set_raw_fwd(0.35)
        elif self.right_joystick.getRawButton(2):
            self.drive.set_raw_fwd(-0.35)

        self.update_sd()

    def update_sd(self):
        self.drive.update_smartdash()

if __name__ == "__main__":
    wpilib.run(MyRobot)