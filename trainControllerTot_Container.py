# container class for calling everything from train
import sys
import numpy

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSlot, pyqtSignal

from Train_Controller_SW.trainControllerSWContainer import TrainControllerSWContainer
from Train_Controller_HW.trainControllerHWContainer import TrainControler_HW_Container


class TrainController_Tot_Container:

    # Signals
    new_train_values_signal = pyqtSignal(list, int)
    new_train_temp_signal = pyqtSignal(float, int)
    # sam connect these signals to your respective update train model values command

    def __init__(self, ware=True):
        # Ware:
        # False: HW
        # True:  SW
        if ware:
            self.trainCtrl = TrainControllerSWContainer()
        else:
            self.trainCtrl = TrainControler_HW_Container()

    def show_ui(self):
        self.trainCtrl.show_ui()

    #  receiver functions
    def getvaluesfromtrain(self, inputs):  # Sam call this to update traincontroller values

        self.trainCtrl.updatevalues(inputs)

        # send signal with updated values
        self.new_train_values_signal.emit(self.trainCtrl.outputs, 1)
        self.new_train_temp_signal.emit(self.trainCtrl.cabin_temp, 1)

        return

    # TrainModel
    # def updatevalues(self, inputs):
    #     # [actual speed, authority, received speed, pbrake, track circuit, underground, beacon]
    #     return self.trainCtrl.updatevalues(inputs)


def TrainC_main():
    trainctrlcntr = TrainController_Tot_Container()
    trainctrlcntr.show_ui()


if __name__ == "__main__":
    TrainC_main()
