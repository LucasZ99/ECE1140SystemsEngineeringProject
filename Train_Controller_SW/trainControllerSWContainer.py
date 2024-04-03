# container class for calling everything from train
import sys
import threading

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, pyqtSlot

from Train_Controller_SW import trainControllerSW
from Train_Controller_SW.trainControllerSWUI import UI


class TrainControllerSWContainer:

    # Signals
    new_train_values_signal = pyqtSignal(dict, int)
    new_train_temp_signal = pyqtSignal(float, int)

    def __init__(self):
        self.trainCtrl = trainControllerSW.TrainController()


        # actions for automatic mode launch
        # threading.Thread(target=self.trainCtrl.automode).start()  # uncomment this to see how auto mode will start
        # threading.Thread(target=self.powerrefresh).start()

    def show_ui(self):
        app = QApplication.instance()

        if app is None:
            app = QApplication([])

        self.ui = UI(self.trainCtrl)

        self.ui.show()  # this unresolved reference is fine
        # self.ui.refreshengine()

        app.exec()

    # sender functions
    def sendvaluetotrain(self, outputs, index):
        self.new_train_values_signal.emit(outputs, 1)

    def sendtemp(self, cabintemp):
        self.new_train_temp_signal.emit(cabintemp, 1)

    # receiver functions

    #  end point for train sending new values
    def getvaluesfromtrain(self, inputs):

        self.actspeedfromtrain(inputs[0])
        self.cmdspeedfromtrain(inputs[1])
        self.authorityfromtrain(inputs[2])
        self.passebrakefromtrain(inputs[3])
        self.polarityfromtrain(inputs[4])
        self.undergroundfromtrain(inputs[5])
        self.beaconfromtrain(inputs[6])

        # do values calculations
        # blah blah blah

        # send signal with updated values
        # self.new_train_valeues_signal.emit(outputs, 1)
        # self.new_train_temp_signal.emit(cabintemp, 1)

        return

    def actspeedfromtrain(self, newspeed):
        self.trainCtrl.actualSpeed = newspeed
        # self.trainCtrl.powercontrol
        return

    def cmdspeedfromtrain(self, newcmdspd):
        pass

    def authorityfromtrain(self, auth):
        pass

    def passebrakefromtrain(self, newpassbrake):
        pass

    def polarityfromtrain(self, newpolarity):
        pass

    def doorsidefromtrain(self, newdoor):
        pass

    def undergroundfromtrain(self, newunder):
        pass

    def beaconfromtrain(self, newbeacon):
        pass


def main():
    trainctrlcntr = TrainControllerSWContainer()
    trainctrlcntr.show_ui()


if __name__ == "__main__":
    main()
