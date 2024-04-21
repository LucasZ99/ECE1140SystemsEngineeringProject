import PyQt6.QtGui as QtGui
import threading
import time
import os

from PyQt6.QtWidgets import *
import sys
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSlot, pyqtSignal, QObject
from PyQt6.QtWidgets import QComboBox


# class ComboBox(QComboBox):
#     clicked = pyqtSignal()

    # def showPopup(self):
    #     self.clicked.emit()
    #     super(ComboBox, self).showPopup()


class UI(QMainWindow):

    closed = pyqtSignal(bool)
    comboClicked = pyqtSignal()
    new_ctrl_list = pyqtSignal()

    def __init__(self, ctrl_list):
        super(UI, self).__init__()

        # create train object
        self.ctrl_list = ctrl_list
        # self.trainctrl = self.ctrl_list[1]  # like this i think i hope, inits with first train ctrl in list

        self.trainctrl = self.ctrl_list  # for testing w self module

        # TODO update values function when trainctrl is changed in drop down list

        # took from lucas (Track_Controller_SW/TrackController.UI), thank you Lucas
        current_dir = os.path.dirname(__file__)
        ui_path = os.path.join(current_dir, "trainControllerSW_UI.ui")
        try:
            loadUi(ui_path, self)
        except Exception as e:
            print("train controller sw ui.py: Error with loading ui file: ", e)

        # self.trains_list = ComboBox(self)

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
        self.speedLim.setText(str(int(self.ms_to_mph(self.trainctrl.speedlim))))
        self.temp.setValue(int(self.trainctrl.cabinTemp))
        self.kp.setValue(int(self.trainctrl.kp))
        self.ki.setValue(int(self.trainctrl.ki))
        self.currSpeed.setText(str(self.ms_to_mph(self.trainctrl.actualSpeed)))
        self.power.setText(f'{self.trainctrl.power}')
        self.setPtSpeed.setValue(int(self.ms_to_mph(self.trainctrl.setPtSpeed)))
        self.speedLimTB.setValue(int(self.ms_to_mph(self.trainctrl.speedlim)))
        #self.train_list.addItems(ctrl_list)

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
        # self.trains_list.clicked.connect(self.addtrain)  # TODO: combobox clicked function WHAT IS IT pls i need this to work

        # show the app
        self.show()

    def closeEvent(self, event):
        print("train controller sw ui.py: hi")
        self.closed.emit(False)
        print("train controller sw ui.py: bye")

    # def showPopup(self):
    #     self.comboClicked.emit()

    def hello(self, value):
        if not value:
            print("train controller sw ui.py: hi!")
        elif value:
            print("train controller sw ui.py: bye")

    # define procedures

    def testingbench(self):
        if self.trainctrl.testBenchState == 0:  # open test bench
            self.trainctrl.testbenchcontrol()
            self.setFixedWidth(1197)
            self.setFixedHeight(733)
            self.testBench.setText("Close Test Bench")
            print("train controller sw ui.py: test bench opened")
        elif self.trainctrl.testBenchState == 1:  # close test bench
            self.trainctrl.testbenchcontrol()
            self.setFixedWidth(810)
            self.setFixedHeight(545)
            self.testBench.setText("Open Test Bench")
            print("train controller sw ui.py: test bench closed")

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
        self.trainctrl.actualspeed = self.actSpeedTB.value()
        self.currSpeed.setText(str(self.trainctrl.actualSpeed))

        # TODO make it so change on enter (maybe just to text box)

    def changecmdspeed(self):
        self.trainctrl.cmdSpeed = self.mph_to_ms(self.cmdSpeedTB.value())

        self.trainctrl.speedcheck()
        self.trainctrl.authority()
        print("trian controller sw ui.py: authority updated after cmdspeed change in testbench")
        self.trainctrl.powercontrol()
        print("trian controller sw ui.py: power updated after cmdspeed change in testbench")
        print()

    def changevitalauth(self):
        self.trainctrl.vitalAuth = self.vitalAuthTB.value()

        self.trainctrl.authority()
        print("trian controller sw ui.py: authority updated after authority change in testbench")
        self.trainctrl.powercontrol()
        print("trian controller sw ui.py: power updated after authority change in testbench")
        print()

    def changespeedlim(self):
        self.trainctrl.speedlim = self.speedLimTB.value()
        self.speedLim.setText(str(self.trainctrl.speedlim))

    # I can probably get rid of accel and decel lim edits since they are static data and never updated.
    def changeaccellim(self):
        self.trainctrl.accelLim = self.accelLimTB.value()

    def changedecellim(self):
        self.trainctrl.decelLim = self.decelLimTB.value()

    def passebrake(self):
        self.trainctrl.ui_ebrakecontrol()
        self.refreshengine()
        print("train controller sw ui.py: refreshed engine")
        print(f'train controller sw ui.py: ebrake now is {self.trainctrl.eBrake}')
        if self.trainctrl.eBrake == 1:
            print("train controller sw ui.py: e brake on")
            self.passEBrakeTB.setText("On")
        elif self.trainctrl.eBrake == 0:
            print("train controller sw ui.py: e brake off")
            self.passEBrakeTB.setText("Off")
            self.setPtSpeed.setValue(int(self.trainctrl.setPtSpeed))

    def trackstate(self):

        newpolarity = not self.trainctrl.polarity

        self.trainctrl.polaritycontrol(newpolarity)
        if self.trainctrl.polarity == 0:  # track is negative polarity
            self.trackStateTB.setText("-")
        elif self.trainctrl.polarity == 1:  # track is positive polarity
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
            self.brakeFail.setChecked(self.trainctrl.brakeFail)  # should be false
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
        self.trainctrl.ui_ebrakecontrol()
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
        self.setPtSpeed.setValue(int(self.ms_to_mph(self.trainctrl.setPtSpeed)))
        self.speedLim.setText(str(int(self.ms_to_mph(self.trainctrl.speedlim))))
        self.currSpeed.setText(str(self.ms_to_mph(self.trainctrl.actualSpeed)))
        self.power.setText(str(self.watt_to_hp(self.trainctrl.power)))
        self.kp.setValue(int(self.trainctrl.kp))
        self.ki.setValue(int(self.trainctrl.ki))

    # def powerrefresh(self):
    #     for i in range(0, 23):
    #         self.setPtSpeed.setValue(int(self.trainctrl.setPtSpeed))
    #         self.speedLim.setText(str(self.trainctrl.speedLim))
    #         self.currSpeed.setText(str(int(self.trainctrl.currSpeed)))
    #         self.power.setText(str(self.trainctrl.power))
    #         self.kp.setValue(int(self.trainctrl.kp))
    #         self.ki.setValue(int(self.trainctrl.ki))
    #         print(i)
    #         time.sleep(5)

    #def addtrain(self, ctrl_list):
    def addtrain(self): # , ctrl_list):
        print("train contrller sw ui.py: clicked train select")
        self.trains_list.clear()

        print("1 train controller sw ui.py: sending new_ctrl_list signal to sw container")
        self.update_ctrl_list(self.new_ctrl_list.emit())
        print("4 train controller sw ui.py all signals received")
        #print(
        #self.ctrl_list = ctrl_list  # how does this update when new ctrl is added in container..
        # probably gonna have to use a signal for ^^, looking into it
        self.trains_list.addItems(self.ctrl_list)

    def update_ctrl_list(self, new_ctrl_list):
        print("3 train controller sw ui.py: received new_ctrl_list_to_ui signal from container")
        self.ctrl_list = new_ctrl_list

    def mph_to_ms(self, value):
        return value / 2.2237

    def ms_to_mph(self, value):
        return value * 2.237

    def watt_to_hp(self, value):
        return value / 745.7

    def hp_to_watt(self, value):
        return value * 745.7

def main():
    # initialize the app
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()


if __name__ == '__main__':
    main()


