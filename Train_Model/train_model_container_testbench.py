import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton,  QComboBox, QLineEdit)

from Train_Model import TrainModelContainer, UITrain
from Train_Model.train_model_signals import train_model_signals
from TopLevelSignals import TopLevelSignals
from Train_Model.business_logic import train_business_logic


class ContainerTB(QMainWindow):

    def __init__(self, container: TrainModelContainer):
        super(ContainerTB, self).__init__()
        self.container = container
        self.business_logic = train_business_logic
        self.train_ui = UITrain()
        self.train_name_list = list()
        self.index = int()
        self.auth_speed_dict = dict()
        self.block_dict = dict()
        self.passenger_dict = dict()
        self.signals = train_model_signals
        self.top_signals = TopLevelSignals

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

        self.trainControllerUpdateButton = self.findChild(QPushButton, "trainControllerUpdateButton")
        self.trainControllerUpdateButton.clicked.connect(self.business_logic.train_update_controller)

        self.bigUpdateButton = self.findChild(QPushButton, "bigUpdateButton")
        self.bigUpdateButton.clicked.connect(self.big_update_pressed)

        self.trainSelect = self.findChild(QComboBox, "trainSelect")
        self.trainSelect.clear()
        self.trainSelect.currentIndexChanged.connect(self.combo_selection)

        # line edits
        self.trackInput = self.findChild(QLineEdit, "trackInput")
        self.controllerInput = self.findChild(QLineEdit, "controllerInput")
        self.blockInput = self.findChild(QLineEdit, "blockInput")
        self.passInput = self.findChild(QLineEdit, "passInput")
        self.tempInput = self.findChild(QLineEdit, "tempInput")
        self.beaconInput = self.findChild(QLineEdit, "beaconInput")

        self.trackInput.setText("0, 0")
        self.controllerInput.setText("0, 0, False, False, 0, , True, False")
        self.blockInput.setText('0, 0, False')
        self.beaconInput.setText("0"*128)
        self.passInput.setText("0")
        self.tempInput.setText("68")

        self.show()

    def container_ui(self):
        self.train_ui.show()

    def track_pressed(self):
        index = self.get_current_index()
        if index <= 0:
            return
        lst = str(self.trackInput.text()).split(", ", -1)
        if len(lst) != 2:
            return
        # [commanded speed, vital authority]
        input_lst = list()
        input_lst.append(float(lst[0]))
        input_lst.append(int(lst[1]))
        input_lst = tuple(input_lst)
        self.auth_speed_dict[index] = input_lst
        self.signals.tb_track_model_inputs.emit(input_lst, index)

    def controller_pressed(self):
        index = self.get_current_index()
        if index <= 0:
            return
        lst = str(self.controllerInput.text()).split(", ", -1)
        # [commanded speed, power, service brake, emergency brake, left/right doors, announce station, cabin lights,
        # headlights]
        if len(lst) != 8:
            return

        input_list = list()
        input_list.append(lst[0])
        input_list.append(float(lst[1]))
        input_list.append(lst[2] == "True")
        input_list.append(lst[3] == "True")
        input_list.append(int(lst[4]))
        input_list.append(lst[5])
        input_list.append(lst[6] == "True")
        input_list.append(lst[7] == "True")
        input_list = tuple(input_list)
        self.signals.tb_train_controller_inputs.emit(input_list, index)

    def block_pressed(self):
        index = self.get_current_index()
        if index <= 0:
            return
        lst = str(self.blockInput.text()).split(", ", -1)
        # [grade, elevation, underground, beacon]
        if len(lst) != 3:
            return

        input_list = list()
        input_list.append(float(lst[0]))
        input_list.append(float(lst[1]))
        input_list.append(lst[2] == "True")
        input_list.append(str(self.beaconInput.text()))
        input_list = tuple(input_list)
        self.block_dict[index] = input_list
        self.signals.tb_track_update_block.emit(input_list, index)

    def pass_pressed(self):
        index = self.get_current_index()
        if index <= 0:
            return

        passengers = int(self.passInput.text())
        self.passenger_dict[index] = passengers
        self.signals.tb_track_update_passenger.emit(passengers, index)

    def temp_pressed(self):
        index = self.get_current_index()
        if index <= 0:
            return
        self.signals.tb_controller_update_temp.emit(float(self.tempInput.text()), index)

    def phys_pressed(self):
        self.signals.tb_physics_calculation.emit()

    def add_trn(self):
        self.signals.tb_add_train.emit()
        index = max(self.business_logic.train_dict.keys())
        self.train_name_list.append(f'Train {index}')
        self.trainSelect.addItem(f'Train {index}')
        self.auth_speed_dict[index] = (0, 0)

    def remove_trn(self):
        index = self.get_current_index()
        if index <= 0:
            return
        self.trainSelect.clear()
        self.train_name_list.remove(f'Train {index}')
        for name in self.train_name_list:
            self.trainSelect.addItem(name)
        if len(self.train_name_list) != 0:
            self.combo_selection()
        self.signals.tb_remove_train.emit(index)

    def combo_selection(self):
        if len(self.train_name_list) == 0:
            return
        string = str(self.trainSelect.currentText())
        if not ('Train' in string):
            return
        self.index = int(string[6:])

    def get_current_index(self):
        string = str(self.trainSelect.currentText())
        if not ("Train" in string):
            return -1
        return int(string[6:])

    def big_update_pressed(self):
        self.top_signals.update_train_model_from_track_model.emit(self.auth_speed_dict, self.block_dict, False, -1,
                                                                  self.passenger_dict)


contain = TrainModelContainer()
app = QApplication(sys.argv)
ui = ContainerTB(contain)
app.exec()
