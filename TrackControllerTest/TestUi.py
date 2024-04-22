import os

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QComboBox, QPushButton, QLineEdit
from PyQt6.uic import loadUi
from TrackControllerTest.TrackControllerTestSignals import TrackControllerTestSignals as signals


class TestUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Track Controller Test Ui'
        self.signals = signals

        self.blocks = []
        self.blocks_occupancy = {}
        self.authority = [0, 1, 2, 3, 4]
        self.switches = []

        # load ui
        current_dir = os.path.dirname(__file__)  # setting up to work in any dir
        ui_path = os.path.join(current_dir, 'TestUi.ui')
        try:
            loadUi(ui_path, self)
        except Exception as e:
            print("Error with loading UI file: ", e)

        self.authority_select = self.findChild(QComboBox, 'authority_select')
        self.occupancy_block_select = self.findChild(QComboBox, 'occupancy_block_select')
        self.occupancy_toggle_button = self.findChild(QPushButton, 'occupancy_toggle_button')
        self.send_ctc_inputs_button = self.findChild(QPushButton, 'send_ctc_inputs_button')
        self.send_track_inputs_button = self.findChild(QPushButton, 'send_track_inputs_button')
        self.speed_input = self.findChild(QLineEdit, 'speed_input')
        self.track_signal_block_select = self.findChild(QComboBox, 'track_signal_block_select')
        self.toggle_switch_select = self.findChild(QComboBox, 'toggle_switch_select')
        self.toggle_block_select = self.findChild(QComboBox, 'close_block_select')

        self.authority_select.currentIndexChanged.connect(self.authority_update)
        self.occupancy_toggle_button.clicked.connect(self.occupancy_update)
        self.track_signal_block_select.currentIndexChanged.connect(self.track_signal_block_update)
        self.speed_input.editingFinished.connect(self.update_speed)
        self.send_ctc_inputs_button.clicked.connect(self.send_ctc_inputs)
        self.send_track_inputs_button.clicked.connect(self.send_track_inputs)
        self.toggle_switch_select.currentIndexChanged.connect(self.toggle_switch_selected)
        self.toggle_block_select.currentIndexChanged.connect(self.toggle_block_selected)

        # Connect external signals
        self.signals.send_blocks_signal.connect(self.set_blocks)
        self.signals.send_blocks_occupancy_signal.connect(self.set_blocks_occupancy)
        self.signals.send_switches_signal.connect(self.set_switches)

        # send init signals
        self.signals.get_blocks_signal.emit()
        self.signals.get_blocks_occupancy_signal.emit()
        self.signals.get_switches_signal.emit()

        # Initialization:
        self.init_authority_select()
        self.update_occupancy_block_select()
        self.init_block_list()
        self.init_close_block_select()
        self.init_toggle_switch_select()

    @pyqtSlot(dict)
    def set_blocks_occupancy(self, block_occupancy_dict: dict):
        self.blocks_occupancy = block_occupancy_dict

    @pyqtSlot(list)
    def set_blocks(self, blocks: list):
        self.blocks = blocks

    @pyqtSlot(list)
    def set_switches(self, switches: list):
        self.switches = switches

    def init_close_block_select(self):
        self.toggle_block_select.clear()
        self.toggle_block_select.addItem("None")
        for block in self.blocks:
            self.toggle_block_select.addItem(str(block))

    def init_toggle_switch_select(self):
        self.toggle_switch_select.clear()
        self.toggle_switch_select.addItem("None")
        for switch in self.switches:
            self.toggle_switch_select.addItem(f"Switch b{str(switch.block)}")


    @pyqtSlot()
    def toggle_block_selected(self):
        if self.toggle_block_select.currentIndex() != 0:
            if (self.toggle_block_select.currentIndex()) < 58:
                self.signals.block_to_toggle.emit(self.toggle_block_select.currentIndex())
            else:
                self.signals.block_to_toggle.emit(self.toggle_block_select.currentIndex() + 4)

    def toggle_switch_selected(self):
        if self.toggle_switch_select.currentIndex() != 0:
            self.signals.switch_to_toggle.emit([self.switches[self.toggle_switch_select.currentIndex() - 1]])

    def init_authority_select(self):
        self.authority_select.clear()
        for authority in self.authority:
            self.authority_select.addItem(str(authority))
            self.authority_select.adjustSize()

    def update_occupancy_block_select(self):

        self.occupancy_block_select.clear()

        for block, occupancy in self.blocks_occupancy.items():
            self.occupancy_block_select.addItem(str(block) + " " + str(occupancy))

        # self.show()

    def init_block_list(self):
        self.track_signal_block_select.clear()
        for block in self.blocks:
            self.track_signal_block_select.addItem(str(block))
            self.occupancy_block_select.adjustSize()

    def authority_update(self):
        self.signals.track_signal_authority_update_signal.emit(self.authority_select.currentIndex())
        # self.test_business_logic.track_signal_authority_update(authority=self.authority_select.currentIndex())

    def occupancy_update(self):
        if (self.occupancy_block_select.currentIndex() + 1) < 58:
            self.blocks_occupancy[self.occupancy_block_select.currentIndex() + 1] \
                = not self.blocks_occupancy[self.occupancy_block_select.currentIndex() + 1]
        else:
            self.blocks_occupancy[self.occupancy_block_select.currentIndex() + 5] \
                = not self.blocks_occupancy[self.occupancy_block_select.currentIndex() + 5]

        self.signals.occupancy_update_signal.emit(self.blocks_occupancy)
        # self.test_business_logic.occupancy_update(blocks_occupancy=self.blocks_occupancy)

        self.update_occupancy_block_select()

    def track_signal_block_update(self):
        block_list_index = self.track_signal_block_select.currentIndex()
        block = self.blocks[block_list_index]
        self.signals.track_signal_block_update_signal.emit(block)
        # self.test_business_logic.track_signal_block_update(block)

    def update_speed(self):
        text = self.speed_input.text()  # checking to see if it is a valid integer
        if text.isnumeric() or text.replace(".", "").isnumeric():  # text must be an int or float
            value = float(text)
            if value >= 0:
                self.signals.track_signal_speed_update_signal.emit(value)
                # self.test_business_logic.track_signal_speed_update(value)

    def send_ctc_inputs(self):
        self.signals.send_ctc_inputs_signal.emit()
        # self.test_business_logic.send_ctc_inputs()

    def send_track_inputs(self):
        self.signals.send_track_inputs_signal.emit()
        # self.test_business_logic.send_track_inputs()
