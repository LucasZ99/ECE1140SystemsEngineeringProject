import sys
import threading
# from Track_Controller_SW import TrackController

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt6.uic import loadUi


class LauncherUi(QMainWindow):
    open_time_module_ui_signal = pyqtSignal()
    open_track_controller_ui_signal = pyqtSignal(str)
    open_track_controller_tb_ui_signal = pyqtSignal(str)
    open_track_model_ui_signal = pyqtSignal()
    open_train_controller_SW_ui_signal = pyqtSignal()
    open_train_controller_HW_ui_signal = pyqtSignal()
    open_train_model_ui_signal = pyqtSignal()
    open_ctc_ui_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        loadUi('launcher.ui', self)

        # instantiate buttons as objects
        self.CTC_button = self.findChild(QPushButton, 'CTC_button')
        self.time_module_button = self.findChild(QPushButton, 'time_module_button')
        self.track_controller_A_button = self.findChild(QPushButton, 'track_controller_A_button')
        self.track_controller_B_button = self.findChild(QPushButton, 'track_controller_b_button')
        self.track_controller_C_button = self.findChild(QPushButton, 'track_controller_c_button')
        self.track_model_button = self.findChild(QPushButton, 'track_model_button')
        self.train_controller_button_SW = self.findChild(QPushButton, 'train_controller_button_SW')
        self.train_controller_button_HW = self.findChild(QPushButton, 'train_controller_button_HW')
        self.train_model_button = self.findChild(QPushButton, 'train_model_button')
        self.track_controller_A_testbench_button = self.findChild(QPushButton, 'track_controller_A_testbench_button')
        self.track_controller_B_testbench_button = self.findChild(QPushButton, 'track_controller_B_testbench_button')
        self.track_controller_C_testbench_button = self.findChild(QPushButton, 'track_controller_C_testbench_button')

        # Connect button clicks to functionality
        # Time Module
        self.time_module_button.clicked.connect(self.start_time_module_ui)

        # CTC
        self.CTC_button.clicked.connect(self.start_ctc_ui)

        # Track Controller
        self.track_controller_A_button.clicked.connect(self.start_track_controller_sw_a_ui)
        self.track_controller_A_testbench_button.clicked.connect(self.start_track_controller_a_tb_ui)
        self.track_controller_B_testbench_button.clicked.connect(self.start_track_controller_b_tb_ui)
        self.track_controller_C_button.clicked.connect(self.start_track_controller_sw_c_ui)
        self.track_controller_C_testbench_button.clicked.connect(self.start_track_controller_c_tb_ui)
        self.train_model_button.clicked.connect(self.start_train_model_ui)

        # Track Model
        self.track_model_button.clicked.connect(self.start_track_model_ui)

        # Train Controller
        self.train_controller_button_SW.clicked.connect(self.start_train_controller_SW_ui)
        self.train_controller_button_HW.clicked.connect(self.start_train_controller_HW_ui)

        self.show()

    def start_time_module_ui(self):
        self.open_time_module_ui_signal.emit()
        print("Time module button clicked")

    def start_ctc_ui(self):
        self.open_ctc_ui_signal.emit()
        print("CTC button clicked")

    def start_track_controller_sw_a_ui(self):
        self.open_track_controller_ui_signal.emit("A")
        print("Track Controller A button clicked")

    def start_track_controller_a_tb_ui(self):
        self.open_track_controller_tb_ui_signal.emit("A")
        print("Track Controller TB A button clicked")

    def start_track_controller_b_tb_ui(self):
        self.open_track_controller_tb_ui_signal.emit("B")
        print("Track Controller TB B button clicked")

    def start_track_controller_sw_c_ui(self):
        self.open_track_controller_ui_signal.emit("C")
        print("Track Controller C button clicked")

    def start_track_controller_c_tb_ui(self):
        self.open_track_controller_tb_ui_signal.emit("C")
        print("Track Controller TB C button clicked")

    def start_track_model_ui(self):
        self.open_track_model_ui_signal.emit()
        print("Track Model ui button clicked")

    def start_train_controller_SW_ui(self):
        self.open_train_controller_SW_ui_signal.emit()
        print("Train Controller SW ui button clicked")

    def start_train_controller_HW_ui(self):
        self.open_train_controller_HW_ui_signal.emit()
        print("Train Controller HW ui button clicked")

    def start_train_model_ui(self):
        self.open_train_model_ui_signal.emit()
        print("Train Model ui button clicked")


def show_launcher_ui():
    app = QApplication(sys.argv)
    ui = LauncherUi()
    ui.show()
    app.exec()


def start_launcher_ui():
    launcher_thread = threading.Thread(target=show_launcher_ui)
    launcher_thread.start()


if __name__ == '__main__':
    start_launcher_ui()
