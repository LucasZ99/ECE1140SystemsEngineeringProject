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

class SW_UI_JEB382(QMainWindow):
    def __init__(self,numtrain,Driver_arr,TrainModel_arr):
        super(SW_UI_JEB382, self).__init__()
        self.setWindowTitle('TrainControllerHW SW_UI #'+str(numtrain))
        
        self.TB_window = TestBench_JEB382(numtrain,TrainModel_arr)

        l = QVBoxLayout()
        button1 = QPushButton("Push for Window 1")
        button1.clicked.connect(self.toggle_TB)
        l.addWidget(button1)

        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

    def toggle_TB(self, checked):
        if self.TB_window.isVisible():
            self.TB_window.hide()
        else:
            self.TB_window.show()
    
    #code when window closes
    def closeEvent(self, *args, **kwargs):
        super(SW_UI_JEB382, self).closeEvent(*args, **kwargs)
        self.TB_window.hide()
        self.TB_window.Thread1_active = False
        print("close")




#=============================

def SW_mainloop_fast(numtrain):
    while True:
        if w:
            if w.TB_window.isVisible():
                print(f"TB TrainC #{numtrain}",TrainModel_arr)
                w.TB_window.updatetick()
                if not w.TB_window.Thread1_active: break
        
        
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