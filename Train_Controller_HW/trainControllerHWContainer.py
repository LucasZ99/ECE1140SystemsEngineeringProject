# container class for calling everything from train
import sys
import numpy

from PyQt6.QtWidgets import QApplication

from .Tovarish_Belback_Jonah_Train_Controller_Testbenchv2 import *
from .Tovarish_Belback_Jonah_Train_Controller_HW_UI_PyFirmata import *


class Container:
    def __init__(self,Testbench=False):
        self.main_Driver_arr = []
        self.main_TrainModel_arr = []
        self.main_output_arr = []
        self.TB= Testbench
    
        self.trainCtrl = TC_HW_init(self.main_Driver_arr, self.main_TrainModel_arr, self.main_output_arr, Testbench)
        #HW_UI_JEB382_PyFirmat(self.main_Driver_arr, self.main_TrainModel_arr, self.main_output_arr, Testbench)

    def show_ui(self,printout=3):
        #it = util.Iterator(board)  
        #it.start()
        
        
        
        #printout 1: Driver
        #printout 2: TrainModel
        #printout 3: Output
        self.trainCtrl.HW_UI_fin(self.TB,printout)

    #  receiver functions

    #TrainModel
    def updatevalues(self, inputs):
        self.main_TrainModel_arr = numpy.copy(inputs)
    
    def output(self):
        return self.main_output_arr

def main():
    trainctrlcntr = Container()
    trainctrlcntr.show_ui()


if __name__ == "__main__":
    main()
