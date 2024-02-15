from Tovarish_Belback_Jonah_Train_Controller_Testbench import TestBench_JEB382

import os
import sys
import functools

import PyQt6.QtGui as QtGui
import threading

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

#TODO
#add passenger ebrake alert
#add disable passenger ebrake
#make so commanded speed in Driver_arr is overwritten by TrainModels cmd spd if in auto
#fix toggle TB text when TB is closed (off/on text flipped)

#add hiding lower section in automatic



verbose = True
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
        
        self.numtrain = numtrain
        
        #array inputed as an init gets updated as UI is used
        #classes that created this TB have the array they passed locally update with it as well
        if len(TrainModel_arr)!=10:
            TrainModel_arr = [0]*10
            TrainModel_arr = [0.0, 0.0, 0.0, 0.0, 0.0, False, False, False, False, ""]
        self.TrainModel_arr = TrainModel_arr
        if len(Driver_arr)!=11:
            Driver_arr = [0]*11
            Driver_arr = [0.0, 0.0, 0.0, False, False, 0.0, False, False, False, False, ""]
        self.Driver_arr = Driver_arr
        
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
        
        self.init_comp=True
        self.aux1=self.Driver_arr[:]#copy not reference
        self.aux2=self.TrainModel_arr[:]
        self.update_SW_UI_JEB382(True)
        if self.Driver_arr[-1] == "" or self.Driver_arr[-1] == 0.0: self.LED_Announce.setText("N/A")


    
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
            
    def update_SW_UI_JEB382(self,skip=False):
        if not(self.init_comp and self.isVisible() ): return
        try:
            #----get values of all the TCKs and BTNs; put in Driver_arr
            if self.BTN_Mode.isChecked() or skip:   #update the array if its manual mode
                self.Driver_arr[0] = self.TCK_Kp.value()    #2_1
                self.Driver_arr[1] = self.TCK_Ki.value()
                self.Driver_arr[2] = self.TCK_CmdSpd.value()
                self.Driver_arr[3] = self.BTN_CabnLgt.isChecked()
                self.Driver_arr[4] = self.BTN_HeadLgt.isChecked()
                self.Driver_arr[5] = self.TCK_Temp.value()
                self.Driver_arr[6] = self.BTN_Door_L.isChecked()
                self.Driver_arr[7] = self.BTN_Door_R.isChecked()
                self.Driver_arr[8] = self.BTN_EBRK.isChecked()
                self.Driver_arr[9] = self.BTN_SBRK.isChecked()
            #self.Driver_arr[10] = Announcement
            #else:hide TODO
            
            #----get values from Test Bench
            if self.TB_window.isVisible():
                self.TB_window.update_TestBench_JEB382()
            
            #detect changes before changing LED
            #change LED values
            if self.aux1[ 3] != self.Driver_arr[ 3]: LED_tog(self.LED_CabnLgt,       self.aux1[ 3])
            if self.aux1[ 4] != self.Driver_arr[ 4]: LED_tog(self.LED_HeadLgt,       self.aux1[ 4])
            self.LED_Temp    .setText(str(  self.aux1[ 5]))
            self.LED_Announce.setText(str(  self.aux1[-1]))
            if self.aux1[ 6] != self.Driver_arr[ 6]: LED_tog(self.LED_Door_L,        self.aux1[ 6])
            if self.aux1[ 7] != self.Driver_arr[ 7]: LED_tog(self.LED_Door_R,        self.aux1[ 7])
            if self.aux2[-4] != self.TrainModel_arr[-4]: LED_tog(self.LED_Sig_Fail,  self.aux2[-4])
            if self.aux2[-3] != self.TrainModel_arr[-3]: LED_tog(self.LED_Eng_Fail,  self.aux2[-3])
            if self.aux2[-2] != self.TrainModel_arr[-2]: LED_tog(self.LED_Brk_Fail,  self.aux2[-2])
            self.LED_CurSpd  .setText(str(  self.aux2[0]))
            if self.aux1[-1] != self.Driver_arr[-1] and self.aux1[-1] != "" and self.aux1[-1] != 0.0:
                print("HEEEERRREEE:",self.aux1[-1])
                self.LED_Announce.setText( str(self.Driver_arr[-1]) )
            
            self.aux1=self.Driver_arr[:]
            self.aux2=self.TrainModel_arr[:]
        except Exception as e:
            print("update:",e)
            return
                    


    #--------
    def genSect0(self,OriginY,OriginX):
        self.BTN_TB = better_button_ret(text1="Toggle TestBench[off]",text2="Toggle TestBench[on]")
        self.BTN_TB.clicked.connect(self.toggle_TB)
        self.layout.addWidget(self.BTN_TB,0,0,1,3)
        
        self.TB_window = TestBench_JEB382(self.numtrain,self.TrainModel_arr,self.BTN_TB)
        
        self.BTN_Mode = better_button_ret(text1="Auto",text2="Manual")
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
        self.LED_CabnLgt = better_button_ret(50,"Off",checkable=False)
        self.layout.addWidget(self.LED_CabnLgt, OriginY+1, OriginX+1, 1, 1)
        self.LED_HeadLgt = better_button_ret(50,"Off",checkable=False)
        self.layout.addWidget(self.LED_HeadLgt, OriginY+2, OriginX+1, 1, 1)
        
        self.LED_Temp = better_button_ret(50,"0.00",checkable=False)
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
        self.LED_Announce = better_button_ret(106,"N/A",checkable=False)
        self.LED_Announce.setStyleSheet("background-color: white; border: 1px solid black")
        self.layout.addWidget(self.LED_Announce, OriginY+1, OriginX+2, 1, 2)
        
        self.layout.addWidget(better_label_ret("Doors (Left, Right)"), OriginY+2, OriginX, 1, 2)
        self.LED_Door_L = better_button_ret(50,"Off",checkable=False)
        self.layout.addWidget(self.LED_Door_L, OriginY+2, OriginX+2, 1, 1)
        self.LED_Door_R = better_button_ret(50,"Off",checkable=False)
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
        self.LED_Sig_Fail = better_button_ret(50,"Off",checkable=False)
        self.layout.addWidget(self.LED_Sig_Fail, OriginY+1, OriginX+1, 1, 1)
        self.LED_Eng_Fail = better_button_ret(50,"Off",checkable=False)
        self.layout.addWidget(self.LED_Eng_Fail, OriginY+2, OriginX+1, 1, 1)
        self.LED_Brk_Fail = better_button_ret(50,"Off",checkable=False)
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
        self.LED_CurSpd = better_button_ret(50,"0.00",checkable=False)
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
        #TODO:add style to better_button_ret
        self.BTN_EBRK = better_button_ret(text1="EMERGENCY BRAKE",
                                          style1="background-color: rgb(200,  50,  50); border: 6px solid rgb(120, 0, 0); border-radius: 6px",
                                          style2="background-color: rgb(200, 100, 100); border: 6px solid rgb(120, 0, 0); border-radius: 6px")
        self.BTN_EBRK.setStyleSheet("background-color: rgb(200, 100, 100); border: 6px solid rgb(120, 0, 0); border-radius: 6px")
        self.BTN_EBRK.setFixedHeight(116)
        self.layout.addWidget(self.BTN_EBRK, OriginY, OriginX+5, 4, 3)
        self.BTN_SBRK = better_button_ret(text1="Service Brake")
        self.BTN_SBRK.setFixedHeight(86)
        self.layout.addWidget(self.BTN_SBRK, OriginY+4, OriginX+5, 3, 3)



#=============================
#abstract generation funcs

def better_button_ret(size=None,text1=None,text2=None,checkable=True,style1=None,style2=None):
        if text1 and not text2: text2=text1
        button = QPushButton()
        button.setCheckable(checkable)
        button.setFixedHeight(24)
        #button.clicked.connect( functools.partial(button_click1, but=button) )
        if checkable:
            button.setStyleSheet("background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px")
            if text1: button.setText(text1)
            else: button.setText("Off")
            button.clicked.connect( functools.partial(gen_but_tog, but=button, text1=text1,text2=text2, style_on=style1,style_off=style2) )
        else:
            button.setStyleSheet("background-color: rgb(222, 62, 38); border: 2px solid rgb(222, 0, 0); border-radius: 4px")
            if text1: button.setText(text2)
        if size: button.setFixedWidth(size)
        return button

def better_label_ret(text,size=10,bold=True):
    label = QLabel(text)
    label.setStyleSheet(f"font-size: {size}pt; border: 0px; {'font-weight: bold;' if bold else ''}")
    return label

def gen_but_tog(but, text1=None,text2=None, style_on=None,style_off=None):
    if but.isChecked():
        but.setStyleSheet(f"{style_on  if style_on  else 'background-color: rgb(143, 186, 255); border: 2px solid rgb( 42,  97, 184); border-radius: 6px'}")
        if text1: but.setText(text2)
        else: but.setText("On")
    else:
        but.setStyleSheet(f"{style_off if style_off else 'background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px'}")
        if text1: but.setText(text1)
        else: but.setText("Off")

#change format of LEDs TODO, .value funcs are fine
def LED_tog(but,checked):
    #on
    if checked:
        but.setText("Off")
        but.setStyleSheet("background-color: rgb(222, 62, 38); border: 2px solid rgb(222, 0, 0); border-radius: 4px")
    else:
        but.setText("On")
        but.setStyleSheet("background-color: rgb(0, 224, 34); border: 2px solid rgb(30, 143, 47); border-radius: 4px")
        

#=============================
#threading debug funcs
import time
def SW_mainloop_fast(numtrain):
    time.sleep(2)
    try:
        while True:
            if w:
                w.update_SW_UI_JEB382()
                if w.TB_window.isVisible():
                    if verbose:
                        print(f"TB TrainC #{numtrain}",TrainModel_arr)
                    #w.TB_window.update_TestBench_JEB382()
                    if not w.TB_window.Thread1_active: break
                #if verbose and not w.TB_window.isVisible(): print(f"SW TrainC #{numtrain}",Driver_arr)
    except Exception as e:
        print("MAINLOOP:",e)
        #print("TB done; minor err")

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
    Driver_arr = [0.00]*11
    TrainModel_arr = [0.00]*10
    SW_fin(numtrain,Driver_arr,TrainModel_arr)