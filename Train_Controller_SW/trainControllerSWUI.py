import PyQt6.QtGui as QtGui
import threading
import time
import os

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
from PyQt6.uic import loadUi

# from Train_Controller_SW.trainControllerSW import TrainController


class UI(QMainWindow):
    def __init__(self, trainctrl):
        super(UI, self).__init__()

        # create train object
        self.trainctrl = trainctrl

        # took from lucas (Track_Controller_SW/TrackController.UI), thank you Lucas
        current_dir = os.path.dirname(__file__)
        ui_path = os.path.join(current_dir, "trainControllerSW_UI.ui")
        try:
            loadUi(ui_path, self)
        except Exception as e:
            print("Error with loading ui file: ", e)

        # open with set dimensions
        self.setFixedWidth(810)
        self.setFixedHeight(545)

        self.extLights.setEnabled(False)
        self.intLights.setEnabled(False)
        self.temp.setEnabled(False)
        self.doorControl.setEnabled(False)
        self.kp.setEnabled(False)
        self.ki.setEnabled(False)
        self.setPtSpeed.setEnabled(False)
        self.servBrake.setEnabled(False)

        # TODO set default values

        self.doorsLeft.setChecked(False)
        self.doorsRight.setChecked(False)
        self.speedLim.setText(f'{self.trainctrl.speedLim}')
        self.temp.setValue(int(self.trainctrl.cabinTemp))
        self.kp.setValue(int(self.trainctrl.kp))
        self.ki.setValue(int(self.trainctrl.ki))
        self.currSpeed.setText(f'{self.trainctrl.currSpeed}')
        self.power.setText(f'{self.trainctrl.power}')
        self.setPtSpeed.setValue(int(self.trainctrl.setPtSpeed))

        # TODO make connections
        self.testBench.clicked.connect(self.testingbench)
        self.actSpeedTB.valueChanged.connect(self.changecurrspeed)
        self.cmdSpeedTB.valueChanged.connect(self.changecmdspeed)
        self.speedLimTB.valueChanged.connect(self.changespeedlim)
        self.vitalAuthTB.valueChanged.connect(self.changevitalauth)
        self.accelLimTB.valueChanged.connect(self.changeaccellim)
        self.decelLimTB.valueChanged.connect(self.changedecellim)
        self.passEBrakeTB.clicked.connect(self.passebrake)
        self.trackStateTB.clicked.connect(self.trackstate)
        self.failSigPickupTB.clicked.connect(self.signalfail)
        self.failEngineTB.clicked.connect(self.enginefail)
        self.failBrakeTB.clicked.connect(self.brakefail)
        self.doorLeftTB.clicked.connect(self.doorleft)
        self.doorRightTB.clicked.connect(self.doorright)
        self.beaconTB.textChanged.connect(self.beaconupdate)

        self.autoMode.clicked.connect(self.automodeswitcher)
        self.manualMode.clicked.connect(self.manualmodeswitcher)

        self.doorControl.clicked.connect(self.doors)
        self.intLights.valueChanged.connect(self.changeintlights)
        self.extLights.valueChanged.connect(self.changeextlights)
        self.temp.valueChanged.connect(self.tempcontrol)
        self.eBrake.clicked.connect(self.ebrake)
        self.setPtSpeed.valueChanged.connect(self.speedupdate)
        self.kp.valueChanged.connect(self.changekp)
        self.ki.valueChanged.connect(self.changeki)
        self.servBrake.clicked.connect(self.useservicebrake)

        # show the app
        self.show()

    # define procedures

    def testingbench(self):
        if self.trainctrl.testBenchState == 0:  # open test bench
            self.trainctrl.testbenchcontrol()
            self.setFixedWidth(1197)
            self.setFixedHeight(733)
            self.testBench.setText("Close Test Bench")
            print("test bench opened")
        elif self.trainctrl.testBenchState == 1:  # close test bench
            self.trainctrl.testbenchcontrol()
            self.setFixedWidth(810)
            self.setFixedHeight(545)
            self.testBench.setText("Open Test Bench")
            print("test bench closed")

    def automodeswitcher(self):
        if self.trainctrl.mode == 1:  # train running in manual mode
            self.trainctrl.modeswitch()  # put train into auto mode
            self.extLights.setEnabled(False)
            self.intLights.setEnabled(False)
            self.temp.setEnabled(False)
            self.doorControl.setEnabled(False)
            self.kp.setEnabled(False)
            self.ki.setEnabled(False)
            self.setPtSpeed.setEnabled(False)
            self.servBrake.setEnabled(False)
            self.inMode.setText("Automatic Mode")
        return

    def manualmodeswitcher(self):
        if self.trainctrl.mode == 0:  # train running in auto mode
            self.trainctrl.modeswitch()  # put train into manual mode
            self.extLights.setEnabled(True)
            self.intLights.setEnabled(True)
            self.temp.setEnabled(True)
            self.doorControl.setEnabled(True)
            self.kp.setEnabled(True)
            self.ki.setEnabled(True)
            self.setPtSpeed.setEnabled(True)
            self.servBrake.setEnabled(True)
            self.inMode.setText("Manual Mode")
        return

    def changecurrspeed(self):
        self.trainctrl.setcurrspeed = self.actSpeedTB.value()
        self.currSpeed.setText(str(self.trainctrl.currSpeed))

    def changecmdspeed(self):
        self.trainctrl.cmdSpeed = self.cmdSpeedTB.value()

    def changespeedlim(self):
        self.trainctrl.speedLim = self.speedLimTB.value()
        self.speedLim.setText(str(self.trainctrl.speedLim))

    def changevitalauth(self):
        self.trainctrl.vitalAuth = self.vitalAuthTB.value()

    def changeaccellim(self):
        self.trainctrl.accelLim = self.accelLimTB.value()

    def changedecellim(self):
        self.trainctrl.decelLim = self.decelLimTB.value()

    def passebrake(self):

        self.trainctrl.passebrakecontrol()
        self.refreshengine()
        if self.trainctrl.passEBrake == 0:
            self.passEBrakeTB.setText("Off")
        elif self.trainctrl.passEBrake == 1:
            self.passEBrakeTB.setText("On")
            self.setPtSpeed.setValue(self.trainctrl.setPtSpeed)

    def trackstate(self):
        self.trainctrl.circuitpolaritycontrol()
        if self.trainctrl.circuitPolarity() == 0:  # track is negative polarity
            self.trackStateTB.setText("-")
        elif self.trainctrl.circuitPolarity() == 1:  # track is positive polarity
            self.trackStateTB.setText("+")

    def signalfail(self):
        self.trainctrl.signalfailcontrol()
        if self.trainctrl.signalFail == 0:  # no signal pickup failure
            self.failSigPickupTB.setText("Off")
            self.signalFail.setChecked(self.trainctrl.signalFail)   # should be false
        elif self.trainctrl.signalFail == 1:  # signal pickup failure
            self.failSigPickupTB.setText("On")
            self.signalFail.setChecked(self.trainctrl.signalFail)  # should be true
            self.trainctrl.failhandler()
            self.refreshengine()

    def enginefail(self):
        self.trainctrl.enginefailcontrol()
        if self.trainctrl.engineFail == 0:  # no signal pickup failure
            self.failEngineTB.setText("Off")
            self.engineFail.setChecked(self.trainctrl.engineFail)  # should be false
        elif self.trainctrl.engineFail == 1:  # signal pickup failure
            self.failEngineTB.setText("On")
            self.engineFail.setChecked(self.trainctrl.engineFail)  # should be true
            self.trainctrl.failhandler()
            self.refreshengine()

    def brakefail(self):
        self.trainctrl.brakefailcontrol()
        if self.trainctrl.brakeFail == 0:  # no signal pickup failure
            self.failBrakeTB.setText("Off")
            self.brakeFail.setChecked(self.trainctrl.brakeFail())  # should be false
        elif self.trainctrl.brakeFail == 1:  # signal pickup failure
            self.failBrakeTB.setText("On")
            self.brakeFail.setChecked(self.trainctrl.brakeFail)  # should be true
            self.trainctrl.failhandler()
            self.refreshengine()

    def doorleft(self):
        if self.trainctrl.doorSide == 0:
            self.trainctrl.doorSide = 1
            self.doorsLeft.setChecked(1)
        elif self.trainctrl.doorSide == 1:
            self.trainctrl.doorSide = 0
            self.doorsLeft.setChecked(0)
        elif self.trainctrl.doorSide == 2:
            self.trainctrl.doorSide = 3
            self.doorsLeft.setChecked(1)
        elif self.trainctrl.doorSide == 3:
            self.trainctrl.doorSide = 2
            self.doorsLeft.setChecked(0)

    def doorright(self):
        if self.trainctrl.doorSide == 0:
            self.trainctrl.doorSide = 2
            self.doorsRight.setChecked(1)
        elif self.trainctrl.doorSide == 1:
            self.trainctrl.doorSide = 3
            self.doorsRight.setChecked(1)
        elif self.trainctrl.doorSide == 2:
            self.trainctrl.doorSide = 0
            self.doorsRight.setChecked(0)
        elif self.trainctrl.doorSide == 3:
            self.trainctrl.doorSide = 1
            self.doorsRight.setChecked(0)

    def beaconupdate(self):
        self.trainctrl.parsebeacon(str(self.beaconTB.toPlainText()))

    def changeextlights(self):
        self.trainctrl.extlightscontrol()

    def changeintlights(self):
        self.trainctrl.intlightscontrol()

    def tempcontrol(self):
        self.trainctrl.tempcontrol(self.temp.value())

    def doors(self):
        if self.doorsLeft.isChecked() and not self.doorsRight.isChecked():
            self.trainctrl.doorSide = 1
        elif not self.doorsLeft.isChecked() and self.doorsRight.isChecked():
            self.trainctrl.doorSide = 2
        elif self.doorsLeft.isChecked() and self.doorsRight.isChecked():
            self.trainctrl.doorSide = 3
        else:
            self.trainctrl.doorSide = 0

        self.trainctrl.doorcontrol()

        if self.trainctrl.doorState == 1:  # doors open
            self.doorControl.setText("Opened")
            self.testLabel.setText(f'door state is {self.trainctrl.doorState}')
            self.doorLabel.setText(f'doors open and left is {self.trainctrl.doorL} '
                                   f'and right is {self.trainctrl.doorR}')
            self.testLabel.adjustSize()
            self.doorLabel.adjustSize()
        elif self.trainctrl.doorState == 0:  # doors closed
            self.doorControl.setText("Closed")
            self.testLabel.setText(f'door state is {self.trainctrl.doorState}')
            self.doorLabel.setText(f'doors closed and left is {self.trainctrl.doorL} '
                                   f'and right is {self.trainctrl.doorR}')
            self.testLabel.adjustSize()
            self.doorLabel.adjustSize()

    def ebrake(self):
        self.trainctrl.ebrakecontrol()
        if self.trainctrl.eBrake == 0:
            self.eBrake.setText("EMERGENCY BRAKE: OFF")
            self.testLabel.setText(f'ebrake off and {self.trainctrl.eBrake}')
            self.testLabel.adjustSize()
            self.refreshengine()
        elif self.trainctrl.eBrake == 1:
            self.eBrake.setText("EMERGENCY BRAKE: ON")
            self.testLabel.setText(f'ebrake off and {self.trainctrl.eBrake}')
            self.testLabel.adjustSize()
            # self.setPtSpeed.setValue(self.trainctrl.setPtSpeed) # crashes here, probably because speed is undefined
            self.refreshengine()

    def speedupdate(self):
        if self.trainctrl.eBrake == 0 and self.trainctrl.passEBrake == 0:
            f'{self.setPtSpeed.value()}'
            self.trainctrl.setsetptspeed(self.setPtSpeed.value())
            self.refreshengine()
        #elif self.trainctrl.eBrake() == 1 or self.trainctrl.passEBrake == 1:
            #self.setPtSpeed.setValue(0)

    def changekp(self):
        self.trainctrl.kp = self.kp.value()
        self.refreshengine()

    def changeki(self):
        self.trainctrl.ki = self.ki.value()
        self.refreshengine()

    def useservicebrake(self):
        if self.trainctrl.servBrake == 0:
            self.trainctrl.setservbrake(1)
            self.servBrake.setText("Service Brake: On")
            self.refreshengine()
        elif self.trainctrl.servBrake == 1:
            self.trainctrl.setservbrake(0)
            self.servBrake.setText("Service Brake: Off")
            self.refreshengine()

    def refreshengine(self):
        self.setPtSpeed.setValue(int(self.trainctrl.setPtSpeed))
        self.speedLim.setText(str(self.trainctrl.speedLim))
        self.currSpeed.setText(str(int(self.trainctrl.currSpeed)))
        self.power.setText(str(self.trainctrl.power))
        self.kp.setValue(int(self.trainctrl.kp))
        self.ki.setValue(int(self.trainctrl.ki))

    def powerrefresh(self):
        for i in range(0, 23):
            self.setPtSpeed.setValue(int(self.trainctrl.setPtSpeed))
            self.speedLim.setText(str(self.trainctrl.speedLim))
            self.currSpeed.setText(str(int(self.trainctrl.currSpeed)))
            self.power.setText(str(self.trainctrl.power))
            self.kp.setValue(int(self.trainctrl.kp))
            self.ki.setValue(int(self.trainctrl.ki))
            print(i)
            time.sleep(5)

    # TODO setpt speed from driver, service brake, power calcs, speed calcs and checks, beacon

def main():
    # initialize the app
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()

if __name__ == '__main__':
    main()


