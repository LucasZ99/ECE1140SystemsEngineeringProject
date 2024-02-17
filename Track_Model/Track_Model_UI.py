from PyQt6.QtWidgets import (
    QTableWidget, QApplication, QWidget, QPushButton, QLineEdit, QGridLayout, QTableWidget, QGroupBox, QVBoxLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys


##############################
# Main Window
##############################
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.jpg"))
        self.setWindowTitle("Track Model")
        self.setContentsMargins(20, 20, 20, 20)
        self.resize(800, 600)

        layout = QGridLayout()
        self.setLayout(layout)

        # 3x3 grid
        # [s] [m] [m]
        # [s] [m] [m]
        # [s] [f] [t]
        self.selected_section_group = QGroupBox("Selected Section")

        ss_group_layout = QVBoxLayout()
        ss_group_layout.addWidget()

        layout.addWidget(self.selected_section_group, 0, 0, 3, 1)

        self.failure_modes_group = QGroupBox("Failure Modes")
        layout.addWidget(self.failure_modes_group, 2, 1, 1, 1)
        self.temperature_controls_group = QGroupBox("Temperature Controls")
        layout.addWidget(self.temperature_controls_group, 2, 2, 1, 1)
        self.map_group = QGroupBox("Map")
        layout.addWidget(self.map_group, 0, 1, 2, 2)

        # button1 = QPushButton("Button1")
        # layout.addWidget(button1, 0, 1)
        #
        # table1 = QTableWidget(12, 3, self)
        # layout.addWidget(table1, 0, 0)
        #
        # table2 = QTableWidget(12, 3, self)
        # layout.addWidget(table2, 1, 0)
        #
        # table3 = QTableWidget(12, 3, self)
        # layout.addWidget(table3, 2, 0)


##############################
# Table Object
##############################



##############################
# Run app
##############################
app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
