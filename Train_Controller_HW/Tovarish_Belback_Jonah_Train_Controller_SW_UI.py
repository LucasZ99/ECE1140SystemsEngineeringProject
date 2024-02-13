from Tovarish_Belback_Jonah_Train_Controller_Testbench import TestBench_JEB382


import sys
import functools

from PyQt6.QtWidgets import *
from PyQt6 import QtCore
import threading

from PyQt6.QtCore import *  # pyqtSlot, QTimer, Qt,
import PyQt6.QtGui as QtGui
from PyQt6.QtGui import QPainter, QColor, QPen, QKeySequence






w = None

class SW_UI_JEB382(QWidget):
    def __init__(self,numtrain,Driver_arr,TrainModel_arr):
        super(SW_UI_JEB382, self).__init__()
        self.setWindowTitle('TrainControllerHW SW_UI #'+str(numtrain))        
        #self.setFixedHeight(600)
        #self.setFixedWidth(1000)
        
        self.TB_window = TestBench_JEB382(numtrain,TrainModel_arr)

        self.layout = QGridLayout(self)
        button1 = QPushButton("Push for Window 1")
        button1.clicked.connect(self.toggle_TB)
        self.layout.addWidget(button1,0,0,1,8)
        
        #---real
        #Mode select TODO
        #Open/Close TB select TODO
        '''self.genSect1_1()#TrainEnviroment TODO
        self.genSect1_2()#Station Info TODO
        self.genSect1_3()#FailStates TODO
        self.genSect2_1()#EngControl TODO
        self.genSect2_2()#DriverControl TODO'''
        self.genSect1_1(1,0)#TrainEnviroment TODO
        self.genSect1_2(1,4)#Station Info TODO
        self.genSect1_3(1,8)#FailStates TODO
        self.genSect2_1(7,0)#EngControl TODO
        self.genSect2_2(7,4)#DriverControl TODO
        self.layout.addWidget(QLabel(""), 6, 0, 1, 8)#spacer
        
        '''self.layout.addWidget(self.TrainEnv,      1, 0, 5, 3)#higher
        self.layout.addWidget(self.StationInfo,   1, 1, 3, 3)
        self.layout.addWidget(self.FailState,     1, 1, 4, 2)
        self.layout.addWidget(self.EngControl,    2, 0, 3, 2)#lower
        self.layout.addWidget(self.DriverControl, 2, 2, 5, 6)'''
        '''self.layout.addWidget(self.TrainEnv,      2, 0, 5, 3)#higher
        self.layout.addWidget(self.StationInfo,   2, 3, 5, 3)
        self.layout.addWidget(self.FailState,     2, 6, 5, 2)
        self.layout.addWidget(self.EngControl,    5, 0, 6, 3)#lower
        self.layout.addWidget(self.DriverControl, 5, 3, 6, 6)'''
    
    #--------
    #code when window closes
    def closeEvent(self, *args, **kwargs):
        super(SW_UI_JEB382, self).closeEvent(*args, **kwargs)
        self.TB_window.hide()
        self.TB_window.Thread1_active = False
        print("close")
        
    def toggle_TB(self):
        if self.TB_window.isVisible(): self.TB_window.hide(); print("JEB382 TB Hidden")
        else: self.TB_window.show()
    

    #--------
    def genSect1_1(self,OriginX,OriginY):
        #5R;3C
        self.TrainEnv = QWidget()
        self.TrainEnv.layout = QGridLayout(self)
        
        self.TrainEnv.setFixedHeight(200)
        
        #generate labels
        label = QLabel("Train Enviroment")
        label.setStyleSheet("font-size: 16pt; border: 0px")
        self.layout.addWidget(label, OriginX, OriginY, 1, 3)
        
        label_names = ["Cabin Lights","Headlights","Cabin Temp","Doors (Left,Right)"]
        for i in range(1,len(label_names)+1):
            label = QLabel(label_names[i-1])
            label.setStyleSheet("border: 0px")
            self.layout.addWidget(label, OriginX+i, OriginY, 1, 1)
        
        #indiviually make rest of section
        #LEDs
        self.LED_CabnLgt = better_button_ret(40,"Off",False)
        self.TrainEnv.layout.addWidget(self.LED_CabnLgt, OriginX+1, OriginY+1, 1, 1)
        print(OriginX+1, OriginY+1)
        '''self.LED_HeadLgt = better_button_ret(40,"Off",False)
        self.layout.addWidget(self.LED_HeadLgt, OriginX+2, OriginY+1, 1, 1)
        
        self.Door_L = better_button_ret(40,"Off",False)
        self.TrainEnv.layout.addWidget(self.Door_L, OriginX+4, OriginY+1, 1, 1)
        self.Door_R = better_button_ret(40,"Off",False)
        self.layout.addWidget(self.Door_R, OriginX+4, OriginY+2, 1, 1)
        
        self.Tck_Temp = QDoubleSpinBox()
        self.Tck_Temp.setStyleSheet("border: 0px")
        self.layout.addWidget(self.Tck_Temp, OriginX+3, OriginY+1, 1, 1)
        label = QLabel("°F")
        label.setStyleSheet("border: 0px")
        self.layout.addWidget(label, OriginX+3, OriginY+2, 1, 3)'''
            
        
        self.TrainEnv.setLayout(self.TrainEnv.layout)
            
        
        
        
        
    #--------
    def genSect1_2(self,OriginX,OriginY):
        #3R;3C
        self.StationInfo = QWidget()
        self.StationInfo.layout = QGridLayout(self)
        
        #self.StationInfo.setFixedHeight(200)
        
        #generate labels
        label = QLabel("Station Information")
        label.setStyleSheet("font-size: 16pt; border: 0px")
        self.layout.addWidget(label, OriginX, OriginY, 1, 3)
        
        
        self.StationInfo.setLayout(self.StationInfo.layout)
    
    #--------
    def genSect1_3(self,OriginX,OriginY):
        #4R;2C
        self.FailState = QWidget()
        self.FailState.layout = QGridLayout(self)
        
        self.FailState.setFixedHeight(200)
        
        #generate labels
        label = QLabel("Fail States")
        label.setStyleSheet("font-size: 16pt; border: 0px")
        self.layout.addWidget(label, OriginX, OriginY, 1, 3)
        
        
        
        self.FailState.setLayout(self.FailState.layout)
    
    #--------
    def genSect2_1(self,OriginX,OriginY):
        #3R;2C
        self.EngControl = QWidget()
        self.EngControl.layout = QGridLayout(self)
        
        self.EngControl.setFixedHeight(200)
        
        #generate labels
        label = QLabel("Engineer Control")
        label.setStyleSheet("font-size: 16pt; border: 0px")
        self.layout.addWidget(label, OriginX, OriginY, 1, 3)
        
        
        
        self.EngControl.setLayout(self.EngControl.layout)
    
    #--------
    def genSect2_2(self,OriginX,OriginY):
        #4R;3C+(2 Button spacing)
        self.DriverControl = QWidget()
        self.DriverControl.layout = QGridLayout(self)
        
        self.DriverControl.setFixedHeight(200)
        
        #generate labels
        label = QLabel("Driver Control")
        label.setStyleSheet("font-size: 16pt; border: 0px")
        self.layout.addWidget(label, OriginX, OriginY, 1, 3)
        
        
        
        self.DriverControl.setLayout(self.DriverControl.layout)



#=============================


def better_button_ret(size,text=None,checkable=True):
        button = QPushButton()
        button.setCheckable(checkable)
        #button.clicked.connect( functools.partial(button_click1, but=button) )
        if checkable:
            button.setStyleSheet("background-color: rgb(156, 156, 156); border: 1px solid black")
            if text: button.setText(text)
            else: button.setText("Off")
        else:
            button.setStyleSheet("background-color: rgb(222, 62, 38); border: 1px solid black")
            if text: button.setText(text)
        button.setFixedWidth(size)
        return button

#=============================


def SW_mainloop_fast(numtrain):
    try:
        while True:
            if w:
                if w.TB_window.isVisible():
                    print(f"TB TrainC #{numtrain}",TrainModel_arr)
                    w.TB_window.updatetick()
                    if not w.TB_window.Thread1_active: break
    except:
        print("TB done; minor err")

def SW_pyqtloop(numtrain,Driver_arr,TrainModel_arr):
    app = QApplication(sys.argv)
    global w
    w = SW_UI_JEB382(numtrain, Driver_arr, TrainModel_arr)
    w.show()
    sys.exit(app.exec())
    
def SW_fin(numtrain,Driver_arr,TrainModel_arr):
    t1 = threading.Thread(target=SW_pyqtloop, args=(numtrain,Driver_arr,TrainModel_arr,))
    t2 = threading.Thread(target=SW_mainloop_fast, args=(numtrain,))
 
    t1.start()
    t2.start()
 
    t1.join()
    t2.join()



if __name__ == "__main__":    
    numtrain=1
    Driver_arr = [0]*10
    TrainModel_arr = [0]*10
    SW_fin(numtrain,Driver_arr,TrainModel_arr)