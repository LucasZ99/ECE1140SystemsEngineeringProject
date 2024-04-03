# container class for calling everything from train
import sys
import numpy

from PyQt6.QtWidgets import QApplication

from Train_Controller_SW.trainControllerSWContainer import TrainControllerSWContainer
from Train_Controller_HW.trainControllerHWContainer import TrainControler_HW_Container


class TrainController_Tot_Container:
    def __init__(self,Ware = True):
        # Ware:
        # False: HW
        # True:  SW
        if Ware: self.trainCtrl = TrainControllerSWContainer()
        else: self.trainCtrl = TrainControler_HW_Container()

    def show_ui(self):
        self.trainCtrl.show_ui()

    #  receiver functions

    #TrainModel
    def updatevalues(self, inputs):
        return self.trainCtrl.updatevalues(inputs)

def TrainC_main():
    trainctrlcntr = TrainController_Tot_Container()
    trainctrlcntr.show_ui()


if __name__ == "__main__":
    TrainC_main()
