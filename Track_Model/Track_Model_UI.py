from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QGridLayout, QTableWidget, QGroupBox, QVBoxLayout,
    QTableWidget, QLabel, QSlider, QComboBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from Animated_Toggle import AnimatedToggle
import sys


##############################
# Main Window
##############################
class Window(QWidget):
    def __init__(self):
        super().__init__()
        # Backend
        # self.trackModel = track_model

        # Window Layout
        self.setWindowIcon(QIcon("icon.jpg"))
        self.setWindowTitle("Track Model")
        self.setContentsMargins(20, 20, 20, 20)
        self.resize(1920//2, 1080//2)
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

        fm_group_layout = QGridLayout()

        f1_title = QLabel()
        f1_title.setText("Broken Rail Failure:")
        f2_title = QLabel()
        f2_title.setText("Track Circuit Failure:")
        f3_title = QLabel()
        f3_title.setText("Power Failure:")
        fm_group_layout.addWidget(f1_title, 0, 0)
        fm_group_layout.addWidget(f2_title, 1, 0)
        fm_group_layout.addWidget(f3_title, 2, 0)

        int_list_blocks = list(range(1, 16))
        str_list_blocks = list(map(str, int_list_blocks))
        combo1 = QComboBox()
        combo1.addItems(str_list_blocks)
        combo2 = QComboBox()
        combo2.addItems(str_list_blocks)
        combo3 = QComboBox()
        combo3.addItems(str_list_blocks)
        fm_group_layout.addWidget(combo1, 0, 1)
        fm_group_layout.addWidget(combo2, 1, 1)
        fm_group_layout.addWidget(combo3, 2, 1)

        toggle1 = AnimatedToggle()
        toggle1.setFixedSize(toggle1.sizeHint())
        toggle2 = AnimatedToggle()
        toggle2.setFixedSize(toggle2.sizeHint())
        toggle3 = AnimatedToggle()
        toggle3.setFixedSize(toggle3.sizeHint())
        fm_group_layout.addWidget(toggle1, 0, 2)
        fm_group_layout.addWidget(toggle2, 1, 2)
        fm_group_layout.addWidget(toggle3, 2, 2)

        self.failure_modes_group.setLayout(fm_group_layout)
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
