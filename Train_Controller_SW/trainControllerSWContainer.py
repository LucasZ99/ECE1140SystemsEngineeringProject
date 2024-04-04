# container class for calling everything from train
import sys
import threading

from PyQt6.QtWidgets import QApplication

from SystemTime import SystemTimeContainer
from Train_Controller_SW import trainControllerSW
from Train_Controller_SW.trainControllerSWUI import UI


class TrainControllerSWContainer:

    def __init__(self, system_time_container: SystemTimeContainer):
        self.system_time = system_time_container.system_time
        self.trainCtrl = trainControllerSW.TrainController(self.system_time)
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
    def updatevalues(self, inputs, num=0):
        print(num)
        if num == 0:
            self.trainCtrl.old_updater(inputs)
        elif num < 1 and num > 3:
            print("update type out of range")
        else:
            self.trainCtrl.updater(inputs, num)

        # update values, perform all new calcs, and send back list of new values
        self.outputs = self.trainCtrl.updater(inputs)
        self.cabin_temp = self.trainCtrl.getcabintemp()

        return


def main():
    trainctrlcntr = TrainControllerSWContainer()
    trainctrlcntr.show_ui()


if __name__ == "__main__":
    main()
