import sys
import threading
# from Track_Controller_SW import TrackController

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt6.uic import loadUi


class TrackModelTestUI(QMainWindow):
    update_track_model_from_wayside = pyqtSignal(list, list, list, list, list)
    update_track_model_from_train_model = pyqtSignal(object, object)
    # TODO: Everything below this is just copied and pasted
    # UI should include:
    #
    # wayside (just do str inputs for all of these?):
    # authority_safe_speed_update: list[tuple[block_id: int, authority: int, safe_speed: float]]
    # switch_changed_indexes: list[switch_index: int]
    # signal_changed_indexes: list[signal_index: int]
    # rr_crossing_indexes: list[crossing_index: int]
    # toggle_block_indexes: list[block_index: int]
    #
    # train model (just do str inputs for all of these?):
    # delta_x_dict:
    # 			dict[train_id:int, delta_x:float]
    # disembarking_passengers_dict:
    # 			dict[train_id: int, disembarking_passengers: int]
    #
    # 2 separate buttons for each signal

    #
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
        print("Test ui button clicked")

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
