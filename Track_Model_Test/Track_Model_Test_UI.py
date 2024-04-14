import sys
import threading
# from Track_Controller_SW import TrackController

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt6.uic import loadUi


class TrackModelTestLauncherUI(QMainWindow):
    open_track_model_ui_signal = pyqtSignal()
    open_track_controller_ui_signal = pyqtSignal()
    open_train_model_ui_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Instantiate buttons as objects
        self.track_model_button = QPushButton('Track Model')
        self.test_button = QPushButton('Test Inputs')

        # Connect button clicks to functionality
        self.track_model_button.clicked.connect(self.start_track_model_ui)
        self.test_button.clicked.connect(self.start_test_ui)

        self.show()

    def start_test_ui(self):
        self.open_test_ui_signal.emit()
        print("Track Controller A button clicked")

    def start_track_model_ui(self):
        self.open_track_model_ui_signal.emit()
        print("Track Model ui button clicked")


def show_launcher_ui():
    app = QApplication(sys.argv)
    ui = TrackModelTestLauncherUI()
    ui.show()
    app.exec()


def start_launcher_ui():
    launcher_thread = threading.Thread(target=show_launcher_ui)
    launcher_thread.start()


if __name__ == '__main__':
    start_launcher_ui()
