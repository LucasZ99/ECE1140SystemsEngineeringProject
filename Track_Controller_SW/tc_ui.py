import functools

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QFileDialog, QDialog, QPushButton, QLabel, QLCDNumber, QApplication, QMainWindow, QWidget, \
    QVBoxLayout
from PyQt5 import uic
import sys

import numpy as np
from PyQt5 import QtCore
from switching import switch
from PLC_Logic import parse_plc
import TestBench
import switching


def better_button_ret(size=None, text1=None, text2=None, checkable=True, style1=None, style2=None):
    if text1 and not text2: text2 = text1
    button = QPushButton()
    button.setCheckable(checkable)
    button.setFixedHeight(24)
    # button.clicked.connect( functools.partial(button_click1, but=button) )
    if checkable:
        # button.setStyleSheet(
        #     "background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px")
        if text1:
            button.setText(text1)
        else:
            button.setText("Off")
        button.clicked.connect(
            functools.partial(gen_but_tog, but=button, text1=text1, text2=text2, style_on=style1, style_off=style2))
    else:
        # button.setStyleSheet("background-color: rgb(222, 62, 38); border: 2px solid rgb(222, 0, 0); border-radius: 4px")
        if text1: button.setText(text2)
    if size: button.setFixedWidth(size)
    return button


def gen_but_tog(but, text1=None, text2=None, style_on=None, style_off=None):
    if but.isChecked():
        # but.setStyleSheet(
        #     f"{style_on if style_on else 'background-color: rgb(143, 186, 255); border: 2px solid rgb( 42,  97, 184); border-radius: 6px'}")
        if text1:
            but.setText(text2)
        else:
            but.setText("On")
    else:
        # but.setStyleSheet(
        #     f"{style_off if style_off else 'background-color: rgb(156, 156, 156); border: 2px solid rgb(100, 100, 100); border-radius: 6px'}")
        if text1:
            but.setText(text1)
        else:
            but.setText("Off")


class ManualMode(QWidget):
    def __init__(self, switch_array):
        super().__init__()
        self.setWindowTitle('Manual Mode')
        self.setFixedSize(400, 400)
        self.layout = QVBoxLayout(self)

        # button_array = []
        for switch in switch_array:
            self.layout.addWidget(
                better_button_ret(200,
                                  text1=f"Facing Block {switch.current_pos}",
                                  text2=f"Facing Block {switch.pos_b if switch.current_pos == switch.pos_a else switch.pos_a}")
            )


class OccupancyWorker(QtCore.QObject):
    occupancy_updated = QtCore.pyqtSignal(object)

    def __init__(self, block_occupancy):
        super().__init__()
        self.occupancy_arr = block_occupancy

    def run(self):
        self.occupancy_updated.emit(self.occupancy_arr)


class UI(QMainWindow):
    def __init__(self, switch_array, plc_logic, block_occupancy, authority):
        super(UI, self).__init__()
        # load ui
        uic.loadUi('track_controller.ui', self)

        # Fix the size
        self.setFixedWidth(757)
        self.setFixedHeight(649)

        # Assign attributes
        self.switch_array = switch_array
        self.plc_logic = plc_logic
        self.block_occupancy = block_occupancy
        self.authority = authority

        # Define widgets
        self.manual_mode = self.findChild(QPushButton, 'manual_mode')
        self.browse_button = self.findChild(QPushButton, 'browse')
        self.filename = self.findChild(QLabel, 'filename')
        self.block_occupied = self.findChild(QLCDNumber, 'block_number')
        self.switch_block = self.findChild(QLCDNumber, 'switch_block_number')
        self.light_b6 = self.findChild(QLabel, 'light_block_6')
        self.light_b11 = self.findChild(QLabel, 'light_block_7')
        self.rr_crossing = self.findChild(QLabel, 'label')
        self.tb_button = self.findChild(QPushButton, 'tb_button')

        # define connections
        self.browse_button.clicked.connect(self.browse_files)
        self.manual_mode.clicked.connect(self.manual_mode_dialogue)
        self.tb_button.clicked.connect(self.open_tb)

        # run threads
        self.occupancy_thread()

        # show the app and TB
        self.show()

    def open_tb(self):
        TestBench.main(self.block_occupancy, self.authority)

    def manual_mode_dialogue(self):
        self.w = ManualMode(self.switch_array)
        # TODO: send eventual update to track model
        self.w.show()

    def browse_files(self):
        fname = QFileDialog.getOpenFileName(self, 'Open PLC File', 'C:/Users/lucas')
        self.filename.setText(fname[0])
        self.filename.adjustSize()

        # send filename to parsing program
        self.plc_logic.set_filepath(fname[0])

    def occupancy_thread(self):
        # Create the thread handler
        occupancy_thread = QtCore.QThread()
        occupancy_worker = OccupancyWorker(self.block_occupancy)
        occupancy_worker.moveToThread(occupancy_thread)
        occupancy_thread.started.connect(occupancy_worker.run)
        occupancy_thread.finished.connect(occupancy_thread.quit)

        # Connect to GUI update function
        occupancy_worker.occupancy_updated.connect(self.update_occupancy)

        occupancy_thread.start()
    def update_occupancy(self):
        # Find the truth value from the block occupancy array
        self.block_occupied.display(np.argmax(self.block_occupancy > 0))


def main(switches_arr, plc_logic, block_occupancy, authority):
    app = QApplication(sys.argv)
    UIWindow = UI(switches_arr, plc_logic, block_occupancy, authority)
    UIWindow.show()
    app.exec_()


if __name__ == '__main__':
    auth = 0
    main([], parse_plc(), [], auth)
