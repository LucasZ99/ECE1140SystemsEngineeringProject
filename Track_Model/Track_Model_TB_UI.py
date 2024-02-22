import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QGridLayout, QTableWidget, QGroupBox, QVBoxLayout,
    QTableWidget, QLabel, QSlider, QComboBox, QFileDialog, QTableView, QTableWidgetItem, QMainWindow,
    QFrame, QHeaderView, QAbstractScrollArea
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from Animated_Toggle import AnimatedToggle
import sys
from Track_Model import TrackModel
from dynamic_map import DynamicMap
import numpy as np


##############################
# Main Window
##############################
class TestBenchWindow(QWidget):
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
        track_controller_layout.addWidget(self.commanded_speed_input, 0, 1)
        self.authority_input = QLineEdit()
        self.authority_input.setPlaceholderText('(m)')
        track_controller_layout.addWidget(self.authority_input, 1, 1)
        # ComboBoxes
        self.str_list_blocks = list(np.arange(1, 16).astype(str))
        self.combo1 = QComboBox()
        self.combo1.addItems(self.str_list_blocks)
        self.combo1.activated.connect(self.combo1_new_item_selected)
        self.combo2 = QComboBox()
        self.combo2.addItems(self.str_list_blocks)
        self.combo2.activated.connect(self.combo2_new_item_selected)
        self.combo3 = QComboBox()
        self.combo3.addItems(self.str_list_blocks)
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
        self.station_input = QLineEdit()
        self.station_input.setPlaceholderText('Station Name')
        train_model_layout.addWidget(self.station_input, 2, 0)
        self.num_input = QLineEdit()
        self.num_input.setPlaceholderText('Disembarking Passengers')
        train_model_layout.addWidget(self.num_input, 2, 1)
        self.apply_button2 = QPushButton("Apply")
        self.apply_button2.clicked.connect(self.apply_button2_clicked)
        train_model_layout.addWidget(self.apply_button2, 3, 2)


    def combo1_new_item_selected(self):
        pass

    def combo2_new_item_selected(self):
        pass

    def combo3_new_item_selected(self):
        pass

    def combo4_new_item_selected(self):
        pass

    def toggle1_clicked(self):
        pass

    def toggle2_clicked(self):
        pass

    def toggle3_clicked(self):
        pass

    def toggle4_clicked(self):
        pass

    def apply_button_clicked(self):
        pass

    def apply_button2_clicked(self):
        pass


app = QApplication([])
window = TestBenchWindow()
window.show()
app.exec()
