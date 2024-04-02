from copy import copy

import os
import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, \
    QListWidgetItem, QButtonGroup, QListWidget
from PyQt6.uic import loadUi

from Track_Controller_SW.BusinessLogic import BusinessLogic
from Track_Controller_SW.switching import Switch


class ManualMode(QWidget):
    switch_changed_signal = pyqtSignal(int)

    def __init__(self, business_logic: BusinessLogic):
        super().__init__()
        self.setWindowTitle('Maintenance Mode')
        self.setMinimumSize(200, 200)
        self.layout = QVBoxLayout(self)
        self.business_logic = business_logic
        self.switches_list = copy(self.business_logic.switches_list)

        self.switch_button_group = QButtonGroup()
        button_id = 0
        for switch in self.switches_list:
            button = self.switch_button_ret(
                size=200,
                text1=f"Switch at Block {switch.block}")

            self.switch_button_group.addButton(button, button_id)
            button_id += 1
            self.layout.addWidget(button)

        self.switch_button_group.buttonClicked.connect(self.switch_button_pressed)

    def switch_button_pressed(self, button: QPushButton) -> None:
        QtCore.QMetaObject.invokeMethod(self, "switch_changed_signal",
                                        QtCore.Q_ARG(int, self.switch_button_group.id(button)))

    def switch_button_ret(self, size=None, text1=None, checkable=True, style1=None, style2=None):
        button = QPushButton()
        button.setCheckable(checkable)
        button.setFixedHeight(24)
        if checkable:
            if text1:
                button.setText(text1)
            else:
                button.setText("Off")
        if size:
            button.setFixedWidth(size)
        return button


class UI(QMainWindow):
    def __init__(self, business_logic):

        super(UI, self).__init__()
        self.fname = "filename"
        self.block_indexes = None
        self.switch_list_widget = None
        self.block_number = None
        self.manual_mode_window = None
        self.lights_list = None

        # load ui
        current_dir = os.path.dirname(__file__)  # setting up to work in any dir
        ui_path = os.path.join(current_dir, 'TrackController.ui')
        try:
            loadUi(ui_path, self)
        except Exception as e:
            print("Error with loading UI file: ", e)

        # Fix the size
        self.setFixedWidth(757)
        self.setFixedHeight(649)

        # Assign attributes
        self.business_logic = business_logic

        # Define widgets
        self.manual_mode = self.findChild(QPushButton, 'manual_mode')
        self.browse_button = self.findChild(QPushButton, 'browse')
        self.filename = self.findChild(QLabel, 'filename')
        # self.occupancy_disp = self.findChild(QListWidget, 'block_number')
        self.light_1_a = self.findChild(QPushButton, 'light_1_a')
        self.light_1_a.setStyleSheet("background-color: rgb(0, 224, 34)")
        self.light_1_b = self.findChild(QPushButton, 'light_1_b')
        self.light_1_b.setStyleSheet("background-color: rgb(222, 62, 38)")
        self.light_2_a = self.findChild(QPushButton, 'light_2_a')
        self.light_2_a.setStyleSheet("background-color: rgb(0, 224, 34)")
        self.light_2_b = self.findChild(QPushButton, 'light_2_b')
        self.light_2_b.setStyleSheet("background-color: rgb(222, 62, 38)")
        self.rr_crossing = self.findChild(QPushButton, 'rr_crossing_button')
        self.rr_crossing.setStyleSheet("background-color: rgb(0, 224, 34)")
        # self.tb_button = self.findChild(QPushButton, 'tb_button')
        self.block_number = self.findChild(QListWidget, 'block_number')

        # Testbench
        # self.tb_window = None

        # Initialize switch list
        self.init_switch_list()

        # Initialize occupancy list
        self.init_occupancy()

        # Initialize lights
        self.init_lights()

        # Initialize filename
        try:
            self.filename.setText(self.business_logic.filepath)
            self.filename.adjustSize()
        except Exception as e:
            print(e)

        # define connections
        self.browse_button.clicked.connect(self.browse_files)
        self.manual_mode.clicked.connect(self.manual_mode_dialogue)
        # self.tb_button.clicked.connect(self.open_tb)

        # outside signals
        self.business_logic.occupancy_signal.connect(self.update_occupancy)
        self.business_logic.switches_signal.connect(self.update_switches)
        self.business_logic.rr_crossing_signal.connect(self.activate_rr_crossing)
        self.business_logic.light_signal.connect(self.update_light)

        # show the app
        self.show()

    # must initialize with business object data, then have it dynamically update when running
    def init_switch_list(self):
        self.switch_list_widget.clear()
        for switch in self.business_logic.switches_list:
            item = QListWidgetItem(switch.to_string())
            self.switch_list_widget.addItem(item)

    # dynamically updating endpoint called by business logic
    @pyqtSlot(list)
    def update_switches(self, switches_arr: list[Switch]) -> None:
        self.switch_list_widget.clear()
        for switch in switches_arr:
            item = QListWidgetItem(switch.to_string())
            self.switch_list_widget.addItem(item)

    # must initialize with business object data, then have it dynamically update when running
    def init_occupancy(self) -> None:
        self.block_indexes = copy(self.business_logic.block_indexes)
        self.block_number.clear()
        for index, occupancy in zip(self.business_logic.block_indexes, self.business_logic.occupancy_list):
            # for occupancy in self.business_logic.occupancy_list:
            item = QListWidgetItem(str(index) + " " + str(occupancy))
            self.block_number.addItem(item)

    # dynamically updating endpoint called by business logic
    @pyqtSlot(list)
    def update_occupancy(self, occupancy_list : list) -> None:
        self.block_number.clear()
        for index, occupancy in zip(self.block_indexes, occupancy_list):
            # for occupancy in self.business_logic.occupancy_list:
            item = QListWidgetItem(str(index) + " " + str(occupancy))
            self.block_number.addItem(item)

    def init_lights(self):
        self.lights_list = copy(self.business_logic.lights_list)
        self.light_1_a.setText(f"Light @ b{self.lights_list[0].block}")
        self.light_1_b.setText(f"Light @ b{self.lights_list[1].block}")
        self.light_2_a.setText(f"Light @ b{self.lights_list[2].block}")
        self.light_2_b.setText(f"Light @ b{self.lights_list[3].block}")

    # only the signal that should be green is sent
    @pyqtSlot(int)
    def update_light(self, light_num: int) -> None:
        if light_num == 0:
            # set light_1_a green
            self.light_1_a.setStyleSheet("background-color: rgb(0, 224, 34)")
            self.light_1_b.setStyleSheet("background-color: rgb(222, 62, 38)")
        elif light_num == 1:
            # set light_1_b green
            self.light_1_b.setStyleSheet("background-color: rgb(0, 224, 34)")
            self.light_1_a.setStyleSheet("background-color: rgb(222, 62, 38)")
        elif light_num == 2:
            # set light_2_a green
            self.light_2_a.setStyleSheet("background-color: rgb(0, 224, 34)")
            self.light_2_b.setStyleSheet("background-color: rgb(222, 62, 38)")
        elif light_num == 3:
            # set light_2_b green
            self.light_2_b.setStyleSheet("background-color: rgb(0, 224, 34)")
            self.light_2_a.setStyleSheet("background-color: rgb(222, 62, 38)")




    def manual_mode_dialogue(self):
        self.manual_mode_window = ManualMode(self.business_logic)
        self.manual_mode_window.switch_changed_signal.connect(self.business_logic.switches_changed)
        self.manual_mode_window.adjustSize()
        self.manual_mode_window.show()
        self.show()



    @pyqtSlot(bool)
    def activate_rr_crossing(self, active_bool: bool) -> None:
        if active_bool:
            self.rr_crossing.setText("Railroad Crossing Active")
            self.rr_crossing.setStyleSheet("background-color: rgb(222, 62, 38)")
        else:
            self.rr_crossing.setText("Railroad Crossing Inactive")
            self.rr_crossing.setStyleSheet("background-color: rgb(0, 224, 34)")

    def browse_files(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open PLC File', 'C:/Users/lucas')
        self.filename.setText(self.fname)
        self.filename.adjustSize()
        self.business_logic.set_plc_filepath(self.fname)
