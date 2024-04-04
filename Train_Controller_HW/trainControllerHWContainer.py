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
from SystemTime import SystemTimeContainer

class TrainControler_HW_Container:
    def __init__(self,system_time_container: SystemTimeContainer,Testbench=False):
        self.main_Driver_arr = []
        self.main_TrainModel_arr = [0,0,0,False,False,False,"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"]
        self.outputs = []
        self.TB= Testbench
        self.cabin_temp=68
        self.system_time = system_time_container.system_time
    
        self.trainCtrl = TC_HW_init(self.main_Driver_arr, self.main_TrainModel_arr, self.outputs, self.system_time, Testbench)
        #HW_UI_JEB382_PyFirmat(self.main_Driver_arr, self.main_TrainModel_arr, self.main_output_arr, Testbench)

    def show_ui(self):
        #it = util.Iterator(board)  
        #it.start()
        
        
        
        #printout 1: Driver
        #printout 2: TrainModel
        #printout 3: Output
        #self.trainCtrl.HW_UI_fin(self.TB)
        self.trainCtrl.updateTot()

    #  receiver functions

    #TrainModel
    def updatevalues(self, inputs):
        #update train controller with Train Model
        print("updatevalues")
        print(f"Train Controller HW: before TrainModel_arr: {self.trainCtrl.TrainModel_arr}")
        self.main_TrainModel_arr = numpy.copy(inputs)
        print(f"Train Controller HW: after  TrainModel_arr: {self.trainCtrl.TrainModel_arr}")
        #self.trainCtrl.updateRead() #get driver inputs
        
        #update output array to handoff to Train Model
        self.trainCtrl.updateTot()
        print(f"Train Controller HW: self.trainCtrl.output_arr: {self.trainCtrl.output_arr}")
        #self.trainCtrl.updateDisplay()  #update arduino display
        self.outputs = self.trainCtrl.output_arr[:-1]
        print(f"Train Controller HW: self.outputs[:-1]: {self.outputs}")
        self.cabin_temp = self.trainCtrl.output_arr[-1]
        print(f"Train Controller HW: self.outputs[-1]: {self.outputs[-1]}")
        #return self.main_output_arr[:-1]

def TrainC_HW_main():
    system_time = SystemTimeContainer()
    trainctrlcntr = TrainControler_HW_Container(system_time)
    trainctrlcntr.show_ui()


if __name__ == "__main__":
    TrainC_HW_main()
