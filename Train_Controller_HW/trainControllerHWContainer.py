# container class for calling everything from train
import sys
import numpy

from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    from Tovarish_Belback_Jonah_Train_Controller_Testbenchv2 import *
    from Tovarish_Belback_Jonah_Train_Controller_HW_UI_PyFirmata import *
else:
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

    def show_ui(self):
        #it = util.Iterator(board)  
        #it.start()
        
        
        
        #printout 1: Driver
        #printout 2: TrainModel
        #printout 3: Output
        self.trainCtrl.HW_UI_fin(self.TB)

    #  receiver functions

    #TrainModel
    def updatevalues(self, inputs):
        #update train controller with Train Model
        self.main_TrainModel_arr = numpy.copy(inputs)
        self.trainCtrl.updateRead() #get driver inputs
        
        #update output array to handoff to Train Model
        self.trainCtrl.updateTot()
        self.trainCtrl.updateDisplay()  #update arduino display
        return self.main_output_arr

def main():
    trainctrlcntr = Container()
    trainctrlcntr.show_ui()


if __name__ == "__main__":
    main()
