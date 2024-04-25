import os

import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QGridLayout, QTableWidget, QGroupBox, QVBoxLayout,
    QTableWidget, QLabel, QSlider, QComboBox, QFileDialog, QTableView, QTableWidgetItem, QMainWindow,
    QFrame, QHeaderView, QAbstractScrollArea, QHBoxLayout
)
from PyQt6.QtGui import QIcon, QPixmap, QFont, QPalette
from PyQt6.QtCore import Qt, pyqtSignal
from Track_Model.animated_toggle import AnimatedToggle
import sys
from Track_Model.Track_Model import TrackModel
from Track_Model.dynamic_map import DynamicMap
from Track_Model.oldTB_UI import TestBenchWindow
from Track_Model.map import Map
import time
from Track_Model.TrackModelSignals import TrackModelSignals as signals


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Backend
        # self.file_name = self.getFileName()
        self.file_name = 'Green Line.xlsx'
        # self.test_bench_window = TestBenchWindow()
        self.counter = 0
        # Window Layout
        self.setWindowIcon(QIcon("icon.jpg"))
        self.setWindowTitle("Track Model")
        self.setContentsMargins(20, 20, 20, 20)
        self.resize(1920 // 2, 1080 // 2)
        layout = QGridLayout()

        # PICTURES
        dirname = os.path.dirname(__file__)
        white_file = os.path.join(dirname, 'white_circle.png')
        green_file = os.path.join(dirname, 'green_circle.png')
        red_file = os.path.join(dirname, 'red_circle.png')

        self.white_pixmap = QPixmap(white_file)
        self.green_pixmap = QPixmap(green_file)
        self.red_pixmap = QPixmap(red_file)

        # FONTS
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(20)

        # SIGNALS
        self.signals = signals
        # self.signals.refresh_ui_signal.connect(self.refresh)
        self.signals.send_full_path_signal.connect(self.receive_full_path)
        self.signals.send_train_dict_signal.connect(self.receive_train_dict)
        self.signals.send_data_signal.connect(self.receive_data)
        self.signals.send_block_info_signal.connect(self.receive_block_info)

        # initialize track model data
        self.full_path = []
        self.train_dict = {}
        self.data = np.array([])
        self.block_info = np.array([])

        self.signals.get_full_path_signal.emit()
        self.signals.get_train_dict_signal.emit()
        self.signals.get_data_signal.emit()
        self.signals.get_block_info_signal.emit(1)

        # str_list_blocks
        self.str_list_blocks = list(self.data[1:, 2].astype(str))
        for i in range(1, len(self.str_list_blocks) + 1):
            self.str_list_blocks[i-1] = self.data[i, 1] + self.str_list_blocks[i-1]

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
        self.block_view_layout_group = QGroupBox('Details')

        info = self.block_info

        # SELECT BLOCK
        self.select_block_label = QLabel('Select Block:')
        self.select_block_label.setFont(title_font)
        # block selection combo
        self.block_info_combo = QComboBox()
        self.block_info_combo.addItems(self.str_list_blocks)
        self.block_info_combo.activated.connect(self.refresh_block_info)
        self.block_info_combo.setFixedSize(60, 25)
        select_block_layout = QGridLayout()

        self.select_block_label.setContentsMargins(0, 0, 0, 0)
        self.block_info_combo.setContentsMargins(0, 0, 0, 0)

        select_block_layout.addWidget(self.select_block_label, 0, 1, 1, 1)
        select_block_layout.addWidget(self.block_info_combo, 1, 1, 1, 1)

        # BLOCK INFO
        self.block_info_label = QLabel('Block Info')
        self.block_info_label.setFont(title_font)
        # strs
        self.length_label = QLabel('Length: ' + str(round(info[0]*3.28084, 2)) + ' ft')
        self.grade_label = QLabel('Grade: ' + str(info[1]) + ' %')
        self.speed_lim_label = QLabel('Speed Limit: ' + str(round(info[2]*0.621371, 2)) + ' mph')
        self.elevation_label = QLabel('Elevation: ' + str(round(info[3]*3.28084, 2)) + ' ft')
        beacon_str = 'N/A'
        if str(info[5]) != '0' * 128:
            beacon_str = str(info[5])
        self.beacon_label = QLabel('Beacon: ' + beacon_str)
        # bools
        self.occupied_label = QLabel('Occupied')
        pixmap = self.white_pixmap
        if str(info[4]) == 'nan':
            pixmap = self.white_pixmap
        elif info[4]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.occupied_label2 = QLabel(self)
        self.occupied_label2.setPixmap(pixmap)

        self.heated_label = QLabel('Track Heated')
        if str(info[6]) == 'nan':
            pixmap = self.white_pixmap
        elif info[6]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.heated_label2 = QLabel(self)
        self.heated_label2.setPixmap(pixmap)

        self.underground_label = QLabel('Underground')
        if str(info[7]) == 'nan':
            pixmap = self.white_pixmap
        elif info[7]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.underground_label2 = QLabel(self)
        self.underground_label2.setPixmap(pixmap)

        self.infrastructure_label = QLabel('Infrastructure')
        self.infrastructure_label.setFont(title_font)
        self.switch_label = QLabel('Switch')
        self.signal_label = QLabel('Signal')
        self.rxr_label = QLabel('RxR')

        if str(info[11]) == 'nan':
            pixmap = self.white_pixmap
        elif info[11]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.switch_label2 = QLabel(self)
        self.switch_label2.setPixmap(pixmap)

        if str(info[12]) == 'nan':
            pixmap = self.white_pixmap
        elif info[12]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.signal_label2 = QLabel(self)
        self.signal_label2.setPixmap(pixmap)

        if str(info[13]) == 'nan':
            pixmap = self.white_pixmap
        elif info[13]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.rxr_label2 = QLabel(self)
        self.rxr_label2.setPixmap(pixmap)

        # block info layout

        block_info_layout = QGridLayout()

        block_info_layout.addWidget(self.block_info_label, 0, 1, 1, 2)

        block_info_layout.addWidget(self.length_label, 1, 0, 1, 2)
        block_info_layout.addWidget(self.grade_label, 2, 0, 1, 2)
        block_info_layout.addWidget(self.elevation_label, 3, 0, 1, 2)
        block_info_layout.addWidget(self.speed_lim_label, 4, 0, 1, 2)
        block_info_layout.addWidget(self.beacon_label, 5, 0, 1, 2)

        block_info_layout.addWidget(self.occupied_label2, 1, 2, 1, 1)
        block_info_layout.addWidget(self.occupied_label, 1, 3, 1, 1)
        block_info_layout.addWidget(self.heated_label2, 2, 2, 1, 1)
        block_info_layout.addWidget(self.heated_label, 2, 3, 1, 1)
        block_info_layout.addWidget(self.underground_label2, 3, 2, 1, 1)
        block_info_layout.addWidget(self.underground_label, 3, 3, 1, 1)

        block_info_layout.addWidget(self.infrastructure_label, 6, 1, 1, 2)
        block_info_layout.addWidget(self.switch_label2, 7, 1, 1, 1)
        block_info_layout.addWidget(self.switch_label, 7, 2, 1, 1)
        block_info_layout.addWidget(self.signal_label2, 8, 1, 1, 1)
        block_info_layout.addWidget(self.signal_label, 8, 2, 1, 1)
        block_info_layout.addWidget(self.rxr_label2, 9, 1, 1, 1)
        block_info_layout.addWidget(self.rxr_label, 9, 2, 1, 1)

        # FAILURES
        self.failures_label = QLabel('Failures')
        self.failures_label.setFont(title_font)

        self.power_fail_label = QLabel('Power Failure')
        if str(info[8]) == 'nan':
            pixmap = self.white_pixmap
        elif info[8]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.power_fail_label2 = QLabel(self)
        self.power_fail_label2.setPixmap(pixmap)

        self.track_circ_fail_label = QLabel('Track Circuit Failure')
        if str(info[9]) == 'nan':
            pixmap = self.white_pixmap
        elif info[9]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.track_circ_fail_label2 = QLabel(self)
        self.track_circ_fail_label2.setPixmap(pixmap)

        self.broken_rail_fail_label = QLabel('Broken Rail Failure')
        if str(info[10]) == 'nan':
            pixmap = self.white_pixmap
        elif info[10]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.broken_rail_fail_label2 = QLabel(self)
        self.broken_rail_fail_label2.setPixmap(pixmap)

        self.failure_combo = QComboBox()
        self.failure_combo.addItems(['Power', 'Track Circuit', 'Broken Rail'])
        self.failure_combo.activated.connect(self.failure_combo_updated)

        self.failure_toggle = AnimatedToggle()
        self.failure_toggle.setFixedSize(self.failure_toggle.sizeHint())
        self.failure_toggle.clicked.connect(self.failure_toggle_clicked)

        failures_layout = QGridLayout()
        failures_layout.addWidget(self.failures_label, 0, 0, 1, 2)
        failures_layout.addWidget(self.power_fail_label2, 1, 0, 1, 1)
        failures_layout.addWidget(self.power_fail_label, 1, 1, 1, 1)
        failures_layout.addWidget(self.track_circ_fail_label2, 2, 0, 1, 1)
        failures_layout.addWidget(self.track_circ_fail_label, 2, 1, 1, 1)
        failures_layout.addWidget(self.broken_rail_fail_label2, 3, 0, 1, 1)
        failures_layout.addWidget(self.broken_rail_fail_label, 3, 1, 1, 1)
        failures_layout.addWidget(self.failure_combo, 4, 0, 1, 1)
        failures_layout.addWidget(self.failure_toggle, 4, 1, 1, 1)

        # train dictionary display
        self.train_dict_label = QLabel('Trains: ' + str(self.train_dict))

        # Final BV Layout
        bv_layout = QGridLayout()
        self.block_view_layout_group.setLayout(bv_layout)

        combo_layout = QHBoxLayout()
        combo_layout.addWidget(self.select_block_label)
        combo_layout.addWidget(self.block_info_combo)

        bv_layout.addLayout(combo_layout, 0, 0, 1, 1)
        bv_layout.addLayout(failures_layout, 1, 0, 1, 1)
        bv_layout.addLayout(block_info_layout, 0, 1, 2, 1)
        bv_layout.addWidget(self.train_dict_label, 2, 0, 1, 2)

        # map
        self.map_layout_group = QGroupBox("Map")
        m_layout = QVBoxLayout()
        self.map = Map()
        self.pix_dict = self.map.get_pix_dict()
        m_layout.addWidget(self.map)
        self.map_layout_group.setLayout(m_layout)

        # add layouts to parent layout
        layout.addWidget(self.block_view_layout_group, 0, 0, 2, 2)
        layout.addWidget(self.map_layout_group, 0, 2, 3, 2)
        layout.addWidget(self.upload_layout_group, 2, 1, 1, 1)
        layout.addWidget(self.temperature_controls_group, 2, 0, 1, 1)
        # layout.addWidget(self.failure_modes_group, 2, 0, 1, 1)

        # center widget
        center_widget = QWidget()
        center_widget.setLayout(layout)
        self.setCentralWidget(center_widget)

        # MORE SIGNALS
        self.signals.refresh_ui_signal.connect(self.refresh)
        self.signals.map_add_train_signal.connect(self.map.add_train)
        self.signals.map_move_train_signal.connect(self.map.move_train)
        self.signals.map_update_signal_signal.connect(self.map_update_signal)
        self.signals.map_update_rxr_signal.connect(self.map_update_rxr)
        self.signals.map_update_closure_signal.connect(self.map_update_closure)

        # STYLE
        style_file = os.path.join(dirname, 'style.css')
        with open(style_file, 'r') as file:
            self.setStyleSheet(file.read())



    ##############################
    # Event Handlers
    ##############################
    def display_slider_value(self):
        self.slider_label.setText(str(self.sender().value()) + "°F")
        # self.slider_label.adjustSize()  # Expands label size as numbers get larger
        self.signals.set_env_temperature_signal.emit(self.sender().value())
        if self.sender().value() <= 32:  # could check current heater value, but no need
            signals.set_heaters_signal.emit(1)  # we do not use bool b/c we need NaN value for non-heater blocks
        else:
            signals.set_heaters_signal.emit(0)
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

        # TODO: UPDATE TRACK MODEL FROM UI inputted file

        # return our new file name
        return self.file_name

    def failure_combo_updated(self):
        block = int(self.block_info_combo.currentText()[1:])
        failure_mode = str(self.failure_combo.currentText())
        failure_mode_int = 0
        if failure_mode == 'Power':
            failure_mode_int = 13
        elif failure_mode == 'Track Circuit':
            failure_mode_int = 14
        else:  # broken rail failure
            failure_mode_int = 15
        self.signals.get_data_signal.emit()
        self.failure_toggle.setChecked(bool(self.data[block, failure_mode_int]))

    def failure_toggle_clicked(self):
        block = int(self.block_info_combo.currentText()[1:])
        val = bool(self.failure_toggle.isChecked())
        failure_mode = str(self.failure_combo.currentText())
        if failure_mode == 'Power':
            self.signals.set_power_failure_signal.emit(block, val)
            self.map_update_closure(block, val)  # map
        elif failure_mode == 'Track Circuit':
            self.signals.set_track_circuit_failure_signal.emit(block, val)
            self.map_update_closure(block, val)  # map
        else:  # broken rail failure
            self.signals.set_broken_rail_failure_signal.emit(block, val)
            self.map_update_closure(block, val)  # map
        self.refresh()

    # def refresh_block_info(self):
    #     block = int(self.block_info_combo.currentText()[1:])
    #     self.signals.get_block_info_signal.emit(block)
    #     info = self.block_info
    #     self.length_label.setText('length = ' + str(info[0]))
    #     self.grade_label.setText('grade = ' + str(info[1]))
    #     self.speed_lim_label.setText('speed lim = ' + str(info[2]))
    #     self.elevation_label.setText('elevation = ' + str(info[3]))
    #     self.occupied_label.setText('occupied = ' + str(info[4]))
    #     beacon_str = 'N/A'
    #     if str(info[5]) != ('0' * 128):
    #         beacon_str = str(info[5])
    #     self.beacon_label.setText('Beacon: ' + beacon_str)
    #     self.track_heated_label.setText('track heated = ' + str(info[6]))
    #     self.underground_label.setText('underground = ' + str(info[7]))
    #
    #     self.power_fail_label.setText('power failure = ' + str(info[8]))
    #     self.track_circ_fail_label.setText('track circuit failure = ' + str(info[9]))
    #     self.broken_rail_label.setText('broken rail failure = ' + str(info[10]))
    #
    #     self.switch_label.setText('switch = ' + str(info[11]))
    #     self.signal_label.setText('signal = ' + str(info[12]))
    #     self.rxr_label.setText('rxr = ' + str(info[13]))
    #
    #     self.signals.get_train_dict_signal.emit()
    #     self.train_dict_label.setText('Trains: ' + str(self.train_dict))

    def refresh_block_info(self):
        block = int(self.block_info_combo.currentText()[1:])
        self.signals.get_block_info_signal.emit(block)
        info = self.block_info

        # BLOCK INFO
        # strs
        self.length_label.setText('Length: ' + str(round(info[0] * 3.28084, 2)) + ' ft')
        self.grade_label.setText('Grade: ' + str(info[1]) + ' %')
        self.speed_lim_label.setText('Speed Limit: ' + str(round(info[2] * 0.621371, 2)) + ' mph')
        self.elevation_label.setText('Elevation: ' + str(round(info[3] * 3.28084, 2)) + ' ft')
        beacon_str = 'N/A'
        if str(info[5]) != '0' * 128:
            beacon_str = str(info[5])
        self.beacon_label.setText('Beacon: ' + beacon_str)
        # bools
        pixmap = self.white_pixmap
        if str(info[4]) == 'nan':
            pixmap = self.white_pixmap
        elif info[4]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.occupied_label2.setPixmap(pixmap)

        if str(info[6]) == 'nan':
            pixmap = self.white_pixmap
        elif info[6]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.heated_label2.setPixmap(pixmap)

        if str(info[7]) == 'nan':
            pixmap = self.white_pixmap
        elif info[7]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.underground_label2.setPixmap(pixmap)

        if str(info[11]) == 'nan':
            pixmap = self.white_pixmap
        elif info[11]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.switch_label2.setPixmap(pixmap)

        if str(info[12]) == 'nan':
            pixmap = self.white_pixmap
        elif info[12]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.signal_label2.setPixmap(pixmap)

        if str(info[13]) == 'nan':
            pixmap = self.white_pixmap
        elif info[13]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.rxr_label2.setPixmap(pixmap)

        # FAILURES

        if str(info[8]) == 'nan':
            pixmap = self.white_pixmap
        elif info[8]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.power_fail_label2.setPixmap(pixmap)

        if str(info[9]) == 'nan':
            pixmap = self.white_pixmap
        elif info[9]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.track_circ_fail_label2.setPixmap(pixmap)

        if str(info[10]) == 'nan':
            pixmap = self.white_pixmap
        elif info[10]:
            pixmap = self.green_pixmap
        else:
            pixmap = self.red_pixmap
        self.broken_rail_fail_label2.setPixmap(pixmap)

        # keep toggle in right place
        self.failure_combo_updated()

        self.signals.get_train_dict_signal.emit()
        self.train_dict_label.setText('Trains: ' + str(self.train_dict))

        self.map.move_view_finder(block)

    def add_train(self):
        self.map.add_train()

    def move_train(self, train_id, block):
        self.map.move_train(train_id, block)

    def map_update_signal(self, index, val):
        self.map.set_signal(index, val)

    def map_update_rxr(self, index, val):
        self.map.set_rxr(index, val)

    def map_update_closure(self, index, val):
        self.map.update_closure(index, val)

    def refresh(self):
        self.signals.get_data_signal.emit()
        self.signals.get_train_dict_signal.emit()
        self.refresh_block_info()
        print('refresh ui called')
        
    def receive_data(self, data):
        self.data = data
    
    def receive_block_info(self, block_info):
        self.block_info = block_info
    
    def receive_full_path(self, full_path):
        self.full_path = full_path
    
    def receive_train_dict(self, train_dict):
        self.train_dict = train_dict


##############################
# Run app
##############################
#
# app = QApplication(sys.argv)
# window = Window()
# window.show()
# sys.exit(app.exec())

