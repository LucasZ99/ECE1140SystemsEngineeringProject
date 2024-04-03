from PyQt6.QtGui import QIcon
import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton, QGroupBox,
                             QCheckBox, QComboBox, QProgressBar, QLineEdit)
from PyQt6.QtCore import pyqtSignal

import random

from Train_Model import TrainModel, TrainBusinessLogic, TrainModelContainer
from trainControllerTot_Container import TrainController_Tot_Container
from SystemTime import SystemTimeContainer


class ContainerTB(QMainWindow):

    def __init__(self, container: TrainModelContainer):
        super(ContainerTB, self).__init__()
        self.container = container

        # load the ui file
        current_dir = os.path.dirname(__file__)  # setting up to work in any dir
        ui_path = os.path.join(current_dir, 'testbench.ui')
        try:
            uic.loadUi(ui_path, self)
        except Exception as e:
            print("Error with loading UI file: ", e)
        # buttons
        self.uiButton = self.findChild(QPushButton, "uiButton")
        self.uiButton.clicked.connect(self.container_ui)

        self.trackButton = self.findChild(QPushButton, "tracButton")
        self.trackButton.clicked.connect(self.track_pressed)

        self.controllerButton = self.findChild(QPushButton, "controllerButton")
        self.blockButton = self.findChild(QPushButton, "blockButton")
        self.passButton = self.findChild(QPushButton, "passButton")
        self.tempButton = self.findChild(QPushButton, "tempButton")
        self.physButton = self.findChild(QPushButton, "physButton")
        self.addButton = self.findChild(QPushButton, "addButton")
        self.addButton.clicked.connect(self.add_trn)

        self.removeButton = self.findChild(QPushButton, "removeButton")

        # line edits
        self.trackInput = self.findChild(QLineEdit, "trackInput")
        self.controllerInput = self.findChild(QLineEdit, "controllerInput")
        self.blockInput = self.findChild(QLineEdit, "blockInput")
        self.passInput = self.findChild(QLineEdit, "passInput")
        self.tempInput = self.findChild(QLineEdit, "tempInput")

        self.trackInput.setText("0, 0")
        self.controllerInput.setText("0, 0, False, False, 0, , True, False")
        self.blockInput.setText("0, 0, 50, False, ")
        self.passInput.setText("0")
        self.tempInput.setText("68")

        self.show()

    def container_ui(self):
        self.container.show_ui()

    def track_pressed(self):
        lst = str(self.trackInput.text()).split(",", -1)
        if len(lst) != 2:
            return
        input_lst = list()
        input_lst.append(float(lst[0]))
        input_lst.append(float(lst[0]))
        self.container.track_model_inputs(input_lst, 1)

    def add_trn(self):
        self.container.add_train()


contain = TrainModelContainer(TrainBusinessLogic(), TrainController_Tot_Container(True), SystemTimeContainer())
app = QApplication(sys.argv)
ui = ContainerTB(contain)
app.exec()

