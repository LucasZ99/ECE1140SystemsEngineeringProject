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
from TableModel import TableModel
from dynamic_map import DynamicMap


##############################
# Main Window
##############################
class TestBenchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test Bench')

        layout = QVBoxLayout()
        self.setLayout(layout)

        track_controller_group = QGroupBox('Track Controller')
        track_controller_layout = QGridLayout()
        # Column 1
        track_controller_layout.addWidget(QLabel('Commanded Speed:'), 0, 0)
        track_controller_layout.addWidget(QLabel('Authority:'), 1, 0)
        track_controller_layout.addWidget(QLabel('Switch Position:'), 2, 0)
        track_controller_layout.addWidget(QLabel('Signal Activation:'), 3, 0)
        track_controller_layout.addWidget(QLabel('Rail Road Crossing:'), 4, 0)
        track_controller_group.setLayout(track_controller_layout)
        layout.addWidget(track_controller_group)
        # Column 2
        self.commanded_speed_input = QLineEdit()
        self.commanded_speed_input.setPlaceholderText('Input m/s')
        track_controller_layout.addWidget(self.commanded_speed_input, 0, 1)
        self.authority_input = QLineEdit()
        self.authority_input.setPlaceholderText('Input m')
        track_controller_layout.addWidget(self.authority_input, 1, 1)

        train_model_group = QGroupBox('Train Model')
        train_model_layout = QGridLayout()
        layout.addWidget(train_model_group)


app = QApplication([])
window = TestBenchWindow()
window.show()
app.exec()
