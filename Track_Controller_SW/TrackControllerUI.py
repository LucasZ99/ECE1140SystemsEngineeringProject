import functools

import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, \
    QLCDNumber, QListWidgetItem, QButtonGroup
from PyQt6.uic import loadUi

import TestBench
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
        self.switches_list = np.copy(business_logic.switches_list)


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

        self.switch_list_widget = None
        self.manual_mode_window = None
        # load ui
        loadUi('TrackController.ui', self)

        # Fix the size
        self.setFixedWidth(757)
        self.setFixedHeight(649)

        # Assign attributes
        self.business_logic = business_logic

        # Define widgets
        self.manual_mode = self.findChild(QPushButton, 'manual_mode')
        self.browse_button = self.findChild(QPushButton, 'browse')
        self.filename = self.findChild(QLabel, 'filename')
        self.occupancy_disp = self.findChild(QLCDNumber, 'block_number')
        self.light_b6 = self.findChild(QPushButton, 'light_b6')
        self.light_b6.setStyleSheet("background-color: rgb(0, 224, 34)")
        self.light_b11 = self.findChild(QPushButton, 'light_b11')
        self.light_b11.setStyleSheet("background-color: rgb(222, 62, 38)")

        self.rr_crossing = self.findChild(QPushButton, 'rr_crossing_button')
        self.rr_crossing.setStyleSheet("background-color: rgb(0, 224, 34)")
        self.tb_button = self.findChild(QPushButton, 'tb_button')

        # Testbench
        self.tb_window = None

        # Initialize switch list
        self.update_switch_list()

        # define connections
        self.browse_button.clicked.connect(self.browse_files)
        self.manual_mode.clicked.connect(self.manual_mode_dialogue)
        self.tb_button.clicked.connect(self.open_tb)

        # outside signals
        self.business_logic.occupancy_signal.connect(self.update_occupancy)
        self.business_logic.switches_signal.connect(self.update_switches)
        self.business_logic.rr_crossing_signal.connect(self.activate_rr_crossing)
        self.business_logic.light_signal.connect(self.update_light)

        # show the app
        self.show()

    def update_switch_list(self):
        self.switch_list_widget.clear()
        for switch in self.business_logic.switches_list:
            item = QListWidgetItem(switch.to_string())
            self.switch_list_widget.addItem(item)

    def open_tb(self):
        if self.tb_window is None or not self.tb_window.isVisible():
            self.tb_window = TestBench.TbMainWindow(self.business_logic)
            self.tb_window.occupancy_changed_signal.connect(self.business_logic.occupancy_changed)
            self.tb_window.switch_changed_signal.connect(self.business_logic.switches_changed)
            self.tb_window.authority_updated_signal.connect(self.business_logic.authority_updated)
            self.tb_window.sug_speed_updated_signal.connect(self.business_logic.sug_speed_updated)
            self.tb_window.show()

    def manual_mode_dialogue(self):
        self.manual_mode_window = ManualMode(self.business_logic)
        self.manual_mode_window.switch_changed_signal.connect(self.business_logic.switches_changed)
        self.manual_mode_window.show()
        self.show()

    @pyqtSlot(int)
    def update_light(self, light_num: int) -> None:
        if light_num == 6:
            self.light_b6.setStyleSheet("background-color: rgb(0, 224, 34)")  # Green
            self.light_b11.setStyleSheet("background-color: rgb(222, 62, 38)")  # Red
        elif light_num == 11:
            self.light_b6.setStyleSheet("background-color: rgb(222, 62, 38)")
            self.light_b11.setStyleSheet("background-color: rgb(0, 224, 34)")

    @pyqtSlot(bool)
    def activate_rr_crossing(self, active_bool: bool) -> None:
        if active_bool:
            self.rr_crossing.setText("Railroad Crossing Active")
            self.rr_crossing.setStyleSheet("background-color: rgb(222, 62, 38)")
        else:
            self.rr_crossing.setText("Railroad Crossing Inactive")
            self.rr_crossing.setStyleSheet("background-color: rgb(0, 224, 34)")

    @pyqtSlot(list)
    def update_occupancy(self, occupancy_arr: list) -> None:
        block = np.argmax(occupancy_arr)
        self.occupancy_disp.display(block)
        self.show()

    @pyqtSlot(list)
    def update_switches(self, switches_arr: list[Switch]) -> None:
        self.switch_list_widget.clear()
        for switch in switches_arr:
            item = QListWidgetItem(switch.to_string())
            self.switch_list_widget.addItem(item)

    def browse_files(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open PLC File', 'C:/Users/lucas')
        self.filename.setText(fname)
        self.filename.adjustSize()
        self.business_logic.set_plc_filepath(self.filename)
