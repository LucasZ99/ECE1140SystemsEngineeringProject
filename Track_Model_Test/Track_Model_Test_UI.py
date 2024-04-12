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
        loadUi('launcher.ui', self)

        # Instantiate buttons as objects
        self.track_model_button = QPushButton('Track Model')
        self.test_track_controller_button = QPushButton('Test Track Controller Inputs')
        self.test_train_model_button = QPushButton('Test Train Model Inputs')

        # Connect button clicks to functionality
        self.track_model_button.clicked.connect(self.start_track_model_ui)
        self.test_track_controller_button.clicked.connect(self.start_track_controller_ui)
        self.test_train_model_button.clicked.connect(self.start_train_model_ui)

        self.show()

    def start_track_controller_ui(self):
        self.open_track_controller_ui_signal.emit()
        print("Track Controller A button clicked")

    def start_track_model_ui(self):
        self.open_track_model_ui_signal.emit()
        print("Track Model ui button clicked")

    def start_train_model_ui(self):
        self.open_train_model_ui_signal.emit()
        print("Train Model ui button clicked")


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
