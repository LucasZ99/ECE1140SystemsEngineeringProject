from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QTextEdit, QPushButton, QTableWidget, QGroupBox,
                             QCheckBox, QComboBox, QProgressBar)
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
        self.primeGroup = self.findChild(QGroupBox, "primeGroup")
        self.trainSelect = self.findChild(QComboBox, "trainSelect")
        self.emerButton = self.findChild(QPushButton, "emerButton")
        self.tbCheck = self.findChild(QCheckBox, "tbCheck")

        self.phyGroup = self.findChild(QGroupBox, "phyGroup")
        self.powerValue = self.findChild(QLabel, "powerValue")
        self.accValue = self.findChild(QLabel, "accValue")
        self.speedValue = self.findChild(QLabel, "speedValue")
        self.totMassValue = self.findChild(QLabel, "totMassValue")
        self.gradeValue = self.findChild(QLabel, "gradeValue")
        self.elevValue = self.findChild(QLabel, "elevLabel")
        self.pBrakeValue = self.findChild(QProgressBar, "pBrakeValue")
        self.sBrakeValue = self.findChild(QProgressBar, "sBrakeValue")
        self.dBrakeValue = self.findChild(QProgressBar, "dBrakeValue")

        self.trainGroup = self.findChild(QGroupBox, "trainGroup")
        self.lengthValue = self.findChild(QLabel, "lengthValue")
        self.heightValue = self.findChild(QLabel, "heightValue")
        self.widthValue = self.findChild(QLabel, "widthValue")
        self.carsValue = self.findChild(QLabel, "carsValue")
        self.trainMassValue = self.findChild(QLabel, "trainMassValue")
        self.crewValue = self.findChild(QLabel, "crewValue")
        self.passValue = self.findChild(QLabel, "passValue")

        self.failGroup = self.findChild(QGroupBox, "failGroup")

        self.transGroup = self.findChild(QGroupBox, "transGroup")

        self.opGroup = self.findChild(QGroupBox, "opGroup")

        self.phyGroup_tb = self.findChild(QGroupBox, "phyGroup_tb")

        self.trainGroup_tb = self.findChild(QGroupBox, "trainGroup_tb")

        self.transGroup_tb = self.findChild(QGroupBox, "transGroup_tb")

        self.opGroup_tb = self.findChild(QGroupBox, "opGroup_tb")

        # define behavior
        self.phyGroup_tb.hide()
        self.trainGroup_tb.hide()
        self.transGroup_tb.hide()
        self.opGroup_tb.hide()
        self.tb = False
        self.tbCheck.stateChanged.connect(self.tb_toggle)

        # show the app
        self.show()

    def tb_toggle(self):
        if self.tb:
            self.phyGroup.show()
            self.trainGroup.show()
            self.transGroup.show()
            self.opGroup.show()

            self.phyGroup_tb.hide()
            self.trainGroup_tb.hide()
            self.transGroup_tb.hide()
            self.opGroup_tb.hide()
            self.tb = False
        else:
            self.phyGroup.hide()
            self.trainGroup.hide()
            self.transGroup.hide()
            self.opGroup.hide()

            self.phyGroup_tb.show()
            self.trainGroup_tb.show()
            self.transGroup_tb.show()
            self.opGroup_tb.show()
            self.tb = True


# initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec()
