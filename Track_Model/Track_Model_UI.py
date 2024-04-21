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
from Track_Model.oldTB_UI import TestBenchWindow
from Track_Model.map import Map
import time


##############################
# Main Window
##############################
class Window(QMainWindow):  # TODO: FAILURE MODE FROM NEW COMBOBOX
    def __init__(self, track_model):
        super().__init__()
        # Backend
        # self.file_name = self.getFileName()
        self.file_name = 'Green Line.xlsx'
        self.track_model = track_model
        self.full_path = track_model.get_full_path()
        # self.test_bench_window = TestBenchWindow()
        self.counter = 0
        # Window Layout
        self.setWindowIcon(QIcon("icon.jpg"))
        self.setWindowTitle("Track Model")
        self.setContentsMargins(20, 20, 20, 20)
        self.resize(1920 // 2, 1080 // 2)
        layout = QGridLayout()
        # signals
        self.track_model.refresh_ui_signal.connect(self.refresh)

        # str_list_blocks
        self.str_list_blocks = list(self.track_model.get_data()[1:, 2].astype(str))
        for i in range(1, len(self.str_list_blocks) + 1):
            self.str_list_blocks[i-1] = self.track_model.get_data()[i, 1] + self.str_list_blocks[i-1]

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

        self.upload_layout_group.setLayout(ul_layout)

        # block view
        self.block_view_layout_group = QGroupBox("Block Info")
        bv_layout = QGridLayout()
        # block selection combo
        self.block_info_combo = QComboBox()
        self.block_info_combo.addItems(self.str_list_blocks)
        self.block_info_combo.activated.connect(self.refresh_block_info)
        self.block_info_combo.setFixedSize(60, 25)
        bv_layout.addWidget(self.block_info_combo)
        # block info labels
        info = track_model.get_block_info(1)
        self.length_label = QLabel('length = ' + str(info[0]))
        self.grade_label = QLabel('grade = ' + str(info[1]))
        self.speed_lim_label = QLabel('speed lim = ' + str(info[2]))
        self.elevation_label = QLabel('elevation = ' + str(info[3]))
        self.occupied_label = QLabel('occupied = ' + str(info[4]))
        self.beacon_label = QLabel('beacon = ' + str(info[5]))
        self.track_heated_label = QLabel('track heated = ' + str(info[6]))
        self.underground_label = QLabel('underground = ' + str(info[7]))
        self.power_fail_label = QLabel('power failure = ' + str(info[8]))
        self.track_circ_fail_label = QLabel('track circuit failure = ' + str(info[9]))
        self.broken_rail_label = QLabel('broken rail failure = ' + str(info[10]))
        self.switch_label = QLabel('switch = ' + str(info[11]))
        self.signal_label = QLabel('signal = ' + str(info[12]))
        self.rxr_label = QLabel('rxr = ' + str(info[13]))
        bv_layout.addWidget(self.length_label, 1, 0)
        bv_layout.addWidget(self.grade_label, 2, 0)
        bv_layout.addWidget(self.speed_lim_label, 3, 0)
        bv_layout.addWidget(self.elevation_label, 4, 0)
        bv_layout.addWidget(self.occupied_label, 5, 0)
        bv_layout.addWidget(self.beacon_label, 6, 0)
        bv_layout.addWidget(self.track_heated_label, 7, 0)
        bv_layout.addWidget(self.underground_label, 8, 0)
        # failures
        bv_layout.addWidget(self.power_fail_label, 1, 1)
        bv_layout.addWidget(self.track_circ_fail_label, 2, 1)
        bv_layout.addWidget(self.broken_rail_label, 3, 1)
        # infrastructure
        bv_layout.addWidget(self.switch_label, 4, 1)
        bv_layout.addWidget(self.signal_label, 5, 1)
        bv_layout.addWidget(self.rxr_label, 6, 1)
        # train dictionary display
        self.train_dict_label = QLabel('Trains: ' + str(self.track_model.get_train_dict()))
        bv_layout.addWidget(self.train_dict_label, 9, 0)
        # failure combo/toggle
        self.failure_combo = QComboBox()
        self.failure_combo.addItems(['Power Failure', 'Track Circuit Failure', 'Broken Rail Failure'])
        self.failure_combo.activated.connect(self.failure_combo_updated)

        self.failure_toggle = AnimatedToggle()
        self.failure_toggle.setFixedSize(self.failure_toggle.sizeHint())
        self.failure_toggle.clicked.connect(self.failure_toggle_clicked)
        self.block_view_layout_group.setLayout(bv_layout)
        bv_layout.addWidget(self.failure_combo, 10, 0)
        bv_layout.addWidget(self.failure_toggle, 10, 1)
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
        # layout.addWidget(self.failure_modes_group, 2, 0, 1, 1)

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

    def failure_combo_updated(self):
        block = int(self.block_info_combo.currentText()[1:])
        failure_mode = str(self.failure_combo.currentText())
        failure_mode_int = 0
        if failure_mode == 'Power Failure':
            failure_mode_int = 13
        elif failure_mode == 'Track Circuit Failure':
            failure_mode_int = 14
        else:  # broken rail failure
            failure_mode_int = 15
        self.failure_toggle.setChecked(self.track_model.get_data()[block, failure_mode_int])

    def failure_toggle_clicked(self):
        block = int(self.block_info_combo.currentText()[1:])
        val = bool(self.failure_toggle.isChecked())
        failure_mode = str(self.failure_combo.currentText())
        if failure_mode == 'Power Failure':
            self.track_model.set_power_failure(block, val)
        elif failure_mode == 'Track Circuit Failure':
            self.track_model.set_track_circuit_failure(block, val)
        else:  # broken rail failure
            self.track_model.set_broken_rail_failure(block, val)
        self.refresh()

    def refresh_block_info(self):
        block = int(self.block_info_combo.currentText()[1:])
        info = self.track_model.get_block_info(block)
        self.length_label.setText('length = ' + str(info[0]))
        self.grade_label.setText('grade = ' + str(info[1]))
        self.speed_lim_label.setText('speed lim = ' + str(info[2]))
        self.elevation_label.setText('elevation = ' + str(info[3]))
        self.occupied_label.setText('occupied = ' + str(info[4]))
        self.beacon_label.setText('beacon = ' + str(info[5]))
        self.track_heated_label.setText('track heated = ' + str(info[6]))
        self.underground_label.setText('underground = ' + str(info[7]))

        self.power_fail_label.setText('power failure = ' + str(info[8]))
        self.track_circ_fail_label.setText('track circuit failure = ' + str(info[9]))
        self.broken_rail_label.setText('broken rail failure = ' + str(info[10]))

        self.switch_label.setText('switch = ' + str(info[11]))
        self.signal_label.setText('signal = ' + str(info[12]))
        self.rxr_label.setText('rxr = ' + str(info[13]))

        self.train_dict_label.setText('Trains: ' + str(self.track_model.get_train_dict()))

    def add_train(self):
        self.map.add_train()

    def move_train(self, train_id, block):
        self.map.move_train(train_id, block)

    def map_update_signal(self, index, val):
        self.map.set_signal(index, val)

    def map_update_rxr(self, index, val):
        self.map.set_rxr(index, val)

    def refresh(self):
        self.refresh_block_info()
        print('refresh ui called')


##############################
# Run app
##############################
#
# app = QApplication(sys.argv)
# window = Window()
# window.show()
# sys.exit(app.exec())

