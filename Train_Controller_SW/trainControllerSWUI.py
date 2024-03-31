import PyQt6.QtGui as QtGui
import threading
import time

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
import trainControllerSW
from PyQt6 import uic

# create train object
trainctrl = trainControllerSW.TrainController()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # load the ui file
        uic.loadUi("trainControllerSW_UI.ui", self)

        # open with set dimensions
        self.setFixedWidth(810)
        self.setFixedHeight(545)

        # actions for automatic mode launch
        threading.Thread(target=trainctrl.automode).start()
        self.refreshengine()
        # threading.Thread(target=self.powerrefresh).start()

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
        self.speedLim.setText(f'{trainctrl.speedLim}')
        self.temp.setValue(int(trainctrl.cabinTemp))
        self.kp.setValue(int(trainctrl.kp))
        self.ki.setValue(int(trainctrl.ki))
        self.currSpeed.setText(f'{trainctrl.currSpeed}')
        self.power.setText(f'{trainctrl.power}')

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
        if trainctrl.testBenchState() == 0:  # open test bench
            trainctrl.testBenchState = 1
            self.setFixedWidth(1197)
            self.setFixedHeight(733)
            self.testBench.setText("Close Test Bench")
        elif trainctrl.testBenchState == 1:  # close test bench
            trainctrl.testBenchState = 0
            self.setFixedWidth(810)
            self.setFixedHeight(545)
            self.testBench.setText("Open Test Bench")

    def automodeswitcher(self):
        if trainctrl.mode == 1:  # train running in manual mode
            trainctrl.modeswitch()  # put train into auto mode
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
        if trainctrl.mode == 0:  # train running in auto mode
            trainctrl.modeswitch()  # put train into manual mode
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
        trainctrl.setcurrspeed = self.actSpeedTB.value()
        self.currSpeed.setText(str(trainctrl.currSpeed))

    def changecmdspeed(self):
        trainctrl.cmdSpeed = self.cmdSpeedTB.value()

    def changespeedlim(self):
        trainctrl.speedLim = self.speedLimTB.value()
        self.speedLim.setText(str(trainctrl.speedLim))

    def changevitalauth(self):
        trainctrl.vitalAuth = self.vitalAuthTB.value()

    def changeaccellim(self):
        trainctrl.accelLim = self.accelLimTB.value()

    def changedecellim(self):
        trainctrl.decelLim = self.decelLimTB.value()

    def passebrake(self):

        trainctrl.passebrakecontrol()
        self.refreshengine()
        if trainctrl.passEBrake == 0:
            self.passEBrakeTB.setText("Off")
        elif trainctrl.passEBrake() == 1:
            self.passEBrakeTB.setText("On")
            self.setPtSpeed.setValue(trainctrl.setPtSpeed)

    def trackstate(self):
        trainctrl.circuitpolaritycontrol()
        if trainctrl.circuitPolarity() == 0:  # track is negative polarity
            self.trackStateTB.setText("-")
        elif trainctrl.circuitPolarity() == 1:  # track is positive polarity
            self.trackStateTB.setText("+")

    def signalfail(self):
        trainctrl.signalfailcontrol()
        if trainctrl.signalFail == 0:  # no signal pickup failure
            self.failSigPickupTB.setText("Off")
            self.signalFail.setChecked(trainctrl.signalFail)   # should be false
        elif trainctrl.signalFail == 1:  # signal pickup failure
            self.failSigPickupTB.setText("On")
            self.signalFail.setChecked(trainctrl.signalFail)  # should be true
            trainctrl.failhandler()
            self.refreshengine()

    def enginefail(self):
        trainctrl.enginefailcontrol()
        if trainctrl.engineFail == 0:  # no signal pickup failure
            self.failEngineTB.setText("Off")
            self.engineFail.setChecked(trainctrl.engineFail)  # should be false
        elif trainctrl.engineFail == 1:  # signal pickup failure
            self.failEngineTB.setText("On")
            self.engineFail.setChecked(trainctrl.engineFail)  # should be true
            trainctrl.failhandler()
            self.refreshengine()

    def brakefail(self):
        trainctrl.brakefailcontrol()
        if trainctrl.brakeFail == 0:  # no signal pickup failure
            self.failBrakeTB.setText("Off")
            self.brakeFail.setChecked(trainctrl.brakeFail())  # should be false
        elif trainctrl.brakeFail == 1:  # signal pickup failure
            self.failBrakeTB.setText("On")
            self.brakeFail.setChecked(trainctrl.brakeFail)  # should be true
            trainctrl.failhandler()
            self.refreshengine()

    def doorleft(self):
        if trainctrl.doorSide == 0:
            trainctrl.doorSide = 1
            self.doorsLeft.setChecked(1)
        elif trainctrl.doorSide == 1:
            trainctrl.doorSide = 0
            self.doorsLeft.setChecked(0)
        elif trainctrl.doorSide == 2:
            trainctrl.doorSide = 3
            self.doorsLeft.setChecked(1)
        elif trainctrl.doorSide == 3:
            trainctrl.doorSide = 2
            self.doorsLeft.setChecked(0)

    def doorright(self):
        if trainctrl.doorSide == 0:
            trainctrl.doorSide = 2
            self.doorsRight.setChecked(1)
        elif trainctrl.doorSide == 1:
            trainctrl.doorSide = 3
            self.doorsRight.setChecked(1)
        elif trainctrl.doorSide == 2:
            trainctrl.doorSide = 0
            self.doorsRight.setChecked(0)
        elif trainctrl.doorSide == 3:
            trainctrl.doorSide = 1
            self.doorsRight.setChecked(0)

    def beaconupdate(self):
        trainctrl.parsebeacon(str(self.beaconTB.toPlainText()))

    def changeextlights(self):
        trainctrl.extlightscontrol()

    def changeintlights(self):
        trainctrl.intlightscontrol()

    def tempcontrol(self):
        trainctrl.tempcontrol(self.temp.value())

    def doors(self):
        if self.doorsLeft.isChecked() and not self.doorsRight.isChecked():
            trainctrl.doorSide = 1
        elif not self.doorsLeft.isChecked() and self.doorsRight.isChecked():
            trainctrl.doorSide = 2
        elif self.doorsLeft.isChecked() and self.doorsRight.isChecked():
            trainctrl.doorSide = 3
        else:
            trainctrl.doorSide = 0

        trainctrl.doorcontrol()

        if trainctrl.doorState == 1:  # doors open
            self.doorControl.setText("Opened")
            self.testLabel.setText(f'door state is {trainctrl.doorState}')
            self.doorLabel.setText(f'doors open and left is {trainctrl.doorL} '
                                   f'and right is {trainctrl.doorR}')
            self.testLabel.adjustSize()
            self.doorLabel.adjustSize()
        elif trainctrl.doorState == 0:  # doors closed
            self.doorControl.setText("Closed")
            self.testLabel.setText(f'door state is {trainctrl.doorState}')
            self.doorLabel.setText(f'doors closed and left is {trainctrl.doorL} '
                                   f'and right is {trainctrl.doorR}')
            self.testLabel.adjustSize()
            self.doorLabel.adjustSize()

    def ebrake(self):
        trainctrl.ebrakecontrol()
        if trainctrl.eBrake == 0:
            self.eBrake.setText("EMERGENCY BRAKE: OFF")
            self.testLabel.setText(f'ebrake off and {trainctrl.eBrake}')
            self.testLabel.adjustSize()
            self.refreshengine()
        elif trainctrl.eBrake == 1:
            self.eBrake.setText("EMERGENCY BRAKE: ON")
            self.testLabel.setText(f'ebrake off and {trainctrl.eBrake}')
            self.testLabel.adjustSize()
            self.setPtSpeed.setValue(trainctrl.setPtSpeed)
            self.refreshengine()

    def speedupdate(self):
        if trainctrl.eBrake() == 0 and trainctrl.passEBrake == 0:
            trainctrl.setsetptspeed((self.setPtSpeed.value()))
            self.refreshengine()
        elif trainctrl.eBrake() == 1 or trainctrl.passEBrake == 1:
            self.setPtSpeed.setValue(0)

    def changekp(self):
        trainctrl.kp = self.kp.value()
        self.refreshengine()

    def changeki(self):
        trainctrl.ki = self.ki.value()
        self.refreshengine()

    def useservicebrake(self):
        if trainctrl.servBrake == 0:
            trainctrl.setservbrake(1)
            self.servBrake.setText("Service Brake: On")
            self.refreshengine()
        elif trainctrl.servBrake == 1:
            trainctrl.setservbrake(0)
            self.servBrake.setText("Service Brake: Off")
            self.refreshengine()

    def refreshengine(self):
        self.setPtSpeed.setValue(int(trainctrl.setPtSpeed))
        self.speedLim.setText(str(trainctrl.speedLim))
        self.currSpeed.setText(str(int(trainctrl.currSpeed)))
        self.power.setText(str(trainctrl.power))
        self.kp.setValue(int(trainctrl.kp))
        self.ki.setValue(int(trainctrl.ki))

    def powerrefresh(self):
        for i in range(0, 23):
            self.setPtSpeed.setValue(int(trainctrl.setPtSpeed))
            self.speedLim.setText(str(trainctrl.speedLim))
            self.currSpeed.setText(str(int(trainctrl.currSpeed)))
            self.power.setText(str(trainctrl.power))
            self.kp.setValue(int(trainctrl.kp))
            self.ki.setValue(int(trainctrl.ki))
            print(i)
            time.sleep(5)

    # TODO setpt speed from driver, service brake, power calcs, speed calcs and checks, beacon


# initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec()
