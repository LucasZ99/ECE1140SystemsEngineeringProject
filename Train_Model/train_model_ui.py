from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTextEdit, QPushButton, QTableWidget
from PyQt5 import uic
import sys


class UI(QMainWindow):
    # constants
    tons_per_kilogram = 0.00110231
    feet_per_meter = 3.28084

    def __init__(self):
        super(UI, self).__init__()

        # load the ui file
        uic.loadUi("Train_Model_UI.ui", self)

        # define widgets
        self.table1 = self.findChild(QTableWidget, "pCalcTable")
        self.table2 = self.findChild(QTableWidget, "pCalcTable_2")
        self.button = self.findChild(QPushButton, "pushButton")

        # define behavior
        self.button.clicked.connect(self.clicker)
        self.table2.hide()
        self.table1_hidden = False

        # show the app
        self.show()

    def clicker(self):
        if self.table1_hidden:
            self.table1.show()
            self.table2.hide()
            self.table1_hidden = False
        else:
            self.table1.hide()
            self.table2.show()
            self.table1_hidden = True


# initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec()
