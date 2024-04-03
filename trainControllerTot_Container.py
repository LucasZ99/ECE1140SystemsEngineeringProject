# container class for calling everything from train
import sys
import numpy

from PyQt6.QtWidgets import QApplication

from Train_Controller_SW.trainControllerSWContainer import Container#TrainControler_SW_Container
from Train_Controller_HW.trainControllerHWContainer import TrainControler_HW_Container


class TrainControler_Tot_Container:
    def __init__(self,Ware=True):
        #Ware:
        #False: HW
        #True:  SW
        if Ware: self.trainCtrl = Container() #TrainControler_SW_Container()
        else: self.trainCtrl = TrainControler_HW_Container()

    def show_ui(self):
        self.trainCtrl.show_ui()

    #  receiver functions

    #TrainModel
    def updatevalues(self, inputs):
        # [actual speed, authority, received speed, pbrake, track circuit, underground, beacon]
        return self.trainCtrl.updatevalues(inputs)

def TrainC_main():
    trainctrlcntr = TrainControler_Tot_Container()
    trainctrlcntr.show_ui()


if __name__ == "__main__":
    TrainC_main()
9