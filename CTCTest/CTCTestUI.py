import sys

import PyQt6
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject, Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QTableWidget, QTableWidgetItem, \
    QVBoxLayout, QHeaderView

from CTCTest.TrackControllerModel import *

from Common.GreenLine import *
from Common import TrackSignal, Light, RRCrossing, Switch
from Common.Lines import *


class CTCTestUIContainer(QObject):
    def __init__(self, track_controller: TrackControllerModel):
        super().__init__()
        self.ui = CTCTestUI(track_controller)

    def show_ui(self):
        self.ui.show()


class CTCTestUI(QMainWindow):
    open_ctc_ui_signal = pyqtSignal()
    open_time_ui_signal = pyqtSignal()
    update_ctc_from_track_model = pyqtSignal()
    update_ctc_from_wayside = pyqtSignal(dict, list, list, list)

    def __init__(self, track_controller_model: TrackControllerModel):
        super(CTCTestUI, self).__init__()

        self.setWindowTitle('CTC Test UI')
        self.vboxlayout = QVBoxLayout()

        self.track_controller_model = track_controller_model

        # Show CTC Button
        # self.show_ctc_button = QPushButton("Show CTC")
        # self.show_ctc_button.clicked.connect(self.open_ctc_ui_signal)

        # Block List
        self.block_list = QTableWidget()
        self.block_list_header = ["Block ID", "Occupied", "Authority", "Suggested Speed (m/s)", "Maintenance Mode Set"]
        self.block_list.setColumnCount(len(self.block_list_header))
        self.block_list.setHorizontalHeaderLabels(self.block_list_header)

        for row, block in enumerate(get_line_blocks_in_route_order()):
            self.block_list.insertRow(row)
            block_name = QTableWidgetItem(stop_name(0, block))
            occupied = QTableWidgetItem()
            occupied.setFlags(
                PyQt6.QtCore.Qt.ItemFlag.ItemIsUserCheckable | PyQt6.QtCore.Qt.ItemFlag.ItemIsEnabled |
                PyQt6.QtCore.Qt.ItemFlag.ItemIsEnabled)
            occupied.setCheckState(PyQt6.QtCore.Qt.CheckState.Unchecked)

            maintenance_mode_set = QTableWidgetItem()
            maintenance_mode_set.setFlags(
                PyQt6.QtCore.Qt.ItemFlag.ItemIsUserCheckable | PyQt6.QtCore.Qt.ItemFlag.ItemIsEnabled &
                ~ PyQt6.QtCore.Qt.ItemFlag.ItemIsEnabled)

            self.block_list.setItem(row, 0, block_name)
            self.block_list.setItem(row, 1, occupied)
            self.block_list.setItem(row, 4, maintenance_mode_set)

            # connect check box handler
        self.block_list.itemChanged.connect(self.set_block_occupancy_state)

        self.block_list.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.block_list.resizeColumnsToContents()

        self.block_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.vboxlayout.addWidget(self.block_list)
        self.main_layout_widget = QWidget()
        self.main_layout_widget.setLayout(self.vboxlayout)
        self.main_layout_widget.resize(self.block_list.size())

        self.track_controller_model.update_test_ui_speeds_authorities.connect(self.update_authorities_and_speeds)

        self.setCentralWidget(self.main_layout_widget)

        self.show()

    def set_block_occupancy_state(self, occupied_checkbox):
        block_index = occupied_checkbox.row()
        block = list(GREEN_LINE[BLOCKS].keys())[block_index]
        print(block)
        if occupied_checkbox.checkState() == Qt.CheckState.Checked:
            self.track_controller_model.update_block_occupancy(block, OCCUPIED)
        else:
            self.track_controller_model.update_block_occupancy(block, VACANT)

    @pyqtSlot(list)
    def update_authorities_and_speeds(self, track_signals: list[TrackSignal]):
        print("CTCTestUI: Track Signal Received")
        for track_signal in track_signals:
            table_index = list(GREEN_LINE[BLOCKS].keys()).index(track_signal.block_id)
            speed = QTableWidgetItem(str(track_signal.speed))
            authority = QTableWidgetItem(str(track_signal.authority))
            self.block_list.setItem(table_index, 2, authority)
            self.block_list.setItem(table_index, 3, speed)

    def open_uis(self):
        print("Emitting Signals")
        self.open_ctc_ui_signal.emit()
        print("time ui")
        self.open_time_ui_signal.emit()

    # @pyqtSlot(list, bool, list, list)
    # def update_test_ui_from_wayside(self):
    #     pass
