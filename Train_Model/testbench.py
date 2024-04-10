from PyQt6.QtGui import QIcon
import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton, QGroupBox,
                             QCheckBox, QComboBox, QProgressBar, QLineEdit)

from Train_Model import TrainModelContainer
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
        self.controllerButton.clicked.connect(self.controller_pressed)

        self.blockButton = self.findChild(QPushButton, "blockButton")
        self.blockButton.clicked.connect(self.block_pressed)

        self.passButton = self.findChild(QPushButton, "passButton")
        self.passButton.clicked.connect(self.pass_pressed)

        self.tempButton = self.findChild(QPushButton, "tempButton")
        self.tempButton.clicked.connect(self.temp_pressed)

        self.physButton = self.findChild(QPushButton, "physButton")
        self.physButton.clicked.connect(self.phys_pressed)

        self.addButton = self.findChild(QPushButton, "addButton")
        self.addButton.clicked.connect(self.add_trn)

        self.removeButton = self.findChild(QPushButton, "removeButton")
        self.removeButton.clicked.connect(self.remove_trn)

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
        lst = str(self.trackInput.text()).split(", ", -1)
        if len(lst) != 2:
            return
        # [commanded speed, vital authority]
        input_lst = list()
        input_lst.append(float(lst[0]))
        input_lst.append(int(lst[0]))
        self.container.track_model_inputs(input_lst, 1)

    def controller_pressed(self):
        lst = str(self.controllerInput.text()).split(", ", -1)
        # [commanded speed, power, service brake, emergency brake, left/right doors, announce station, cabin lights,
        # headlights]
        if len(lst) != 8:
            return

        input_list = list()
        input_list.append(float(lst[0]))
        input_list.append(float(lst[1]))
        input_list.append(bool(lst[2]))
        input_list.append(bool(lst[3]))
        input_list.append(int(lst[4]))
        input_list.append(bool(lst[5]))
        input_list.append(bool(lst[7]))
        self.container.train_controller_inputs(input_list, 1)

    def block_pressed(self):
        lst = str(self.blockInput.text()).split(", ", -1)
        # [grade, elevation, block length, underground, beacon]
        if len(lst) != 5:
            return

        input_list = list()
        input_list.append(float(lst[0]))
        input_list.append(float(lst[1]))
        input_list.append(float(lst[2]))
        input_list.append(bool(lst[3]))
        input_list.append(lst[4])
        self.container.track_update_block(input_list, 1)

    def pass_pressed(self):
        self.container.track_update_passengers(int(self.passInput.text()), 1)

    def temp_pressed(self):
        self.container.controller_update_temp(float(self.tempInput.text()), 1)

    def phys_pressed(self):
        self.container.physics_calculation()

    def add_trn(self):
        self.container.add_train()

    def remove_trn(self):
        self.container.remove_train(max(self.container.train_dict.keys()))


contain = TrainModelContainer(TrainController_Tot_Container(SystemTimeContainer()), SystemTimeContainer())
app = QApplication(sys.argv)
ui = ContainerTB(contain)
app.exec()

