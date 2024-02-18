from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QGridLayout, QTableWidget, QGroupBox, QVBoxLayout,
    QTableWidget, QLabel, QSlider
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
        # Backend
        # self.trackModel = track_model
        # Frontend
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

        # Selected Section
        self.selected_section_group = QGroupBox()

        ss_group_layout = QVBoxLayout()

        ss_title = QLabel()
        ss_title.setText("Selected Section (Section X)")
        ss_group_layout.addWidget(ss_title)
        table1 = QTableWidget(12, 3, self)
        ss_group_layout.addWidget(table1)
        table2 = QTableWidget(12, 3, self)
        ss_group_layout.addWidget(table2)
        table3 = QTableWidget(12, 3, self)
        ss_group_layout.addWidget(table3)

        self.selected_section_group.setLayout(ss_group_layout)
        layout.addWidget(self.selected_section_group, 0, 0, 3, 1)

        # Failure Modes
        self.failure_modes_group = QGroupBox("Failure Modes")
        layout.addWidget(self.failure_modes_group, 2, 1, 1, 1)

        # Temperature Controls
        self.temperature_controls_group = QGroupBox("Temperature Controls")
        tc_layout = QVBoxLayout()

        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setGeometry(50, 50, 200, 50)
        slider.setMinimum(-40)
        slider.setMaximum(120)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(5)
        slider.setValue(74)
        slider.valueChanged.connect(self.display_slider_value)
        tc_layout.addWidget(slider)

        self.slider_label = QLabel(self)
        tc_layout.addWidget(self.slider_label)
        self.slider_label.setText("Environmental Temperature: 74 °F")

        self.temperature_controls_group.setLayout(tc_layout)
        layout.addWidget(self.temperature_controls_group, 2, 2, 1, 1)

        # Map
        self.map_group = QGroupBox("Map")
        layout.addWidget(self.map_group, 0, 1, 2, 2)

        ##############################
        # Event Handlers
        ##############################
    def display_slider_value(self):
        self.slider_label.setText("Environmental Temperature: " + str(self.sender().value()) + "°F")
        self.slider_label.adjustSize()  # Expands label size as numbers get larger


##############################
# Run app
##############################
app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
