import os

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QGridLayout, QTableWidget, QGroupBox, QVBoxLayout,
    QTableWidget, QLabel, QSlider, QComboBox, QFileDialog, QTableView, QTableWidgetItem, QMainWindow,
    QFrame, QHeaderView, QAbstractScrollArea
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal
from Track_Model.animated_toggle import AnimatedToggle
import sys
from Track_Model.Track_Model import TrackModel
from Track_Model.dynamic_map import DynamicMap
from Track_Model.Track_Model_TB_UI import TestBenchWindow
from Track_Model.map import Map



##############################
# Main Window
##############################
class Window(QMainWindow):
    def __init__(self, track_model):
        super().__init__()
        # Backend
        # self.file_name = self.getFileName()
        self.file_name = 'Green Line.xlsx'
        self.track_model = track_model
        self.test_bench_window = TestBenchWindow()
        # Window Layout
        self.setWindowIcon(QIcon("icon.jpg"))
        self.setWindowTitle("Track Model")
        self.setContentsMargins(20, 20, 20, 20)
        self.resize(1920 // 2, 1080 // 2)
        layout = QGridLayout()
        # signals
        self.track_model.refresh_map_signal.connect(self.refresh)
        # Style

        # Failure Modes
        self.failure_modes_group = QGroupBox("Failure Modes")

        fm_group_layout = QGridLayout()

        f1_title = QLabel()
        f1_title.setText("Power Failure:")
        f2_title = QLabel()
        f2_title.setText("Track Circuit Failure:")
        f3_title = QLabel()
        f3_title.setText("Broken Rail Failure:")
        fm_group_layout.addWidget(f1_title, 0, 0)
        fm_group_layout.addWidget(f2_title, 1, 0)
        fm_group_layout.addWidget(f3_title, 2, 0)

        self.str_list_blocks = list(self.track_model.get_data()[1:, 2].astype(str))
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

        fm_group_layout.addWidget(self.combo1, 0, 1)
        fm_group_layout.addWidget(self.combo2, 1, 1)
        fm_group_layout.addWidget(self.combo3, 2, 1)

        self.toggle1 = AnimatedToggle()
        self.toggle1.setFixedSize(self.toggle1.sizeHint())
        self.toggle1.clicked.connect(self.toggle1_clicked)

        self.toggle2 = AnimatedToggle()
        self.toggle2.setFixedSize(self.toggle2.sizeHint())
        self.toggle2.clicked.connect(self.toggle2_clicked)

        self.toggle3 = AnimatedToggle()
        self.toggle3.setFixedSize(self.toggle3.sizeHint())
        self.toggle3.clicked.connect(self.toggle3_clicked)

        fm_group_layout.addWidget(self.toggle1, 0, 2)
        fm_group_layout.addWidget(self.toggle2, 1, 2)
        fm_group_layout.addWidget(self.toggle3, 2, 2)

        self.failure_modes_group.setLayout(fm_group_layout)

        # Temperature Controls
        self.temperature_controls_group = QGroupBox("Temperature Controls")
        self.temperature_controls_group.setMaximumSize(300, 200)
        tc_layout = QVBoxLayout()

        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setFixedWidth(250)
        slider.setMinimum(-40)
        slider.setMaximum(120)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(5)
        slider.setValue(74)
        slider.valueChanged.connect(self.display_slider_value)

        tc_layout.addWidget(slider)
        self.slider_label = QLabel(self)
        tc_layout.addWidget(self.slider_label)
        self.slider_label.setText("74 °F")

        self.temperature_controls_group.setLayout(tc_layout)

        # Upload Button
        self.upload_layout_group = QGroupBox("Upload Track Layout")
        ul_layout = QVBoxLayout()

        upload_layout_button = QPushButton("Browse Files")
        upload_layout_button.clicked.connect(self.getFileName)
        ul_layout.addWidget(upload_layout_button)

        self.current_file_label = QLabel('Reading from\n"' + self.file_name.split('/')[-1] + '"')
        ul_layout.addWidget(self.current_file_label)

        # Test Bench Button
        self.test_bench_button = QPushButton("Test Bench")
        self.test_bench_button.clicked.connect(self.test_bench_button_clicked)
        ul_layout.addWidget(self.test_bench_button)

        self.upload_layout_group.setLayout(ul_layout)

        # block view
        self.block_view_layout_group = QGroupBox("View Blocks")
        bv_layout = QVBoxLayout()

        self.block_view_layout_group.setLayout(bv_layout)
        # map
        self.map_layout_group = QGroupBox("Map")
        m_layout = QVBoxLayout()
        self.map = Map()
        self.pix_dict = self.map.get_pix_dict()
        m_layout.addWidget(self.map)
        self.map_layout_group.setLayout(m_layout)

        # add layouts to parent layout
        layout.addWidget(self.block_view_layout_group, 0, 0, 2, 1)
        layout.addWidget(self.map_layout_group, 0, 1, 2, 2)
        layout.addWidget(self.upload_layout_group, 2, 2, 1, 1)
        layout.addWidget(self.temperature_controls_group, 2, 1, 1, 1)
        layout.addWidget(self.failure_modes_group, 2, 0, 1, 1)

        # center widget
        center_widget = QWidget()
        center_widget.setLayout(layout)
        self.setCentralWidget(center_widget)

    ##############################
    # Event Handlers
    ##############################
    def display_slider_value(self):
        self.slider_label.setText(str(self.sender().value()) + "°F")
        # self.slider_label.adjustSize()  # Expands label size as numbers get larger
        self.track_model.set_env_temperature(self.sender().value())
        if self.sender().value() <= 32:  # could check current heater value, but no need
            self.track_model.set_heaters(1)  # we do not use bool b/c we need NaN value for non-heater blocks
        else:
            self.track_model.set_heaters(0)
        self.refresh()  # we could write a new function for only refreshing tables 1&3, but no need

    def getFileName(self):
        # file browser dialog
        file_filter = 'Data File (*.xlsx);; Excel File (*.xlsx, *.xls)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select Track Layout File',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Data File (*.xlsx)'
        )
        # Set file_name and change label
        self.file_name = response[0]
        if hasattr(self, 'current_file_label'):
            self.current_file_label.setText('Reading from\n"' + self.file_name.split('/')[-1] + '"')

        # Update track_model
        self.track_model = TrackModel(self.file_name)

        # TODO: Make a refresh everything (or reset everything) function and put it here
        # return our new file name
        return self.file_name

    def combo1_new_item_selected(self):
        # sets the value of the toggle based on the value from our data
        block = int(self.combo1.currentText())
        print(self.track_model.get_data()[block, 13])
        self.toggle1.setChecked(self.track_model.get_data()[block, 13])

    def toggle1_clicked(self):
        block = int(self.combo1.currentText())
        val = int(self.toggle1.isChecked())
        self.track_model.set_power_failure(block, val)
        self.refresh()

    def combo2_new_item_selected(self):
        # sets the value of the toggle based on the value from our data
        block = int(self.combo2.currentText())
        self.toggle2.setChecked(self.track_model.get_data()[block, 14])

    def toggle2_clicked(self):
        block = int(self.combo2.currentText())
        val = int(self.toggle2.isChecked())
        self.track_model.set_track_circuit_failure(block, val)
        self.refresh()

    def combo3_new_item_selected(self):
        # sets the value of the toggle based on the value from our data
        block = int(self.combo3.currentText())
        self.toggle3.setChecked(self.track_model.get_data()[block, 15])

    def toggle3_clicked(self):
        block = int(self.combo3.currentText())
        val = int(self.toggle3.isChecked())
        self.track_model.set_broken_rail_failure(block, val)
        self.refresh()

    def test_bench_button_clicked(self):
        pass

    def refresh(self):
        occupancy = self.track_model.get_occupancy_list()
        occupancy =
        print('implement refresh pls')


##############################
# Run app
##############################
#
# app = QApplication(sys.argv)
# window = Window()
# window.show()
# sys.exit(app.exec())

