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
    def updatevalues(self, inputs,type):
        #update train controller with Train Model
        print("updatevalues")
        
        print(f"Train Controller HW: inputs: {inputs}")
        #print(f"Train Controller HW: before TrainModel_arr: {self.trainCtrl.TrainModel_arr}")
        
        if type ==0: 
            print("type0")
            self.trainCtrl.TrainModel_arr = inputs
        
        #Auth, Cmd_Spd
        elif type ==1: 
            print("type1")
            self.trainCtrl.TrainModel_arr[2] = inputs[0]#Auth
            self.trainCtrl.TrainModel_arr[1] = inputs[1]#Cmd_Spd
            
        #Track_Cicuit, Aboveground, beacon
        elif type ==2: 
            print("type2")
            self.trainCtrl.TrainModel_arr[4] = inputs[0]#Track_Cicuit
            self.trainCtrl.TrainModel_arr[5] = inputs[1]#Aboveground
            self.trainCtrl.TrainModel_arr[6] = inputs[2]#beacon
            
        #Actual_Spd, Pass_ebrake
        elif type ==3: 
            print("type3")
            self.trainCtrl.TrainModel_arr[0] = inputs[0]#Actual_Spd
            self.trainCtrl.TrainModel_arr[3] = inputs[1]#Pass_ebrake
        else:
            print("TRAIN CONTROLLER HW updatevalues: TYPE ERROR")
            
        #self.trainCtrl.TrainModel_arr = inputs
        #print(f"Train Controller HW: after  TrainModel_arr: {self.trainCtrl.TrainModel_arr}")

        #update output array to handoff to Train Model
        self.trainCtrl.updateTot()
        #print(f"Train Controller HW: self.trainCtrl.output_arr: {self.trainCtrl.output_arr}")
        print(f"Train Controller HW: after2  TrainModel_arr: {self.trainCtrl.TrainModel_arr}")
        self.outputs = self.trainCtrl.output_arr[:-1]
        #print(f"Train Controller HW: self.outputs[:-1]: {self.trainCtrl.output_arr[:-1]}")
        self.cabin_temp = self.trainCtrl.output_arr[-1]
        #print(f"Train Controller HW: self.outputs[-1]: {self.trainCtrl.output_arr[-1]}")

def TrainC_HW_main():
    system_time = SystemTimeContainer()
    trainctrlcntr = TrainControler_HW_Container(system_time)
    trainctrlcntr.show_ui()


if __name__ == "__main__":
    TrainC_HW_main()
