import sys
import threading
# from Track_Controller_SW import TrackController

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
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
        self.authority_safe_speed_update_label = QLabel('authority_safe_speed_update:')
        self.authority_safe_speed_update_input = QLineEdit()
        self.authority_safe_speed_update_input.setText('[(62, 4, 50)]')
        self.authority_safe_speed_update_input.editingFinished.connect(self.authority_safe_speed_update_input_handler)
        self.switch_changed_indexes_label = QLabel('switch_changed_indexes:')
        self.switch_changed_indexes_input = QLineEdit()
        self.switch_changed_indexes_input.setText('[(13, False), (28, False), (57, False), (63, False), (77, False), (85, False) ]')
        self.switch_changed_indexes_input.editingFinished.connect(self.switch_changed_indexes_input_handler)
        self.signal_changed_indexes_label = QLabel('signal_changed_indexes:')
        self.signal_changed_indexes_input = QLineEdit()
        self.signal_changed_indexes_input.setText('[(1, False), (12, False), (29, False), (76, False), (87, False), (100, False), (101, False), (150, False)]')
        self.signal_changed_indexes_input.editingFinished.connect(self.signal_changed_indexes_input_handler)
        self.rr_crossing_indexes_label = QLabel('rr_crossing_indexes:')
        self.rr_crossing_indexes_input = QLineEdit()
        self.rr_crossing_indexes_input.setText('[(19, False), (108, False)]')
        self.rr_crossing_indexes_input.editingFinished.connect(self.rr_crossing_indexes_input_handler)
        self.toggle_block_indexes_label = QLabel('toggle_block_indexes:')
        self.toggle_block_indexes_input = QLineEdit()
        self.toggle_block_indexes_input.setText('[]')
        self.toggle_block_indexes_input.editingFinished.connect(self.toggle_block_indexes_input_handler)

        self.wayside_button = QPushButton('Send Wayside Inputs')

        self.delta_x_dict_label = QLabel('delta_x_dict:')
        self.delta_x_dict_input = QLineEdit()
        self.delta_x_dict_input.setText('{1:25}')
        self.delta_x_dict_input.editingFinished.connect(self.delta_x_dict_input_handler)
        self.disembarking_passengers_dict_label = QLabel('disembarking_passengers_dict')
        self.disembarking_passengers_dict_input = QLineEdit()
        self.disembarking_passengers_dict_input.setText('{}')
        self.disembarking_passengers_dict_input.editingFinished.connect(self.disembarking_passengers_dict_input_handler)

        self.train_model_button = QPushButton('Send Train Model Inputs')

        # Connect button clicks to functionality
        self.wayside_button.clicked.connect(self.wayside_button_clicked)
        self.train_model_button.clicked.connect(self.train_model_button_clicked)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.authority_safe_speed_update_label)
        layout.addWidget(self.authority_safe_speed_update_input)
        layout.addWidget(self.switch_changed_indexes_label)
        layout.addWidget(self.switch_changed_indexes_input)
        layout.addWidget(self.signal_changed_indexes_label)
        layout.addWidget(self.signal_changed_indexes_input)
        layout.addWidget(self.rr_crossing_indexes_label)
        layout.addWidget(self.rr_crossing_indexes_input)
        layout.addWidget(self.toggle_block_indexes_label)
        layout.addWidget(self.toggle_block_indexes_input)
        layout.addWidget(self.wayside_button)

        layout.addWidget(self.delta_x_dict_label)
        layout.addWidget(self.delta_x_dict_input)
        layout.addWidget(self.disembarking_passengers_dict_label)
        layout.addWidget(self.disembarking_passengers_dict_input)
        layout.addWidget(self.train_model_button)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def authority_safe_speed_update_input_handler(self):
        self.authority_safe_speed_update = str_to_list(self.authority_safe_speed_update_input.text())

    def switch_changed_indexes_input_handler(self):
        self.switch_changed_indexes = str_to_list(self.switch_changed_indexes_input.text())

    def signal_changed_indexes_input_handler(self):
        self.signal_changed_indexes = str_to_list(self.signal_changed_indexes_input.text())

    def rr_crossing_indexes_input_handler(self):
        self.rr_crossing_indexes = str_to_list(self.rr_crossing_indexes_input.text())

    def toggle_block_indexes_input_handler(self):
        self.toggle_block_indexes = str_to_list(self.toggle_block_indexes_input.text())

    def wayside_button_clicked(self):
        print(f'Sending wayside inputs:\n'
              f'authority_safe_speed_update = {self.authority_safe_speed_update}, '
              f'switch_changed_indexes = {self.switch_changed_indexes}, '
              f'signal_changed_indexes = {self.signal_changed_indexes}, '
              f'rr_crossing_indexes = {self.rr_crossing_indexes}, '
              f'toggle_block_indexes = {self.toggle_block_indexes}')

        self.update_track_model_from_wayside.emit(
            self.authority_safe_speed_update, self.switch_changed_indexes, self.signal_changed_indexes,
            self.rr_crossing_indexes, self.toggle_block_indexes)

    def delta_x_dict_input_handler(self):
        self.delta_x_dict = str_to_dict(self.delta_x_dict_input.text())

    def disembarking_passengers_dict_input_handler(self):
        self.disembarking_passengers_dict = str_to_dict(self.disembarking_passengers_dict_input.text())

    def train_model_button_clicked(self):
        print(f'Sending train model inputs\n'
              f'delta_x_dict = {self.delta_x_dict}, disembarking_passengers_dict = {self.disembarking_passengers_dict}')
        self.update_track_model_from_train_model.emit(self.delta_x_dict, self.disembarking_passengers_dict)


def str_to_dict(input_str):
    # Enter a dictionary as a string (e.g., {'key': 'value', 'key2': 'value2'}):

    # Convert string to dictionary using eval()
    try:
        my_dict = eval(input_str)
        print("Converted dictionary:", my_dict)
        return my_dict
    except Exception as e:
        print("Error:", e)


def str_to_list(input_str):
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


# def show_launcher_ui():
#     app = QApplication(sys.argv)
#     ui = TrackModelTestUI()
#     ui.show()
#     app.exec()
#
#
# def start_launcher_ui():
#     launcher_thread = threading.Thread(target=show_launcher_ui)
#     launcher_thread.start()
#
#
# if __name__ == '__main__':
#     start_launcher_ui()
