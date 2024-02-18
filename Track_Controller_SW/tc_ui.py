import functools

import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, \
    QLCDNumber, QListWidgetItem
from PyQt6.uic import loadUi

import TestBench


class ManualMode(QWidget):
    switch_changed_signal = pyqtSignal(int)

    def __init__(self, business_logic):
        super().__init__()
        self.setWindowTitle('Manual Mode')
        self.setMinimumSize(200, 200)
        self.layout = QVBoxLayout(self)
        self.business_logic = business_logic
        self.switches_arr = np.copy(business_logic.switches_arr)

        self.switch_button_dict = {}
        self.button_array = []
        count = 0
        for switch in self.switches_arr:
            count += 1
            button = self.switch_button_ret(
                size=200,
                text1=f"Facing Block {switch.current_pos}",
                text2=f"Facing Block {switch.pos_b if switch.current_pos == switch.pos_a else switch.pos_a}")
            self.layout.addWidget(button)
            self.button_array.append(button)
            self.key = f"switch_button_{count}"
            exec(self.key + '=button')
            # address switches by their button
            self.switch_button_dict[self.key] = switch

    def switch_button_ret(self, size=None, text1=None, text2=None, checkable=True, style1=None, style2=None):
        if text1 and not text2:
            text2 = text1
        button = QPushButton()
        button.setCheckable(checkable)
        button.setFixedHeight(24)
        # button.clicked.connect( functools.partial(button_click1, but=button) )
        if checkable:
            # button.setStyleSheet("background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px")
            if text1:
                button.setText(text1)
            else:
                button.setText("Off")
            button.clicked.connect(
                functools.partial(self.switch_but_tog, but=button, text1=text1, text2=text2, style_on=style1,
                                  style_off=style2))
        else:
            # button.setStyleSheet("background-color: rgb(222, 62, 38); border: 2px solid rgb(222, 0, 0); border-radius: 4px")
            if text1:
                button.setText(text2)
        if size:
            button.setFixedWidth(size)
        return button

    def switch_but_tog(self, but, text1=None, text2=None, style_on=None, style_off=None):
        if but.isChecked():
            # but.setStyleSheet(
            #     f"{style_on if style_on else 'background-color: rgb(143, 186, 255);
            #     border: 2px solid rgb( 42,  97, 184);
            #     border-radius: 6px'}")
            if text1:
                but.setText(text2)
            else:
                but.setText("On")
        else:
            # but.setStyleSheet(
            #     f"{style_off if style_off else 'background-color: rgb(156, 156, 156);
            #     border: 2px solid rgb(100, 100, 100);
            #     border-radius: 6px'}")
            if text1:
                but.setText(text1)
            else:
                but.setText("Off")

        self.handle_toggle(0)

    def update_switch(self, index):

        QtCore.QMetaObject.invokeMethod(self, "switch_changed_signal",
                                        QtCore.Q_ARG(int, index))

    def handle_toggle(self, index):
        self.update_switch(index)


class UI(QMainWindow):
    def __init__(self, plc_logic, business_logic):
        super(UI, self).__init__()
        # load ui
        self.manual_mode_window = None
        loadUi('track_controller.ui', self)

        # Fix the size
        self.setFixedWidth(757)
        self.setFixedHeight(649)

        # Assign attributes
        self.plc_logic = plc_logic
        self.business_logic = business_logic

        # Define widgets
        self.manual_mode = self.findChild(QPushButton, 'manual_mode')
        self.browse_button = self.findChild(QPushButton, 'browse')
        self.filename = self.findChild(QLabel, 'filename')
        self.block_occupied = self.findChild(QLCDNumber, 'block_number')
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
        for switch in self.business_logic.switches_arr:
            item = QListWidgetItem(switch.to_string())
            self.switch_list_widget.addItem(item)

    def open_tb(self):
        if self.tb_window is None or not self.tb_window.isVisible():
            self.tb_window = TestBench.TbMainWindow(self.business_logic)
            self.tb_window.occupancy_changed_signal.connect(self.business_logic.occupancy_changed)
            self.tb_window.switch_changed_signal.connect(self.business_logic.switches_changed)
            self.tb_window.authority_updated.connect(self.business_logic.authority_updated)
            self.tb_window.sug_speed_updated.connect(self.business_logic.sug_speed_updated)
            self.tb_window.show()

    def manual_mode_dialogue(self):
        self.manual_mode_window = ManualMode(self.business_logic)
        self.manual_mode_window.switch_changed_signal.connect(self.business_logic.switches_changed)
        self.manual_mode_window.show()
        self.show()

    @pyqtSlot(int)
    def update_light(self, light_num):
        if light_num == 6:
            self.light_b6.setStyleSheet("background-color: rgb(0, 224, 34)")  # Green
            self.light_b11.setStyleSheet("background-color: rgb(222, 62, 38)")  # Red
        else:
            self.light_b6.setStyleSheet("background-color: rgb(222, 62, 38)")
            self.light_b11.setStyleSheet("background-color: rgb(0, 224, 34)")

    @pyqtSlot(bool)
    def activate_rr_crossing(self, active_bool):
        if active_bool:
            self.rr_crossing.setText("Railroad Crossing Active")
            self.rr_crossing.setStyleSheet("background-color: rgb(222, 62, 38)")
        else:
            self.rr_crossing.setText("Railroad Crossing Inactive")
            self.rr_crossing.setStyleSheet("background-color: rgb(0, 224, 34)")

    @pyqtSlot(list)
    def update_occupancy(self, occupancy_arr):
        block = np.argmax(occupancy_arr)
        self.block_occupied.display(block)
        self.show()

    @pyqtSlot(list)
    def update_switches(self, switches_arr):
        self.switch_list_widget.clear()
        for switch in switches_arr:
            item = QListWidgetItem(switch.to_string())
            self.switch_list_widget.addItem(item)

    def browse_files(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open PLC File', 'C:/Users/lucas')
        self.filename.setText(fname)
        self.filename.adjustSize()

        self.plc_logic.set_filepath(fname)
