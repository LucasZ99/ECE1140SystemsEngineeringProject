import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QGridLayout, QTableWidget, QGroupBox, QVBoxLayout,
    QTableWidget, QLabel, QSlider, QComboBox, QFileDialog, QTableView, QTableWidgetItem, QMainWindow,
    QFrame, QHeaderView, QAbstractScrollArea
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
from Track_Model.animated_toggle import AnimatedToggle
import sys
from Track_Model.Track_Model import TrackModel
from Track_Model.dynamic_map import DynamicMap
import numpy as np


##############################
# Main Window
##############################
class TestBenchWindow(QWidget):
    apply_clicked = pyqtSignal(float, float, object, object, object, object, object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test Bench')
        # StyleSheet copied from main UI
        self.setStyleSheet("""
                    QMainWindow{
                        background-color: #d9d9d9;
                    }
                    QGroupBox {
                        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                          stop: 0 #d9d9d9, stop: 1 #FFFFFF);
                        border: 2px solid black;
                        border-radius: 5px;
                        margin-top: 5ex; /* leave space at the top for the title */
                    }  

                    QGroupBox::title {
                        subcontrol-origin: margin;
                        subcontrol-position: top left; /* position at the top center */
                        padding: 0 3px;
                    }

                    QTableWidget {
                        font: 12px;
                        gridline-color: black;
                    }

                    QHeaderView {
                        font: 12px;
                    }

                    QHeaderView::section {
                        font: 12px;
                        border: 1px solid black;
                    }

                """)

        ####################
        # Backend
        ####################
        # Hard Coded for right now, but should initialize based on track model data
        self.commanded_speed = 0
        self.authority = 0
        # [block, value]
        self.switches = {5: 0}
        self.lights = {6: 0, 11: 0}
        self.rxr = {3: 0}
        self.train_presence = np.zeros(15)
        self.disembarking_passengers = {  # Hashmap
            'Station B': 0,
            'Station C': 0
        }
        ####################
        # Frontend
        ####################

        layout = QVBoxLayout()
        self.setLayout(layout)

        track_controller_group = QGroupBox('Track Controller')
        track_controller_layout = QGridLayout()
        # Labels
        track_controller_layout.addWidget(QLabel('Commanded Speed:'), 0, 0)
        track_controller_layout.addWidget(QLabel('Authority:'), 1, 0)
        track_controller_layout.addWidget(QLabel('Switch Position:'), 2, 0)
        track_controller_layout.addWidget(QLabel('Signal Activation:'), 3, 0)
        track_controller_layout.addWidget(QLabel('Rail Road Crossing:'), 4, 0)
        track_controller_group.setLayout(track_controller_layout)
        layout.addWidget(track_controller_group)
        # QLineEdits
        self.commanded_speed_input = QLineEdit()
        self.commanded_speed_input.setPlaceholderText('(m/s)')
        self.commanded_speed_input.textChanged.connect(self.commanded_speed_input_text_changed)
        track_controller_layout.addWidget(self.commanded_speed_input, 0, 1)
        self.authority_input = QLineEdit()
        self.authority_input.setPlaceholderText('(m)')
        self.authority_input.textChanged.connect(self.authority_input_text_changed)
        track_controller_layout.addWidget(self.authority_input, 1, 1)
        # ComboBoxes
        self.str_list_blocks = list(np.arange(1, 16).astype(str))
        self.combo1 = QComboBox()
        self.combo1.addItem('5')
        self.combo1.activated.connect(self.combo1_new_item_selected)
        self.combo2 = QComboBox()
        self.combo2.addItems(['6', '11'])
        self.combo2.activated.connect(self.combo2_new_item_selected)
        self.combo3 = QComboBox()
        self.combo3.addItem('3')
        self.combo3.activated.connect(self.combo3_new_item_selected)
        self.combo1.setFixedSize(50, 25)
        self.combo2.setFixedSize(50, 25)
        self.combo3.setFixedSize(50, 25)
        track_controller_layout.addWidget(self.combo1, 2, 1)
        track_controller_layout.addWidget(self.combo2, 3, 1)
        track_controller_layout.addWidget(self.combo3, 4, 1)
        # Toggles
        self.toggle1 = AnimatedToggle()
        self.toggle1.setFixedSize(self.toggle1.sizeHint())
        self.toggle1.clicked.connect(self.toggle1_clicked)
        self.toggle2 = AnimatedToggle()
        self.toggle2.setFixedSize(self.toggle2.sizeHint())
        self.toggle2.clicked.connect(self.toggle2_clicked)
        self.toggle3 = AnimatedToggle()
        self.toggle3.setFixedSize(self.toggle3.sizeHint())
        self.toggle3.clicked.connect(self.toggle3_clicked)
        track_controller_layout.addWidget(self.toggle1, 2, 2)
        track_controller_layout.addWidget(self.toggle2, 3, 2)
        track_controller_layout.addWidget(self.toggle3, 4, 2)
        # PushButtons
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_button_clicked)
        track_controller_layout.addWidget(self.apply_button, 5, 2)

        train_model_group = QGroupBox('Train Model')
        train_model_layout = QGridLayout()

        # labels
        train_model_layout.addWidget(QLabel('Train Presence:'), 0, 0)
        train_model_layout.addWidget(QLabel('Disembarking Passengers:'), 1, 0)
        # combobox/toggle combo
        self.combo4 = QComboBox()
        self.combo4.addItems(self.str_list_blocks)
        self.combo4.activated.connect(self.combo4_new_item_selected)
        self.combo4.setFixedSize(50, 25)
        self.toggle4 = AnimatedToggle()
        self.toggle4.setFixedSize(self.toggle4.sizeHint())
        self.toggle4.clicked.connect(self.toggle4_clicked)
        train_model_layout.addWidget(self.combo4, 0, 1)
        train_model_layout.addWidget(self.toggle4, 0, 2)

        train_model_group.setLayout(train_model_layout)
        layout.addWidget(train_model_group)
        # forms
        self.station_input = QComboBox()
        self.station_input.addItems(['Station B', 'Station C'])
        self.station_input.activated.connect(self.station_input_changed)
        train_model_layout.addWidget(self.station_input, 2, 0)
        self.num_input = QLineEdit()
        self.num_input.setPlaceholderText('Disembarking Passengers')
        self.num_input.textChanged.connect(self.disembarking_input_text_changed)
        train_model_layout.addWidget(self.num_input, 2, 1)
        self.apply_button2 = QPushButton("Apply")
        self.apply_button2.clicked.connect(self.apply_button_clicked)
        train_model_layout.addWidget(self.apply_button2, 3, 2)

    def combo1_new_item_selected(self):
        # sets the value of the toggle based on the value from our data
        block = int(self.combo1.currentText())
        self.toggle1.setChecked(self.switches[block])

    def combo2_new_item_selected(self):
        # sets the value of the toggle based on the value from our data
        block = int(self.combo2.currentText())
        self.toggle2.setChecked(self.lights[block])

    def combo3_new_item_selected(self):
        # sets the value of the toggle based on the value from our data
        block = int(self.combo3.currentText())
        self.toggle3.setChecked(self.rxr[block])

    def combo4_new_item_selected(self):
        # sets the value of the toggle based on the value from our data
        block = int(self.combo4.currentText())
        self.toggle4.setChecked(bool(self.train_presence[block-1]))

    def toggle1_clicked(self):
        block = int(self.combo1.currentText())
        val = int(self.toggle1.isChecked())
        self.switches[block] = val
        # refresh data and tables

    def toggle2_clicked(self):
        block = int(self.combo2.currentText())
        val = int(self.toggle2.isChecked())
        self.lights[block] = val

    def toggle3_clicked(self):
        block = int(self.combo2.currentText())
        val = int(self.toggle2.isChecked())
        self.rxr[block] = val

    def toggle4_clicked(self):
        block = int(self.combo4.currentText())
        val = int(self.toggle4.isChecked())
        self.train_presence[block-1] = val
        print(self.train_presence)

    def apply_button_clicked(self):
        self.apply_clicked.emit(
            self.commanded_speed, self.authority, self.switches,
            self.lights, self.rxr, self.train_presence, self.disembarking_passengers
        )

    def commanded_speed_input_text_changed(self):
        self.commanded_speed = self.commanded_speed_input.text()

    def authority_input_text_changed(self):
        self.authority = self.authority_input.text()

    def station_input_changed(self):
        print(str(self.station_input.currentText()))
        print(self.disembarking_passengers)
        print(self.disembarking_passengers[str(self.station_input.currentText())])
        self.num_input.setText(str(self.disembarking_passengers[str(self.station_input.currentText())]))

    def disembarking_input_text_changed(self):
        self.disembarking_passengers[self.station_input.currentText()] = int(self.num_input.text())

    def display(self):
        self.show()


# app = QApplication([])
# window = TestBenchWindow()
# window.show()
# app.exec()
