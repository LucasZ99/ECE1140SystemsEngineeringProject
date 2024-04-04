# container class for calling everything from train
import sys
import numpy

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSlot, pyqtSignal, QObject

from Train_Controller_SW.trainControllerSWContainer import TrainControllerSWContainer
from Train_Controller_HW.trainControllerHWContainer import TrainControler_HW_Container
from SystemTime import SystemTimeContainer


class TrainController_Tot_Container(QObject):

    # Signals
    new_train_values_signal = pyqtSignal(list, int)
    new_train_temp_signal = pyqtSignal(float, int)
    # sam connect these signals to your respective update train model values command

    def __init__(self, system_time_container: SystemTimeContainer, ware: bool=True):

        super().__init__()
        # Ware:
        # False: HW
        # True:  SW
        self.Ware = ware
        self.system_time = system_time_container
        if ware:
            self.trainCtrl = TrainControllerSWContainer(self.system_time)
        else:
            self.trainCtrl = TrainControler_HW_Container(self.system_time)

    def show_ui(self):
        self.trainCtrl.show_ui()

    #  receiver functions
    #Auth, Cmd_Spd
    def getvaluesfromtrain_update1(self, inputs):  # Sam call this to update traincontroller values

        self.trainCtrl.updatevalues(inputs,1)

        print("Train Controller TOT Container, type1: values updated, sending signals next")

        # send signal with updated values
        self.new_train_values_signal.emit(self.trainCtrl.outputs, 1)
        self.new_train_temp_signal.emit(self.trainCtrl.cabin_temp, 1)

        return

    #Track_Cicuit, Aboveground, beacon
    def getvaluesfromtrain_update2(self, inputs):  # Sam call this to update traincontroller values

        self.trainCtrl.updatevalues(inputs,2)

        print("Train Controller TOT Container, type2: values updated, sending signals next")

        # send signal with updated values
        self.new_train_values_signal.emit(self.trainCtrl.outputs, 1)
        self.new_train_temp_signal.emit(self.trainCtrl.cabin_temp, 1)

        return

    #Actual_Spd, Pass_ebrake
    def getvaluesfromtrain_update3(self, inputs):  # Sam call this to update traincontroller values

        self.trainCtrl.updatevalues(inputs,3)

        print("Train Controller TOT Container, type3: values updated, sending signals next")

        # send signal with updated values
        self.new_train_values_signal.emit(self.trainCtrl.outputs, 1)
        self.new_train_temp_signal.emit(self.trainCtrl.cabin_temp, 1)

        return

    # TrainModel
    # def updatevalues(self, inputs):
    #     # [actual speed, authority, received speed, pbrake, track circuit, underground, beacon]
    #     return self.trainCtrl.updatevalues(inputs)


def TrainC_main(system_time,type=True):
    trainctrlcntr = TrainController_Tot_Container(system_time,type)
    while True: trainctrlcntr.show_ui()


if __name__ == "__main__":
    system_time = SystemTimeContainer()
    TrainC_main(system_time, False)
