# container class for calling everything from train
import sys
import numpy

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSlot, pyqtSignal, QObject

from Train_Controller_SW.trainControllerSWContainer import TrainControllerSWContainer
from Train_Controller_HW.trainControllerHWContainer import TrainControler_HW_Container
from Train_Controller_SW.trainControllerSWUI import UI
from SystemTime import SystemTimeContainer





#================================================================================
class TrainController_Tot_Container(QObject):

    # Signals
    # new_train_values_signal = pyqtSignal(list, int)
    # new_train_temp_signal = pyqtSignal(float, int)
    # sam connect these signals to your respective update train model values command

    def __init__(self, system_time_container: SystemTimeContainer):
        super().__init__()
        
        self.system_time = system_time_container
        self.ctrl_list = []
        self.HW_index = None # index for future utility incase of handling recovery of deleted HW Controller
    
    
    
    #================================================================================
    # return HW/SW Container
    def new_train_controller(self):
        if self.HW_index:
            trainCtrl = TrainControllerSWContainer(self.system_time)
        else:
            self.HW_index = len(self.ctrl_list)
            trainCtrl = TrainControler_HW_Container(self.system_time)
        self.ctrl_list.append(trainCtrl)
        return trainCtrl



    #================================================================================
    # gonna need a show ui method for the list of sw controllers
    # not sure we will want to handle the hw ui though...

    # like this maybe ? vvv
    def show_hwui(self):
        if self.HW_index:
            self.ctrl_list[self.HW_index].show_ui()
        else:
            print("WARNING: TrainController_Tot_Container: show_hwui without HW Controller")

    def show_swui(self):
        app = QApplication.instance()

        if app is None:
            app = QApplication([])

        self.ui = UI()

        self.ui.show()  # this unresolved reference is fine
        # self.ui.refreshengine()

        app.exec()



#================================================================================
def TrainC_main(system_time, type=True):
    trainctrlcntr = TrainController_Tot_Container(system_time)
    cntrl = trainctrlcntr.new_train_controller()  # removed (type) as parameter
    while True: cntrl.show_ui()


if __name__ == "__main__":
    system_time = SystemTimeContainer()
    TrainC_main(system_time, False)
