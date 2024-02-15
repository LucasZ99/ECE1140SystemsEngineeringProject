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
#update_arr
ticks
0: act spd
1: com spd
2: vit auth
3: spd lim
4: acc lim
buttons
5: pass ebrake
6: sig fail
7: eng fail
8: brake fail
'''

w = None

class TestBench_JEB382(QWidget):
    def __init__(self,numtrain,update_arr,ToggleBtn=None):#,verbose=False):
        super(TestBench_JEB382, self).__init__()
        self.setWindowTitle('TrainControllerHW TB #'+str(numtrain))
        
        ICON = QIcon(os.getcwd()+"\icon.png")
        self.setWindowIcon(ICON)
        
        #this array inputed as an init gets updated as UI is used
        #classes that created this TB have the array they passed locally update with it as well
        if len(update_arr)!=10:
            update_arr = [0]*10
            update_arr = [0.0, 0.0, 0.0, 0.0, 0.0, False, False, False, False, '']
        self.class_arr = update_arr
        #print(update_arr)
        
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
        
        self.genlabels()
        self.genbuttons()
        self.gentxtbox()
        self.Thread1_active = True
    
    #--------
    def genlabels(self):
        
        self.ticks = []
        tickNames1 = ["Actual Speed:","Commanded Speed","Vital Authority","Speed Limit","Accel/Decel Limit"]
        tickNames2 = ["MPH"          ,"MPH"            ,"Miles"          ,"MPH"        ,"MPH/s"]
        
        # generates tickboxes and names with names from array
        for i in range(1,len(tickNames1)+1):
            label1 = QLabel(tickNames1[i-1])
            #label1.setFrameStyle(QFrame.Panel)
            label1.setStyleSheet("border: 0px")
            label1.setMaximumHeight(40)
            self.layout.addWidget(label1, i, 0, 1, 1)
            
            tickbox = QDoubleSpinBox()
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
                self.class_arr[i] = self.ticks[i].value()
            #beacon
            for i in range(len(self.ticks),len(self.buttons)+len(self.ticks)):
                self.class_arr[i] = self.buttons[i-len(self.ticks)].isChecked()
            self.class_arr[-1] = self.textbox.text()
        except:
            print("TB done; min err")
            self.Thread1_active = False
            
            
    #--------
    def genbuttons(self):
        
        self.buttons = []
        buttonNames1 = ["Passenger eBrake","Signal Pickup Failure","Engine Failure","Brake Failure"]
        
        #make 
        
        # generates buttons with names from btnNames array
        for i in range(6,len(buttonNames1)+6):
            label1 = QLabel(buttonNames1[i-6])
            #label1.setFrameStyle(QFrame.Panel)
            label1.setStyleSheet("border: 0px")
            label1.setMaximumHeight(40)
            self.layout.addWidget(label1, i, 0, 1, 1)
            
            button = QPushButton()
            button.setCheckable(True)
            button.clicked.connect( functools.partial(self.count_clicks, index=i-6) )
            button.setStyleSheet("background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px")
            button.setText("Off")
            self.layout.addWidget(button, i, 1, 1, 1)
            self.buttons.append(button)
    def count_clicks(self,index):
        if self.buttons[index].isChecked():
            self.buttons[index].setStyleSheet("background-color: rgb(143, 186, 255); border: 2px solid rgb(42, 97, 184); border-radius: 6px")
            self.buttons[index].setText("On")
            self.class_arr[index+5] = True
        else:
            self.buttons[index].setStyleSheet("background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px")
            self.buttons[index].setText("Off")
            self.class_arr[index+5] = False
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
        txtlab = QLabel("Beacon: 0x")
        self.layout.addWidget(txtlab, 10, 0, 1, 1)
        self.textbox = QLineEdit()
        self.layout.addWidget(self.textbox, 10, 1, 1, 3)
            
            
    '''#--------
    def loop(self,verbose=False):
        while True:
            self.update_TestBench_JEB382()
            if verbose: print(f"TB TrainC #{numtrain}",arr)
            if not self.Thread1_active: break'''
            


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
    arr = [0]*10
    TB_fin(numtrain,arr)