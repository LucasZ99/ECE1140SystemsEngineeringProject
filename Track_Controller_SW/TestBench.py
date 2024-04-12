import itertools
import sys
from copy import copy

import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, QCoreApplication, pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QComboBox, QCheckBox, QGroupBox, \
    QLineEdit

from Track_Controller_SW.BusinessLogic import BusinessLogic


class TbMainWindow(QMainWindow):
    occupancy_changed_signal = pyqtSignal(list)
    switch_changed_signal = pyqtSignal(int)
    authority_updated_signal = pyqtSignal(bool)
    sug_speed_updated_signal = pyqtSignal(float)

    def __init__(self, business_logic: BusinessLogic):
        super(TbMainWindow, self).__init__()
        try:
            self.business_logic = business_logic
            self.occupancy_dict = business_logic.occupancy_dict
            self.block_list = copy(list(business_logic.occupancy_dict.keys()))
            self.occupancy_list = copy(list(business_logic.occupancy_dict.values()))
            self.switches_list = copy(business_logic.switches_list)

            self.setObjectName("MainWindow")
            self.resize(369, 365)
            self.setMinimumSize(369, 365)
            self.setMaximumSize(369, 365)
            self.centralwidget = QWidget(parent=self)
            self.centralwidget.setObjectName("centralwidget")

            self.sug_speed = QLineEdit(parent=self.centralwidget)
            self.sug_speed.setGeometry(140, 210, 104, 31)
            self.sug_speed.setObjectName("textEdit")

            self.label_4 = QLabel(parent=self.centralwidget)
            self.label_4.setGeometry(28, 40, 95, 16)
            self.label_4.setObjectName("label_4")

            self.comboBox_3 = QComboBox(parent=self.centralwidget)
            self.comboBox_3.setGeometry(140, 40, 71, 22)
            self.comboBox_3.setObjectName("comboBox_3")

            for i in self.block_list:
                self.comboBox_3.addItem(f"Block {i}")

            self.groupBox = QGroupBox(parent=self.centralwidget)
            self.groupBox.setGeometry(9, 89, 351, 233)
            self.groupBox.setObjectName("groupBox")

            self.label = QLabel(parent=self.groupBox)
            self.label.setGeometry(40, 80, 81, 20)
            self.label.setObjectName("label")

            self.comboBox = QComboBox(parent=self.groupBox)
            self.comboBox.setGeometry(130, 80, 81, 22)
            self.comboBox.setObjectName("comboBox")

            for i in self.switches_list:
                self.comboBox.addItem(str(i))
                self.comboBox.adjustSize()

            self.label_2 = QLabel(parent=self.groupBox)
            self.label_2.setGeometry(70, 30, 51, 20)
            self.label_2.setObjectName("label_2")

            self.authority_check = QCheckBox(parent=self.groupBox)
            self.authority_check.setGeometry(160, 15, 50, 50)
            self.authority_check.setObjectName("authority_check")

            self.switch_button = QPushButton(parent=self.groupBox)
            self.switch_button.setGeometry(285, 75, 60, 30)
            self.switch_button.setObjectName("switch_button")

            self.label_6 = QLabel(parent=self.groupBox)
            self.label_6.setGeometry(240, 120, 51, 20)
            self.label_6.setObjectName("label_6")

            self.label_7 = QLabel(parent=self.groupBox)
            self.label_7.setGeometry(120, 10, 131, 20)
            self.label_7.setText("")
            self.label_7.setObjectName("label_7")

            self.label_8 = QLabel(parent=self.groupBox)
            self.label_8.setGeometry(130, 100, 121, 20)
            self.label_8.setText("")
            self.label_8.setObjectName("label_8")

            self.groupBox_2 = QGroupBox(parent=self.centralwidget)
            self.groupBox_2.setGeometry(8, 10, 351, 71)
            self.groupBox_2.setObjectName("groupBox_2")

            self.show_button = QPushButton(parent=self.groupBox_2)
            self.show_button.setGeometry(240, 40, 75, 24)
            self.show_button.setObjectName("pushButton")

            self.checkBox_3 = QCheckBox(parent=self.centralwidget)
            self.checkBox_3.setGeometry(250, 30, 74, 20)
            self.checkBox_3.setObjectName("checkBox_3")

            self.label_5 = QLabel(parent=self.centralwidget)
            self.label_5.setGeometry(40, 210, 91, 20)
            self.label_5.setObjectName("label_5")

            self.groupBox.raise_()
            self.groupBox_2.raise_()
            self.sug_speed.raise_()
            self.show_button.raise_()
            self.label_4.raise_()
            self.comboBox_3.raise_()
            self.checkBox_3.raise_()
            self.label_5.raise_()

            self.setCentralWidget(self.centralwidget)

            self.retranslate_ui(self)

            # Events:
            self.switch_button.clicked.connect(self.sw_toggle_handler)
            self.show_button.clicked.connect(self.print_blocks)
            self.checkBox_3.clicked.connect(self.bl_occupancy_handler)
            self.comboBox_3.currentIndexChanged.connect(self.bl_status_handler)
            self.authority_check.stateChanged.connect(self.auth_handler)
            self.sug_speed.editingFinished.connect(self.sug_speed_text_handler)

            # Outside events
            self.business_logic.switches_signal.connect(self.update_switches)

            self.show()
        except Exception as e:
            print(e)

    def retranslate_ui(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Track Controller Test Bench"))
        self.show_button.setText(_translate("MainWindow", "Show Blocks"))
        self.show_button.adjustSize()
        self.label_4.setText(_translate("MainWindow", "Block Occupancy:"))
        self.groupBox.setTitle(_translate("MainWindow", "Inputs from CTC:"))
        self.label.setText(_translate("MainWindow", "Switch Selection:"))
        self.label.adjustSize()
        self.label_2.setText(_translate("MainWindow", "Authority:"))
        self.switch_button.setText(_translate("MainWindow", "Toggle"))
        self.label_6.setText(_translate("MainWindow", "m/s"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Inputs from Track Model:"))
        self.checkBox_3.setText(_translate("MainWindow", "Occupied"))
        self.label_5.setText(_translate("MainWindow", "Suggested Speed:"))

    @pyqtSlot(list)
    def update_switches(self, switch_list: list):
        self.comboBox.clear()
        for switch in switch_list:
            self.comboBox.addItem(str(switch))
            self.comboBox.adjustSize()

    # Handlers:
    def sw_toggle_handler(self):
        self.business_logic.switches_changed(self.comboBox.currentIndex())

    def bl_status_handler(self):  # New block is selected from the dropdown menu
        if self.occupancy_list[self.comboBox_3.currentIndex()] == False:
            self.checkBox_3.setChecked(False)
        else:
            self.checkBox_3.setChecked(True)
        pass

    def bl_occupancy_handler(self):  # The block occupancy status of a block is altered

        if self.checkBox_3.isChecked():
            self.occupancy_list[self.comboBox_3.currentIndex()] = True
        else:
            self.occupancy_list[self.comboBox_3.currentIndex()] = False

        self.occupancy_dict.update(dict(itertools.islice(self.occupancy_list, 0)))
        self.business_logic.occupancy_changed(self.occupancy_dict)

    def auth_handler(self):  # When the checkbox is changed for authority
        pass

    def sug_speed_text_handler(self):
        # text = self.sug_speed.text()  # checking to see if it is a valid integer
        # if text.isnumeric() or text.replace(".", "").isnumeric():  # text must be an int or float
        #     value = float(text)
        #     if value <= 0:
        #         self.label_8.setText("must be a positive value")
        #         self.label_8.setStyleSheet("color: red")
        #         self.show_button.setEnabled(False)
        #     else:
        #         self.label_8.clear()
        #         self.update_sug_speed(value)
        # else:
        #     self.label_8.setText("must be a positive number")
        #     self.label_8.setStyleSheet("color: red")
        #     self.show_button.setEnabled(False)
        pass

    def update_sug_speed(self, value: float) -> None:
        pass

    def update_occupancy(self, blocks: list):
        pass

    def print_blocks(self):
        pass
