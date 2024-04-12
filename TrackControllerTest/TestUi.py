import os

from PyQt6.QtWidgets import QMainWindow, QComboBox, QCheckBox, QPushButton, QLineEdit
from PyQt6.uic import loadUi


class TestUi(QMainWindow):
    def __init__(self, test_business_logic):
        super().__init__()
        self.title = 'Track Controller Test Ui'

        self.test_business_logic = test_business_logic
        self.blocks = self.test_business_logic.blocks
        self.blocks_occupancy = self.test_business_logic.occupancy_dict
        self.authority = [0, 1, 2, 3, 4]

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

        # Initialization:
        self.init_authority_select()
        self.update_occupancy_block_select()
        self.init_block_list()

        self.authority_select.currentIndexChanged.connect(self.authority_update)
        self.occupied_checkbox.clicked.connect(self.occupancy_update)
        self.track_signal_block_select.currentIndexChanged.connect(self.track_signal_block_update)
        self.speed_input.editingFinished.connect(self.update_speed)
        self.send_ctc_inputs_button.clicked.connect(self.send_ctc_inputs)
        self.send_track_inputs_button.clicked.connect(self.send_track_inputs)

    def init_authority_select(self):
        self.authority_select.clear()
        for authority in self.authority:
            self.authority_select.addItem(str(authority))
            self.authority_select.adjustSize()

    def update_occupancy_block_select(self):

        self.occupancy_block_select.clear()

        for block, occupancy in self.blocks_occupancy.items():
            self.occupancy_block_select.addItem(str(block) + " " + str(occupancy))
            self.occupancy_block_select.adjustSize()

        self.show()

    def init_block_list(self):
        self.track_signal_block_select.clear()
        for block in self.blocks:
            self.track_signal_block_select.addItem(str(block))
            self.occupancy_block_select.adjustSize()

    def authority_update(self):
        self.test_business_logic.track_signal_authority_update(authority=self.authority_select.currentIndex())

    def occupancy_update(self):
        if self.occupied_checkbox.isChecked():
            self.blocks_occupancy[self.occupancy_block_select.currentIndex()+1] = True
        else:
            self.blocks_occupancy[self.occupancy_block_select.currentIndex()+1] = False

        self.test_business_logic.occupancy_update(blocks_occupancy=self.blocks_occupancy)
        self.update_occupancy_block_select()

    def track_signal_block_update(self):
        block_list_index = self.track_signal_block_select.currentIndex()
        block = self.blocks[block_list_index]
        self.test_business_logic.track_signal_block_update(block)

    def update_speed(self):
        text = self.speed_input.text()  # checking to see if it is a valid integer
        if text.isnumeric() or text.replace(".", "").isnumeric():  # text must be an int or float
            value = float(text)
            if value >= 0:
                self.test_business_logic.track_signal_speed_update(value)

    def send_ctc_inputs(self):
        self.test_business_logic.send_ctc_inputs()

    def send_track_inputs(self):
        self.test_business_logic.send_track_inputs()
