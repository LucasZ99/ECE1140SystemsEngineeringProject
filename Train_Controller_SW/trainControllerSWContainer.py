# container class for calling everything from train
import sys
import threading

from PyQt6.QtWidgets import QApplication

from Train_Controller_SW import trainControllerSW
from Train_Controller_SW.trainControllerSWUI import UI


class Container:
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

        self.ui.show()
        # self.ui.refreshengine()

        app.exec()

    #  receiver functions

    def updatevalues(self, inputs):

        self.actspeedfromtrain(inputs[0])
        self.cmdspeedfromtrain(inputs[1])
        self.authorityfromtrain(inputs[2])
        self.passebrakefromtrain(inputs[3])
        self.polarityfromtrain(inputs[4])
        self.doorsidefromtrain(inputs[5])
        self.undergroundfromtrain(inputs[6])
        self.beaconfromtrain(inputs[7])

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
    trainctrlcntr = Container()
    trainctrlcntr.show_ui()


if __name__ == "__main__":
    main()
