# container class for calling everything from train
import sys
import threading

from PyQt6.QtWidgets import QApplication

from SystemTime import SystemTime
from Train_Controller_SW import trainControllerSW
from Train_Controller_SW.trainControllerSWUI import UI
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject


class TrainControllerSWContainer:

    new_ctrl_list_to_ui = pyqtSignal(list)

    def __init__(self):
        self.system_time = SystemTime.time()
        self.trainCtrl = trainControllerSW.TrainController()  #self.system_time)
        self.train_model_update = list()
        self.cabin_temp = 68

        # ******** SELF MODULE TESTING ********
        # self.trainCtrl1 = trainControllerSW.TrainController()
        # self.trainCtrl2 = trainControllerSW.TrainController()
        # self.trainCtrl3 = trainControllerSW.TrainController()
        # self.trainCtrl4 = trainControllerSW.TrainController()
        # self.control_list = [self.trainCtrl1, self.trainCtrl2, self.trainCtrl3, self.trainCtrl4]

        print("train controller sw container.py: making sw ui")
        app = QApplication.instance()

        if app is None:
            app = QApplication([])

        self.swUI = UI(self.trainCtrl)
        print("train controller sw container.py: made sw ui")
        # actions for automatic mode launch
        # threading.Thread(target=self.trainCtrl.automode).start()  # uncomment this to see how auto mode will start
        # threading.Thread(target=self.powerrefresh).start()

    def show_ui(self):
        app = QApplication.instance()

        # if app is None:
        app = QApplication([])

        self.swUI = UI(self.trainCtrl)
        self.swUI.closed.connect(self.sw_ui_state)  # comment this out for full integration (signal should go to tot cntnr)

        # ui = UI(self.trainCtrl)
        # ui.new_ctrl_list.connect(self.send_new_ctrl_list)

        self.swUI.show()
        # ui.show()
        # self.ui.refreshengine()

        app.exec()

    def send_new_ctrl_list(self):
        print("2 train controller sw container.py: new_ctrl_list signal recieved from ui")
        return self.control_list

    def sw_ui_state(self, value):
        print("train controller sw container.py: made it!")
        print(f'train controller sw container.py: software ui state is: {value}')

    # receiver functions
    def updatevalues(self, inputs, num=0):
        print("train controller sw container.py: updating train values")
        print(num)
        if num == 0:
            self.train_model_update = self.trainCtrl.old_updater(inputs)
        elif num < 1 and num > 3:
            print("train controller sw container.py: update type out of range")
        else:
            self.train_model_update = self.trainCtrl.updater(inputs, num)

        # update values, perform all new calcs, and send back list of new values
        # self.outputs = self.trainCtrl.updater(inputs)
        self.cabin_temp = self.trainCtrl.getcabintemp()

        return

    def update_train_controller_from_train_model(self, authority_safe_speed, track_info, train_info):
        print("train controller sw container.py: updating train controller from train model")

        # probably gonna split the updater into 3 separate functions in the future but this should work fine for now
        self.trainCtrl.updater(authority_safe_speed, 1)
        print("train controller sw container.py: authority safe speed updated")
        self.trainCtrl.updater(track_info, 2)
        print("train controller sw container.py: track info updated")
        self.trainCtrl.updater(train_info, 3)
        print("train controller sw container.py: train info updated")

        self.train_model_update = self.trainCtrl.update_train_model_from_train_controller()
        print("train controller sw container.py: updated train model update list!")

        print("train controller sw container.py: sending values from train controller to train model")
        return self.train_model_update


def main():
    # system_time = SystemTimeContainer()
    trainctrlcntr = TrainControllerSWContainer()  # system_time)
    trainctrlcntr.show_ui()


if __name__ == "__main__":
    main()
