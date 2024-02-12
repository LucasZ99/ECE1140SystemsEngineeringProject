import sys
import functools
import time
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
import threading

from PyQt6.QtCore import *  # pyqtSlot, QTimer, Qt,
import PyQt6.QtGui as QtGui
from PyQt6.QtGui import QPainter, QColor, QPen, QKeySequence


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

Thread1_active = True
w = None

class mainWindow(QWidget):
    def __init__(self,numtrain,update_arr):
        super(mainWindow, self).__init__()
        self.setWindowTitle('TrainControllerHW TB #'+str(numtrain))
        
        #this array inputed as an init gets updated as UI is used
        #classes that created this TB have the array they passed locally update with it as well
        self.update_arr = update_arr
                
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

        self.show()
    
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
            tickbox.setStyleSheet("border: 0px")
            self.layout.addWidget(tickbox, i, 1, 1, 1)
            self.ticks.append(tickbox)
            
            label2 = QLabel(tickNames2[i-1])
            #label2.setFrameStyle(QFrame.Panel)
            label2.setStyleSheet("border: 0px")
            label2.setMaximumHeight(40)
            self.layout.addWidget(label2, i, 2, 1, 1)
    def updatetick(self):
        for i in range(len(self.ticks)):
            self.update_arr[i] = self.ticks[i].value()
            
            
    
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
            button.setStyleSheet("background-color: green; border: 3px solid black")
            self.layout.addWidget(button, i, 1, 1, 1)
            self.buttons.append(button)
    def count_clicks(self,index):
        if self.buttons[index].isChecked():
            self.buttons[index].setStyleSheet("background-color: red; border: 3px solid black")
            self.update_arr[index+5] = True
        else:
            self.buttons[index].setStyleSheet("background-color: green; border: 3px solid black")
            self.update_arr[index+5] = False
    #code when window closes
    def closeEvent(self, *args, **kwargs):
        super(mainWindow, self).closeEvent(*args, **kwargs)
        global Thread1_active
        Thread1_active = False
        
        
def mainloop_1sec():
    exec = False
    lastexec = 0
    while True:
        if not exec:
            exec = True
            lastexec = time.time()
            #hahahah
            print(arr)
            if w: w.updatetick()
        if time.time() - lastexec > 1: exec = False
        if not Thread1_active: break
def mainloop_fast(numtrain):
    while True:
        print(f"TB TrainC #{numtrain}",arr)
        if w: w.updatetick()
        if not Thread1_active: break
        
        
def pyqtloop(numtrain,arr):
    app = QApplication(sys.argv)
    global w
    w = mainWindow(numtrain, arr)
    sys.exit(app.exec())
    
def TB_fin(numtrain,arr):
    t1 = threading.Thread(target=pyqtloop, args=(numtrain,arr,))
    #t2 = threading.Thread(target=mainloop_1sec, args=(numtrain,))
    t2 = threading.Thread(target=mainloop_fast, args=(numtrain,))
 
    t1.start()
    t2.start()
 
    t1.join()
    t2.join()
    
    
        
if __name__ == "__main__":
    numtrain=1
    arr = [0]*9
    TB_fin(numtrain,arr)
