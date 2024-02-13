from Tovarish_Belback_Jonah_Train_Controller_Testbench import TestBench_JEB382

import os
import sys
import functools

import PyQt6.QtGui as QtGui
import threading

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *





TB_verbose = True
w = None
stylesheet = """
    SW_UI_JEB382 {
        border-image: url(JEB382_bg2);
        background-repeat: no-repeat; 
        background-position: center;
    }
"""

class SW_UI_JEB382(QMainWindow):
    def __init__(self,numtrain,Driver_arr,TrainModel_arr,app=None):
        super(SW_UI_JEB382, self).__init__()
        self.setWindowTitle('TrainControllerHW SW_UI #'+str(numtrain))        
        self.setFixedWidth (640)
        self.setFixedHeight(445)
        #print(self.size())
        
        ICON = QIcon(os.getcwd()+"\icon.png")
        self.setWindowIcon(ICON)
        
        self.WidgetSpace = QWidget()
        self.setCentralWidget(self.WidgetSpace)

        self.layout = QGridLayout(self.WidgetSpace)
        
        #---real
        self.genSect0(0,0) #TestBench; Mode Select
        self.genSect1_1(1,0) #TrainEnviroment
        self.genSect1_2(1,4) #Station Info
        self.genSect1_3(1,10) #FailStates
        self.genSect2_1(6,0) #EngControl
        self.genSect2_2(6,4) #DriverControl TODO
        self.layout.addWidget(QLabel(""), 5, 0,  1, 8)#spacer; Horz 1_x/2_x
        self.layout.addWidget(QLabel(""), 1, 3, 13, 1)#spacer; Vert x_1/x_2
        self.layout.addWidget(QLabel(""), 1, 8,  6, 1)#spacer; Vert x_2/x_3
        path = os.getcwd()+"\Train_Controller_HW\JEB382_bg1.png"
        #print(path)
        if app: app.setStyleSheet(stylesheet)

    
    #--------
    #code when window closes
    def closeEvent(self, *args, **kwargs):
        super(SW_UI_JEB382, self).closeEvent(*args, **kwargs)
        self.TB_window.hide()
        self.TB_window.Thread1_active = False
        print("closed UI")
        
    def toggle_TB(self):
        if self.TB_window.isVisible():
            self.TB_window.hide()
            self.BTN_TB.setStyleSheet("background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px")
            print("JEB382 TB Hidden")
        else:
            self.BTN_TB.setStyleSheet("background-color: rgb(143, 186, 255); border: 2px solid rgb(42, 97, 184); border-radius: 6px")
            self.TB_window.show()
    

    #--------
    def genSect0(self,OriginY,OriginX):
        self.BTN_TB = better_button_ret(text="Toggle TestBench")
        self.BTN_TB.clicked.connect(self.toggle_TB)
        self.layout.addWidget(self.BTN_TB,0,0,1,3)
        
        self.TB_window = TestBench_JEB382(numtrain,TrainModel_arr,self.BTN_TB)
        
        self.BTN_Mode = better_button_ret(text="Auto")
        self.layout.addWidget(self.BTN_Mode, OriginY, OriginX+4, 1, 8)

    #--------
    def genSect1_1(self,OriginY,OriginX):
        #5R;3C
        
        #generate labels
        label = better_label_ret("Train Enviroment",16)
        self.layout.addWidget(label, OriginY, OriginX, 1, 3)
        
        label_names = ["Cabin Lights","Headlights","Cabin Temp"]
        for i in range(1,len(label_names)+1):
            label = better_label_ret(label_names[i-1])
            self.layout.addWidget(label, OriginY+i, OriginX, 1, 1)
        
        #individually make rest of section
        #LEDs
        self.LED_CabnLgt = better_button_ret(50,"Off",False)
        self.layout.addWidget(self.LED_CabnLgt, OriginY+1, OriginX+1, 1, 1)
        self.LED_HeadLgt = better_button_ret(50,"Off",False)
        self.layout.addWidget(self.LED_HeadLgt, OriginY+2, OriginX+1, 1, 1)
        
        self.LED_Temp = better_button_ret(50,"0.00",False)
        self.LED_Temp.setStyleSheet("background-color: white; border: 1px solid black")
        self.layout.addWidget(self.LED_Temp, OriginY+3, OriginX+1, 1, 1)
        label = better_label_ret("°F")
        self.layout.addWidget(label, OriginY+3, OriginX+2, 1, 3)
    
    #--------
    def genSect1_2(self,OriginY,OriginX):
        #3R;3C
        
        #generate labels
        label = better_label_ret("Station Information",16)
        self.layout.addWidget(label, OriginY, OriginX, 1, 3)
        
        #individually make rest of section
        self.layout.addWidget(better_label_ret("Announcement"), OriginY+1, OriginX, 1, 2)
        self.Announce = better_button_ret(106,"N/A",False)
        self.Announce.setStyleSheet("background-color: white; border: 1px solid black")
        self.layout.addWidget(self.Announce, OriginY+1, OriginX+2, 1, 2)
        
        self.layout.addWidget(better_label_ret("Doors (Left, Right)"), OriginY+2, OriginX, 1, 2)
        self.LED_Door_L = better_button_ret(50,"Off",False)
        self.layout.addWidget(self.LED_Door_L, OriginY+2, OriginX+2, 1, 1)
        self.LED_Door_R = better_button_ret(50,"Off",False)
        self.layout.addWidget(self.LED_Door_R, OriginY+2, OriginX+3, 1, 1)
    
    #--------
    def genSect1_3(self,OriginY,OriginX):
        #4R;2C
        
        #generate labels
        label = better_label_ret("Fail States",16)
        self.layout.addWidget(label, OriginY, OriginX, 1, 3)
        
        label_names = ["Signal Failure","Engine Failure","Brake Failure"]
        for i in range(1,len(label_names)+1):
            label = better_label_ret(label_names[i-1])
            self.layout.addWidget(label, OriginY+i, OriginX, 1, 1)
        
        #individually make rest of section
        #LEDs
        self.LED_Sig_Fail = better_button_ret(50,"Off",False)
        self.layout.addWidget(self.LED_Sig_Fail, OriginY+1, OriginX+1, 1, 1)
        self.LED_Eng_Fail = better_button_ret(50,"Off",False)
        self.layout.addWidget(self.LED_Eng_Fail, OriginY+2, OriginX+1, 1, 1)
        self.LED_Brk_Fail = better_button_ret(50,"Off",False)
        self.layout.addWidget(self.LED_Brk_Fail, OriginY+3, OriginX+1, 1, 1)
    
    #--------
    def genSect2_1(self,OriginY,OriginX):
        #3R;2C
        
        #generate labels
        label = better_label_ret("Engineer Control",16)
        self.layout.addWidget(label, OriginY, OriginX, 1, 3)
        
        label_names = ["Kp Gain","Ki Gain"]
        for i in range(1,len(label_names)+1):
            label = better_label_ret(label_names[i-1])
            self.layout.addWidget(label, OriginY+i, OriginX, 1, 1)
        
        #individually make rest of section
        self.TCK_Kp = QDoubleSpinBox()
        self.layout.addWidget(self.TCK_Kp, OriginY+1, OriginX+1, 1, 1)
        self.TCK_Ki = QDoubleSpinBox()
        self.layout.addWidget(self.TCK_Ki, OriginY+2, OriginX+1, 1, 1)
    
    #--------
    def genSect2_2(self,OriginY,OriginX):
        #4R;3C+(2 Button spacing) TODO
        
        #generate labels
        label = better_label_ret("Driver Control",16)
        self.layout.addWidget(label, OriginY, OriginX, 1, 3)
        
        label_names = ["Actual Speed","Commanded Speed","Cabin Lights","Headlights","Cabin Temp","Doors (Left, Right)"]
        for i in range(1,len(label_names)+1):
            label = better_label_ret(label_names[i-1])
            self.layout.addWidget(label, OriginY+i, OriginX, 1, 2)
        
        #individually make rest of section
        self.LED_CurSpd = better_button_ret(50,"0.00",False)
        self.LED_CurSpd.setStyleSheet("background-color: rgb(207, 207, 207); border: 1px solid black")
        self.layout.addWidget(self.LED_CurSpd, OriginY+1, OriginX+2, 1, 1)
        label = better_label_ret("MPH")
        self.layout.addWidget(label, OriginY+1, OriginX+3, 1, 3)
        
        self.TCK_CmdSpd = QDoubleSpinBox()
        self.layout.addWidget(self.TCK_CmdSpd, OriginY+2, OriginX+2, 1, 1)
        label = better_label_ret("MPH")
        self.layout.addWidget(label, OriginY+2, OriginX+3, 1, 3)
        
        self.BTN_CabnLgt = better_button_ret(50)
        self.layout.addWidget(self.BTN_CabnLgt, OriginY+3, OriginX+2, 1, 1)
        self.BTN_HeadLgt = better_button_ret(50)
        self.layout.addWidget(self.BTN_HeadLgt, OriginY+4, OriginX+2, 1, 1)
        
        self.TCK_Temp = QDoubleSpinBox()
        self.layout.addWidget(self.TCK_Temp, OriginY+5, OriginX+2, 1, 1)
        label = better_label_ret("°F")
        self.layout.addWidget(label, OriginY+5, OriginX+3, 1, 3)
        
        self.BTN_Door_L = better_button_ret(50)
        self.layout.addWidget(self.BTN_Door_L, OriginY+6, OriginX+2, 1, 1)
        self.BTN_Door_R = better_button_ret(50)
        self.layout.addWidget(self.BTN_Door_R, OriginY+6, OriginX+3, 1, 1)
        
        #right side
        self.BTN_EBRK = better_button_ret(text="EMERGENCY BRAKE")
        self.BTN_EBRK.setStyleSheet("background-color: rgb(200, 100, 100); border: 6px solid rgb(120, 0, 0); border-radius: 6px")
        self.BTN_EBRK.setFixedHeight(116)
        self.layout.addWidget(self.BTN_EBRK, OriginY, OriginX+5, 4, 3)
        self.BTN_SBRK = better_button_ret(text="Service Brake")
        self.BTN_SBRK.setFixedHeight(86)
        self.layout.addWidget(self.BTN_SBRK, OriginY+4, OriginX+5, 3, 3)



#=============================


def better_button_ret(size=None,text=None,checkable=True):
        button = QPushButton()
        button.setCheckable(checkable)
        button.setFixedHeight(24)
        #button.clicked.connect( functools.partial(button_click1, but=button) )
        if checkable:
            button.setStyleSheet("background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px")
            if text: button.setText(text)
            else: button.setText("Off")
        else:
            button.setStyleSheet("background-color: rgb(222, 62, 38); border: 2px solid rgb(222, 0, 0); border-radius: 4px")
            if text: button.setText(text)
        if size: button.setFixedWidth(size)
        return button

def better_label_ret(text,size=10,bold=True):
    label = QLabel(text)
    label.setStyleSheet(f"font-size: {size}pt; border: 0px; {'font-weight: bold;' if bold else ''}")
    return label

#=============================


def SW_mainloop_fast(numtrain):
    try:
        while True:
            if w:
                if w.TB_window.isVisible():
                    if TB_verbose: print(f"TB TrainC #{numtrain}",TrainModel_arr)
                    w.TB_window.updatetick()
                    if not w.TB_window.Thread1_active: break
                if not TB_verbose: print(f"SW TrainC #{numtrain}",Driver_arr)
    except:
        print("TB done; minor err")

def SW_pyqtloop(numtrain,Driver_arr,TrainModel_arr):
    app = QApplication(sys.argv)
    #app.setStyleSheet(stylesheet)
    global w
    w = SW_UI_JEB382(numtrain, Driver_arr, TrainModel_arr, app)
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