import PyQt6.QtGui as QtGui
import threading
import time
import os

from PyQt6.QtWidgets import *
import sys
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSlot, pyqtSignal, QObject
from PyQt6.QtGui import QFont


# class ComboBox(QComboBox):
#     clicked = pyqtSignal()

    # def showPopup(self):
    #     self.clicked.emit()
    #     super(ComboBox, self).showPopup()


class UI(QMainWindow):

    closed = pyqtSignal(bool)
    comboClicked = pyqtSignal()
    new_ctrl_list = pyqtSignal()

    # signals for backend communication
    trainnum_to_container = pyqtSignal()

    automode_to_controller = pyqtSignal()
    manualmode_to_controller = pyqtSignal()

    extlights_to_controller = pyqtSignal()
    intlights_to_controller = pyqtSignal()
    cabintemp_to_controller = pyqtSignal()
    dooropen_to_controller = pyqtSignal()

    kp_to_controller = pyqtSignal()
    ki_to_controller = pyqtSignal()
    setspeed_to_controller = pyqtSignal()
    servicebrake_to_controller = pyqtSignal()
    ebrake_to_controller = pyqtSignal()

    # from testbench
    TB_actspeed_to_controller = pyqtSignal()
    TB_cmdspeed_to_controller = pyqtSignal()
    TB_authority_to_controller = pyqtSignal()
    TB_passebrake_to_controller = pyqtSignal()
    TB_polarity_to_controller = pyqtSignal()

    TB_signalfail_to_controller = pyqtSignal()
    TB_enginefail_to_controller = pyqtSignal()
    TB_brakefail_to_controller = pyqtSignal()

    TB_doorside_to_controller = pyqtSignal()

    TB_beacon_to_controller = pyqtSignal()

    def __init__(self, ctrl_list):
        super(UI, self).__init__()

        # create train object
        self.ctrl_list = ctrl_list

        if type(ctrl_list) is not list:
            self.trainctrl = self.ctrl_list  # for testing w self module
        else:
            self.trainctrl = self.ctrl_list[1]  # like this i think i hope, inits with first train ctrl in list

        # TODO update values function when trainctrl is changed in drop down list

        # took from lucas (Track_Controller_SW/TrackController.UI), thank you
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
        self.autoMode.setFont(QFont('MS Shell Dlg 2', 8))
        self.manualMode.setFont(QFont('MS Shell Dlg 2', 8))

        self.extLights.setEnabled(False)
        self.intLights.setEnabled(False)
        self.temp.setEnabled(False)
        self.doorControl.setEnabled(False)
        self.kp.setEnabled(False)
        self.ki.setEnabled(False)
        self.setPtSpeed.setEnabled(False)
        self.servBrake.setEnabled(False)
        self.ambientLight.setHidden(True)

        self.testLabel.setHidden(True)
        self.doorLabel.setHidden(True)
        self.failSigPickupInputL.setHidden(True)
        self.failSigPickupTB.setHidden(True)
        self.failEngineInputL.setHidden(True)
        self.failEngineTB.setHidden(True)
        self.failBrakeInputL.setHidden(True)
        self.failBrakeTB.setHidden(True)

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
        self.speedLimTB.setValue(int(self.trainctrl.speedlim))

        j = 1
        if type(self.ctrl_list) is not list:
            self.trains_list.addItem(str(j))
        else:
            for i in self.ctrl_list:
                j += 1
                self.trains_list.addItem(str(j))

        # TODO make connections
        self.testBench.clicked.connect(self.testingbench)
        self.actSpeedTB.valueChanged.connect(self.changecurrspeed)
        self.cmdSpeedTB.valueChanged.connect(self.changecmdspeed)
        self.speedLimTB.valueChanged.connect(self.changespeedlim)
        self.vitalAuthTB.valueChanged.connect(self.changevitalauth)

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
        self.updateTB.clicked.connect(self.update_train_model_values)
        # self.trains_list.clicked.connect(self.addtrain)

        # external connections

        # show the app
        # self.show()

    def closeEvent(self, event):
        print("train controller sw ui.py: ui opened")
        self.closed.emit(False)
        print("train controller sw ui.py: ui closed")

    # define procedures

    def update_train_model_values(self):

        type1 = [0, 0]  # type1: [authority, cmd speed]
        type2 = [False, False, 0]  # type2: [polarity, underground, beacon]
        type3 = [0, False]  # type3: [actual speed, passenger e-brake]

        type1_list = str(self.type1.text()).split(", ", -1)
        if type1_list == [""]:
            type1[0] = None
            type1[1] = None
        else:
            type1[0] = float(type1_list[0])
            type1[1] = int(type1_list[1])
        print()
        self.trainctrl.updater(type1, 1)
        print()
        print("train controller sw ui.py: type 1 values updated")
        print()

        type2_list = str(self.type2.text()).split(", ", -1)
        if type2_list[0] == "True" or type2_list[0] == "true" or type2_list[0] == "T" or type2_list[0] == "t":
            type2[0] = True
        elif type2_list[0] == "False" or type2_list[0] == "false" or type2_list[0] == "F" or type2_list[0] == "f":
            type2[0] = False

        if type2_list[1] == "True" or type2_list[1] == "true" or type2_list[1] == "T" or type2_list[1] == "t":
            type2[1] = True
        elif type2_list[1] == "False" or type2_list[1] == "false" or type2_list[1] == "F" or type2_list[1] == "f":
            type2[1] = False

        # type2[1] = type2_list[1]
        type2[2] = str(self.beaconTB.text())
        self.trainctrl.updater(type2, 2)
        print()
        print("train controller sw ui.py: type 2 values updated")
        print()

        type3_list = str(self.type3.text()).split(", ", -1)
        type3[0] = float(type3_list[0])

        if type3_list[1] == "True" or type3_list[1] == "true" or type3_list[1] == "T" or type3_list[1] == "t":
            type3[1] = True
        elif type3_list[1] == "False" or type3_list[1] == "false" or type3_list[1] == "F" or type3_list[1] == "f":
            type3[1] = False

        self.trainctrl.updater(type3, 3)
        print()
        print("train controller sw ui.py: type 3 values updated")
        print()

        self.update_this_ui()

        print()
        print(f'outputs to train model: {self.trainctrl.update_train_model_from_train_controller()}')
        print()

    def update_this_ui(self):
        self.extLights.setValue(int(self.trainctrl.extLights))
        self.intLights.setValue(int(self.trainctrl.intLights))
        self.temp.setValue(int(self.trainctrl.cabinTemp))

        if self.trainctrl.atStation:
            self.stationName.setText(str(self.trainctrl.station))
        else:
            self.stationName.setText("")

        if self.trainctrl.doorSide == 1:
            self.doorsLeft.setChecked(True)
            self.doorsRight.setChecked(False)
        elif self.trainctrl.doorSide == 2:
            self.doorsLeft.setChecked(False)
            self.doorsRight.setChecked(True)
        elif self.trainctrl.doorSide == 3:
            self.doorsLeft.setChecked(True)
            self.doorsRight.setChecked(True)
        else:
            self.doorsLeft.setChecked(False)
            self.doorsRight.setChecked(False)

        self.speedLim.setText(str(int(self.ms_to_mph(self.trainctrl.speedlim))))

        self.currSpeed.setText(str(int(self.ms_to_mph(self.trainctrl.actualSpeed))))

        if self.trainctrl.cmdSpeed is not None:
            self.setPtSpeed.setValue(int(self.ms_to_mph(self.trainctrl.cmdSpeed)))
        else:
            self.setPtSpeed.setValue(0)

        self.power.setText(str(int(self.watt_to_hp(self.trainctrl.power))))

        if self.trainctrl.servBrake:
            self.servBrake.setText("Service Brake: ON")
        elif not self.trainctrl.servBrake:
            self.servBrake.setText("Service Brake: OFF")

        if self.trainctrl.eBrake:
            self.eBrake.setText("EMERGENCY BRAKE: ON")
        elif not self.trainctrl.eBrake:
            self.eBrake.setText("EMERGENCY BRAKE: OFF")

        if self.trainctrl.mode and self.trainctrl.actualSpeed == 0:
            self.doorControl.setEnabled(True)
        else:
            self.doorControl.setEnabled(False)

        self.ambientLight.setHidden(not self.trainctrl.isUnderground)

    def testingbench(self):
        if self.trainctrl.testBenchState == 0:  # open test bench
            self.trainctrl.testbenchcontrol()
            self.setFixedWidth(1197)
            # self.setFixedHeight(733)
            self.setFixedHeight(625)
            self.testBench.setText("Close Test Bench")
            # print("train controller sw ui.py: test bench opened")
        elif self.trainctrl.testBenchState == 1:  # close test bench
            self.trainctrl.testbenchcontrol()
            self.setFixedWidth(810)
            self.setFixedHeight(545)
            self.testBench.setText("Open Test Bench")
            # print("train controller sw ui.py: test bench closed")

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

            if self.trainctrl.mode and self.trainctrl.actualSpeed == 0:
                self.doorControl.setEnabled(True)
            else:
                self.doorControl.setEnabled(False)

            self.kp.setEnabled(True)
            self.ki.setEnabled(True)
            self.setPtSpeed.setEnabled(True)
            self.servBrake.setEnabled(True)
            self.inMode.setText("Manual Mode")
        return

    def changecurrspeed(self):
        self.trainctrl.setactspeed(float(self.actSpeedTB.value()))
        self.currSpeed.setText(str(round(self.ms_to_mph(self.trainctrl.actualSpeed), 2)))
        self.actSpeedTB.setValue(int(self.trainctrl.actualSpeed))

    def changecmdspeed(self):
        print(f'train controller sw ui.py: new commanded speed is {self.cmdSpeedTB.value()} mph')
        self.trainctrl.cmdSpeed = self.mph_to_ms(self.cmdSpeedTB.value())

        self.trainctrl.speedcheck()
        self.trainctrl.authority()
        print("train controller sw ui.py: authority updated after commanded speed change in testbench")
        self.trainctrl.powercontrol()
        print("train controller sw ui.py: power updated after commanded speed change in testbench")
        print()

    def changevitalauth(self):
        self.trainctrl.vitalAuth = self.vitalAuthTB.value()

        self.trainctrl.authority()
        print("train controller sw ui.py: authority updated after authority change in testbench")
        self.trainctrl.powercontrol()
        print("train controller sw ui.py: power updated after authority change in testbench")
        print()

    def changespeedlim(self):
        self.trainctrl.speedLim = self.speedLimTB.value()
        self.speedLim.setText(str(int(self.ms_to_mph(self.trainctrl.speedlim))))

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

        if self.trainctrl.atStation:
            self.stationName.setText(self.trainctrl.station)
        else:
            self.stationName.setText("")

        if self.trainctrl.doorSide == 1:
            self.doorsLeft.setChecked(True)
            self.doorsRight.setChecked(False)
        elif self.trainctrl.doorSide == 2:
            self.doorsLeft.setChecked(False)
            self.doorsRight.setChecked(True)
        elif self.trainctrl.doorSide == 3:
            self.doorsLeft.setChecked(True)
            self.doorsRight.setChecked(True)
        else:
            self.doorsLeft.setChecked(False)
            self.doorsRight.setChecked(False)

        self.update_this_ui()
        self.speedLimTB.setValue(int(self.trainctrl.speedlim))

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
        if self.trainctrl.isUnderground:
            self.extLights.setValue(1)
        else:
            if self.extLights.value() != self.trainctrl.extLights:
                self.trainctrl.extlightscontrol()

    def changeintlights(self):
        if self.trainctrl.isUnderground:
            self.intLights.setValue(1)
        else:
            if self.intLights.value() != self.trainctrl.intLights:
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
            #self.refreshengine()
        elif self.trainctrl.eBrake == 1:
            self.eBrake.setText("EMERGENCY BRAKE: ON")
            self.servBrake.setText("Service Brake: OFF")
            self.testLabel.setText(f'ebrake on and {self.trainctrl.eBrake}')
            self.testLabel.adjustSize()
            # self.setPtSpeed.setValue(self.trainctrl.setPtSpeed) # crashes here, probably because speed is undefined
            #self.refreshengine()

        self.update_this_ui()

    def speedupdate(self):
        if self.setPtSpeed.value() != int(self.ms_to_mph(self.trainctrl.cmdSpeed)):
            # print("value actually changed")
            self.trainctrl.cmdSpeed = self.mph_to_ms(self.setPtSpeed.value())
            self.trainctrl.vitalitycheck()
            self.trainctrl.powercontrol()
            self.update_this_ui()

    def changekp(self):
        self.trainctrl.kp = self.kp.value()
        print(f'new kp: {self.trainctrl.kp}')

    def changeki(self):
        self.trainctrl.ki = self.ki.value()
        print(f'new ki: {self.trainctrl.ki}')

    def useservicebrake(self):
        if not self.trainctrl.servBrake:
            self.trainctrl.servBrake = True
            self.servBrake.setText("Service Brake: On")
            self.trainctrl.sBrakeSetByDriver = True
        elif self.trainctrl.servBrake:
            self.trainctrl.servBrake = False
            self.servBrake.setText("Service Brake: Off")
            self.trainctrl.sBrakeSetByDriver = False

        self.trainctrl.vitalitycheck()
        self.trainctrl.powercontrol()
        self.update_this_ui()

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
    def addtrain(self):  # , ctrl_list):
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
