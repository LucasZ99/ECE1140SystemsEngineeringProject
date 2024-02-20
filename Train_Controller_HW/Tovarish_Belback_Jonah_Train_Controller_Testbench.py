import os
import sys
import functools
import time
import threading

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


'''app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))
window.setLayout(layout)
window.show()
app.exec()'''


'''
#TrainModel_arr
ticks
0: act spd
1: com spd
2: vit auth
3: spd lim
4: acc lim
buttons
5 : pass ebrake
6 : Track Circuit State
7 : Station side(0to3)
8 : sig fail
9 : eng fail
10: brake fail
11: beacon (128chars)
'''

w = None

class TestBench_JEB382(QWidget):
    def __init__(self,numtrain,TrainModel_arr,ToggleBtn=None):#,verbose=False):
        super(TestBench_JEB382, self).__init__()
        self.setWindowTitle('TrainControllerHW TB #'+str(numtrain))
        
        ICON = QIcon(os.getcwd()+"\icon.png")
        self.setWindowIcon(ICON)
        
        #this array inputed as an init gets updated as UI is used
        #classes that created this TB have the array they passed locally update with it as well
        if len(TrainModel_arr)<12:
            #if array is empty or missing values, autofills at end of missing indexes
            t_TrainModel_arr = [0.0, 0.0, 0.0, 0.0, 0.0, False, False, 0, False, False,False,"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"]
            TrainModel_arr = TrainModel_arr + t_TrainModel_arr[len(TrainModel_arr):]
        #if over, snips
        elif len(TrainModel_arr)>12: TrainModel_arr = TrainModel_arr[0:-(len(TrainModel_arr)-10)]
        #ensure beacon arr indx is proper size
        if len(str(TrainModel_arr[-1]))<128:
            TrainModel_arr[-1] = "0"*(128-len(str(TrainModel_arr[-1])))+str(TrainModel_arr[-1])
        elif len(str(TrainModel_arr[-1]))>128:
            TrainModel_arr[-1] = str(TrainModel_arr[-1])[len(str(TrainModel_arr[-1]))-128:]
        #checks door side state is within range
        if TrainModel_arr[7] not in range(0,4):
            TrainModel_arr[7]=0
        self.statside=TrainModel_arr[7]
        
        self.TrainModel_arr = TrainModel_arr
        #print(TrainModel_arr)
        
        #SW UI passthrough
        self.ToggleBtn = ToggleBtn
                
        #self.resize(800, 600)
        self.layout = QGridLayout(self)

        #self.tabs = tabWidget(self)
        #self.setCentralWidget(self.tabs)
        self.ttlabel = QLabel("Inputs from Train Model #"+str(numtrain))
        #self.ttlabel.setFrameStyle(QFrame.Panel)
        self.ttlabel.setStyleSheet("font-size: 18pt; border: 0px")
        self.ttlabel.setMaximumHeight(40)
        
        self.layout.addWidget(self.ttlabel, 0, 0, 1, 4)
        
        self.genTCKs()
        self.genbuttons()
        self.gentxtbox()
        self.Thread1_active = True
    
    #--------
    def genTCKs(self):
        
        self.ticks = []
        tickNames1 = ["Actual Speed:","Commanded Speed","Vital Authority","Speed Limit","Accel/Decel Limit"]
        tickNames2 = ["MPH"          ,"MPH"            ,"Miles"          ,"MPH"        ,"MPH/s"]
        
        # generates tickboxes and names with names from array
        for i in range(1,len(tickNames1)+1):
            label1 = better_label_ret(tickNames1[i-1])
            self.layout.addWidget(label1, i, 0, 1, 1)
            
            tickbox = QDoubleSpinBox()
            tickbox.setValue(self.TrainModel_arr[i-1])
            self.layout.addWidget(tickbox, i, 1, 1, 1)
            self.ticks.append(tickbox)
            
            label2 = QLabel(tickNames2[i-1])
            #label2.setFrameStyle(QFrame.Panel)
            label2.setStyleSheet("border: 0px")
            label2.setMaximumHeight(40)
            self.layout.addWidget(label2, i, 2, 1, 1)
    def update_TestBench_JEB382(self):
        try:
            #tickers
            for i in range(len(self.ticks)):
                self.TrainModel_arr[i] = self.ticks[i].value()
            #beacon
            for i in range(len(self.ticks),len(self.buttons)+len(self.ticks)):
                self.TrainModel_arr[i] = self.buttons[i-len(self.ticks)].isChecked()
            self.TrainModel_arr[-1] = self.textbox.text()
            
            #exception
            self.TrainModel_arr[7] = self.statside
        except:
            print("TB done; min err")
            self.Thread1_active = False
            
            
    #--------
    def genbuttons(self):
        self.buttons = []
        buttonNames1 = ["Passenger eBrake","Track Circuit State","Station Side","Signal Pickup Failure","Engine Failure","Brake Failure"]
                
        # generates buttons with names from btnNames array
        for i in range(1,len(buttonNames1)+1):
            label1 = better_label_ret(text=buttonNames1[i-1])
            self.layout.addWidget(label1, i, 4, 1, 1)
            
            button = better_button_ret()
            button.setChecked(self.TrainModel_arr[i+4])#TODO
            gen_but_tog(button)
            button.clicked.connect( functools.partial(gen_but_tog,but=button) )
            if i not in [2,3]: self.layout.addWidget(button, i, 5, 1, 1)
            self.buttons.append(button)
            print(i)
        
        #adjust 1,2 ; Track Circuit State,Station Side
        button = better_button_ret(text="Left",style="background-color: rgb(222, 62, 38); border: 2px solid rgb(222, 0, 0); border-radius: 4px")
        button.clicked.connect( functools.partial(gen_but_tog,but=button,text1="Left",text2="Right",
                                                  style_on="background-color: rgb(0, 224, 34); border: 2px solid rgb(30, 143, 47); border-radius: 4px",
                                                  style_off="background-color: rgb(222, 62, 38); border: 2px solid rgb(222, 0, 0); border-radius: 4px") )
        self.layout.addWidget(button, 2, 5, 1, 1)
        self.buttons[1] = button
        
        button = better_button_ret()
        self.BTNF_station(button,start=True)#change layout
        button.clicked.connect( functools.partial(self.BTNF_station,but=button))
        self.layout.addWidget(button, 3, 5, 1, 1)
        self.buttons[2] = button
        
    def BTNF_station(self,but,start=False):
        if   self.statside-start == 0: #0to1 Left
            but.setText("Left")
            but.setStyleSheet("background-color: rgb(255, 175, 255); border: 2px solid rgb(255, 150, 255); border-radius: 6px")
            if not start: self.statside = 1
            
        elif self.statside-start == 1: #1to2 Right
            but.setText("Right")
            but.setStyleSheet("background-color: rgb(255, 150, 255); border: 2px solid rgb(255, 115, 255); border-radius: 6px")
            if not start: self.statside = 2
            
        elif self.statside-start == 2: #2to3 Both
            but.setText("Both")
            but.setStyleSheet("background-color: rgb(255, 115, 255); border: 2px solid rgb(189,  72, 181); border-radius: 6px")
            if not start: self.statside = 3
            
        elif self.statside-start == 3: #3to0 Neither
            but.setText("Neither")
            but.setStyleSheet("background-color: rgb(255, 207, 255); border: 2px solid rgb(255, 175, 255); border-radius: 6px")
            if not start: self.statside = 0
        else: print("TestBench_JEB382 BTNF_station error")
        
     
    #code when window closes
    def closeEvent(self, *args, **kwargs):
        super(TestBench_JEB382, self).closeEvent(*args, **kwargs)
        if __name__ == "__main__": self.Thread1_active = False
        else:
            print("JEB382 TB Hidden")
            self.ToggleBtn.setText("Toggle TestBench[off]")
            self.ToggleBtn.setStyleSheet("background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px")
            
    
    #--------
    def gentxtbox(self):
        txtlab = better_label_ret("Beacon (128chars): 0x")
        self.layout.addWidget(txtlab, 12, 0, 1, 1)
        self.textbox = QLineEdit()
        self.textbox.setFixedWidth(852)
        self.textbox.setText(self.TrainModel_arr[-1])
        self.layout.addWidget(self.textbox, 13, 0, 1, 8)
            
 #--------#--------#--------#--------#--------
def better_button_ret(sizeW=True,sizeH=24,checkable=True,text="Off",style="background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px"):
        button = QPushButton()
        if sizeW: button.setFixedWidth(120)
        button.setFixedHeight(sizeH)
        button.setCheckable(checkable)
        button.setStyleSheet(style)
        button.setText(text)
        
        return button

def better_label_ret(text,size=10,bold=False):
    label = QLabel(text)
    label.setFixedWidth(120)
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


#=============================

def TB_mainloop_fast(numtrain):
    while True:
        print(f"TB TrainC #{numtrain}",arr)
        if w:
            w.update_TestBench_JEB382()
            if not w.Thread1_active: break
        
        
def TB_pyqtloop(numtrain,arr):
    app = QApplication(sys.argv)
    global w
    w = TestBench_JEB382(numtrain, arr)
    w.show()
    sys.exit(app.exec())
    
def TB_fin(numtrain,arr):
    t1 = threading.Thread(target=TB_pyqtloop, args=(numtrain,arr,))
    t2 = threading.Thread(target=TB_mainloop_fast, args=(numtrain,))
 
    t1.start()
    t2.start()
 
    t1.join()
    t2.join()
    
    
        
if __name__ == "__main__":
    numtrain=1
    arr =(
    # [9]*12
    [8.0, 9.0, 10.0, 11.0, 12.0, True, False, 1, True, False, True,"hiyaaaaa"]
    )
    #TB_fin(numtrain,arr)
    TB_pyqtloop(numtrain,arr)