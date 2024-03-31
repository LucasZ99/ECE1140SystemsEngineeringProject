import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from Train_Model import UITrain

print("hello")
app = QApplication(sys.argv)
ui = UITrain()
ui.show()
app.exec()