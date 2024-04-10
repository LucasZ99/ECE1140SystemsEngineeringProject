import os

from PyQt6.QtWidgets import QMainWindow, QComboBox, QCheckBox, QPushButton, QLineEdit
from PyQt6.uic import loadUi


class TestUi(QMainWindow):
    def __init__(self, test_business_logic):
        super().__init__()
        self.title = 'Track Controller Test Ui'

        self.test_business_logic = test_business_logic

        # load ui
        current_dir = os.path.dirname(__file__)  # setting up to work in any dir
        ui_path = os.path.join(current_dir, 'TestUi.ui')
        try:
            loadUi(ui_path, self)
        except Exception as e:
            print("Error with loading UI file: ", e)

        self.authority_select = self.findChild(QComboBox, 'authority_select')
        self.occupancy_block_select = self.findChild(QComboBox, 'occupancy_block_select')
        self.occupied_checkbox = self.findChild(QCheckBox, 'occupied_checkbox')
        self.send_ctc_inputs_button = self.findChild(QPushButton, 'send_ctc_inputs_button')
        self.send_track_inputs_button = self.findChild(QPushButton, 'send_track_inputs_button')
        self.speed_input = self.findChild(QLineEdit, 'speed_input')
        self.track_signal_block_select = self.findChild(QComboBox, 'track_signal_block_select')





