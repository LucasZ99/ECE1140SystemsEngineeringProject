import sys
import threading
# from Track_Controller_SW import TrackController

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt6.uic import loadUi


class LauncherUi(QMainWindow):
    open_track_controller_ui_signal = pyqtSignal(str)

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
        self.train_controller_button = self.findChild(QPushButton, 'train_controller_button')
        self.train_model_button = self.findChild(QPushButton, 'train_model_button')

        # connect button clicks to functionality
        self.track_controller_A_button.clicked.connect(self.start_track_controller_sw_a_ui)
        self.show()

    def start_track_controller_sw_a_ui(self):
        self.open_track_controller_ui_signal.emit("A")
        print("TC A button clicked")


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
