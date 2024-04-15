import sys
import threading
# from Track_Controller_SW import TrackController

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit
from PyQt6.uic import loadUi


class TrackModelTestUI(QMainWindow):
    update_track_model_from_wayside = pyqtSignal(list, list, list, list, list)
    update_track_model_from_train_model = pyqtSignal(object, object)

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

        self.authority_safe_speed_update = []
        self.switch_changed_indexes = []
        self.signal_changed_indexes = []
        self.rr_crossing_indexes = []
        self.toggle_block_indexes = []
        self.delta_x_dict = {}
        self.disembarking_passengers_dict = {}

        # Instantiate labels and forms
        authority_safe_speed_update_label = QLabel('authority_safe_speed_update:')
        authority_safe_speed_update_input = QLineEdit()
        authority_safe_speed_update_input.editingFinished.connect(self.authority_safe_speed_update_input_handler)
        switch_changed_indexes_label = QLabel('switch_changed_indexes:')
        switch_changed_indexes_input = QLineEdit()
        switch_changed_indexes_input.editingFinished.connect(self.switch_changed_indexes_input_handler)
        signal_changed_indexes_label = QLabel('signal_changed_indexes:')
        signal_changed_indexes_input = QLineEdit()
        signal_changed_indexes_input.editingFinished.connect(self.signal_changed_indexes_input_handler)
        rr_crossing_indexes_label = QLabel('rr_crossing_indexes:')
        rr_crossing_indexes_input = QLineEdit()
        rr_crossing_indexes_input.editingFinished.connect(self.rr_crossing_indexes_input_handler)
        toggle_block_indexes_label = QLabel('toggle_block_indexes:')
        toggle_block_indexes_input = QLineEdit()
        toggle_block_indexes_input.editingFinished.connect(self.toggle_block_indexes_input_handler)

        self.wayside_button = QPushButton('Send Wayside Inputs')

        delta_x_dict_label = QLabel('delta_x_dict:')
        delta_x_dict_input = QLineEdit()
        disembarking_passengers_dict_label = QLabel('disembarking_passengers_dict')
        disembarking_passengers_dict_input = QLineEdit()

        self.train_model_button = QPushButton('Send Train Model Inputs')

        # Connect button clicks to functionality
        self.wayside_button.clicked.connect(self.wayside_button_clicked)
        self.train_model_button.clicked.connect(self.train_model_button_clicked)

        self.show()

    def start_test_ui(self):
        self.open_test_ui_signal.emit()
        print("Test ui button clicked")

    def start_track_model_ui(self):
        self.open_track_model_ui_signal.emit()
        print("Track Model ui button clicked")

    def authority_safe_speed_update_input_handler(self):
        pass

    def switch_changed_indexes_input_handler(self):
        pass

    def signal_changed_indexes_input_handler(self):
        pass

    def rr_crossing_indexes_input_handler(self):
        pass

    def toggle_block_indexes_input_handler(self):
        pass

    def wayside_button_clicked(self):
        pass

    def train_model_button_clicked(self):
        pass


def str_to_dict(input_str):
    # Enter a dictionary as a string (e.g., {'key': 'value', 'key2': 'value2'}):

    # Convert string to dictionary using eval()
    try:
        my_dict = eval(input_str)
        print("Converted dictionary:", my_dict)
        return my_dict
    except Exception as e:
        print("Error:", e)


def str_to_list_of_tuples(input_str):
    # Get input string
    # Enter a list of tuples as a string (e.g., [('key', 'value'), ('key2', 'value2')]):
    # or just a list

    # Convert string to list of tuples using eval()
    try:
        my_list = eval(input_str)
        print("Converted list of tuples:", my_list)
        return my_list
    except Exception as e:
        print("Error:", e)


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
