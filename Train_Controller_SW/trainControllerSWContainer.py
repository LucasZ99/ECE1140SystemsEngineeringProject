# container class for calling everything from train
import sys
import threading

from PyQt6.QtWidgets import QApplication

from Train_Controller_SW import trainControllerSW
from Train_Controller_SW.trainControllerSWUI import UI


class TrainControllerSWContainer:

    def __init__(self):
        self.trainCtrl = trainControllerSW.TrainController()
        self.outputs = list()
        self.cabin_temp = 68
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

    # receiver functions

    #  end point for train sending new values
    def updatevalues(self, inputs):

        # update values, perform all new calcs, and send back list of new values
        self.outputs = self.trainCtrl.updater(inputs)
        self.cabin_temp = self.trainCtrl.getcabintemp()

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
