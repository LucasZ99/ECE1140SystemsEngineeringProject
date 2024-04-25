import os

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, \
    QListWidgetItem, QButtonGroup, QListWidget
from PyQt6.uic import loadUi

from Common import Switch
from Track_Controller_SW.TrackControllerSignals import TrackControllerSignals as signals


class ManualMode(QWidget):

    def __init__(self, section: str):
        super().__init__()
        self.section = section
        self.setWindowTitle(f"Maintenance Mode {self.section}")
        self.setMinimumSize(200, 200)
        self.layout = QVBoxLayout(self)
        self.switches_list = []
        self.signals = signals
        self.switch_button_group = QButtonGroup()

        # Connect internal signals
        self.switch_button_group.buttonClicked.connect(self.switch_button_pressed)

        # Connect external signals
        if section == 'A':
            self.signals.send_switches_list_A_switch_ui_signal.connect(self.get_switches_list)
            self.signals.get_switches_list_A_switch_ui_signal.emit()
        else:
            self.signals.send_switches_list_C_switch_ui_signal.connect(self.get_switches_list)
            self.signals.get_switches_list_C_switch_ui_signal.emit()

        current_dir = os.path.dirname(__file__)  # setting up to work in any dir
        style_file = os.path.join(current_dir, 'style.css')
        with open(style_file, 'r') as file:
            self.setStyleSheet(file.read())

    @pyqtSlot(list)
    def get_switches_list(self, switches: list):
        self.switches_list = switches

        button_id = 0
        for switch in self.switches_list:
            button = self.switch_button_ret(
                size=200,
                text1=f"Switch at Block {switch.block}")

            self.switch_button_group.addButton(button, button_id)
            button_id += 1
            self.layout.addWidget(button)

    def switch_button_pressed(self, button: QPushButton) -> None:
        if self.section == 'A':
            self.signals.maintenance_switch_changed_A_signal.emit(self.switch_button_group.id(button))
        else:
            self.signals.maintenance_switch_changed_C_signal.emit(self.switch_button_group.id(button))

    def switch_button_ret(self, size=None, text1=None, checkable=True, style1=None, style2=None):
        button = QPushButton()
        button.setCheckable(checkable)
        button.setFixedHeight(24)
        if checkable:
            if text1:
                button.setText(text1)
            else:
                button.setText("Off")
        if size:
            button.setFixedWidth(size)
        return button


class UI(QMainWindow):
    def __init__(self, section: str):

        super(UI, self).__init__()
        self.section = section
        self.fname = "filename"
        self.switch_list_widget = None
        self.block_number = None
        self.manual_mode_window = None
        self.lights_list = None
        self.signals = signals

        # load ui
        current_dir = os.path.dirname(__file__)  # setting up to work in any dir
        ui_path = os.path.join(current_dir, 'TrackController.ui')


        try:
            loadUi(ui_path, self)
        except Exception as e:
            print("Error with loading UI file: ", e)

        style_file = os.path.join(current_dir, 'style.css')
        with open(style_file, 'r') as file:
            self.setStyleSheet(file.read())

        self.setWindowTitle(f"Track Controller {self.section}")


        # Define widgets
        self.manual_mode = self.findChild(QPushButton, 'manual_mode')
        self.browse_button = self.findChild(QPushButton, 'browse')
        self.filename = self.findChild(QLabel, 'filename')
        # self.occupancy_disp = self.findChild(QListWidget, 'block_number')
        self.light_1_a = self.findChild(QPushButton, 'light_1_a')
        self.light_1_a.setStyleSheet("background-color: rgb(0, 224, 34)")
        self.light_1_b = self.findChild(QPushButton, 'light_1_b')
        self.light_1_b.setStyleSheet("background-color: rgb(222, 62, 38)")
        self.light_2_a = self.findChild(QPushButton, 'light_2_a')
        self.light_2_a.setStyleSheet("background-color: rgb(0, 224, 34)")
        self.light_2_b = self.findChild(QPushButton, 'light_2_b')
        self.light_2_b.setStyleSheet("background-color: rgb(222, 62, 38)")
        self.rr_crossing = self.findChild(QPushButton, 'rr_crossing_button')
        self.rr_crossing.setStyleSheet("background-color: rgb(0, 224, 34)")
        # self.tb_button = self.findChild(QPushButton, 'tb_button')
        self.block_number = self.findChild(QListWidget, 'block_number')

        # Connect outside signals
        if self.section == "A":

            # Initialize / update switch list
            self.signals.send_switches_list_A_signal.connect(self.update_switches)

            # Initialize / update occupancy list
            self.signals.send_occupancy_A_signal.connect(self.update_occupancy)

            # Initialize lights
            self.signals.init_lights_A_signal.connect(self.init_lights)

            # Update light
            self.signals.send_lights_A_signal.connect(self.update_lights)

            # Initialize filename
            self.signals.send_filename_A_signal.connect(self.init_filename)

            # Update RR crossing
            self.signals.send_rr_crossing_A_signal.connect(self.activate_rr_crossing)

            self.signals.get_switches_list_A_signal.emit()
            self.signals.get_occupancy_A_signal.emit()
            self.signals.get_lights_A_signal.emit()
            self.signals.get_filename_A_signal.emit()

        else:  # section is C
            # Initialize / update switch list
            self.signals.send_switches_list_C_signal.connect(self.update_switches)

            # Initialize / update occupancy list
            self.signals.send_occupancy_C_signal.connect(self.update_occupancy)

            # Initialize lights
            self.signals.init_lights_C_signal.connect(self.init_lights)

            # Update light
            self.signals.send_lights_C_signal.connect(self.update_lights)

            # Initialize filename
            self.signals.send_filename_C_signal.connect(self.init_filename)

            # No RR crossing
            self.rr_crossing.hide()

            self.signals.get_switches_list_C_signal.emit()
            self.signals.get_occupancy_C_signal.emit()
            self.signals.get_lights_C_signal.emit()
            self.signals.get_filename_C_signal.emit()

        # define internal connections
        self.browse_button.clicked.connect(self.browse_files)
        self.manual_mode.clicked.connect(self.manual_mode_dialogue)

        print("signals emitted from tc ui")

    @pyqtSlot(str)
    def init_filename(self, filename: str):
        self.filename.setText(filename)

    # dynamically updating endpoint called by business logic
    @pyqtSlot(list)
    def update_switches(self, switches_list: list[Switch]) -> None:
        print(f"WAYSIDE_{self.section}: update switches received")
        self.switch_list_widget.clear()
        for switch in switches_list:
            item = QListWidgetItem(str(switch))
            self.switch_list_widget.addItem(item)

    @pyqtSlot(dict)
    def update_occupancy(self, occupancy_dict: dict) -> None:
        self.block_number.clear()
        for index, occupancy in occupancy_dict.items():
            item = QListWidgetItem(str(index) + " " + str(occupancy))
            self.block_number.addItem(item)

    @pyqtSlot(list)
    def init_lights(self, lights_list: list):
        self.lights_list = lights_list
        self.light_1_a.setText(f"Light @ b{self.lights_list[0].block}")
        self.light_1_b.setText(f"Light @ b{self.lights_list[1].block}")
        self.light_2_a.setText(f"Light @ b{self.lights_list[2].block}")
        self.light_2_b.setText(f"Light @ b{self.lights_list[3].block}")

    # only the signal that should be green is sent
    @pyqtSlot(list)
    def update_lights(self, lights_list: list) -> None:
        self.lights_list = lights_list
        print(f"WAYSIDE_{self.section} UI lights list received: {[str(light) for light in self.lights_list]}")
        if self.lights_list[0].val is True:
            # light 1a green
            self.light_1_a.setStyleSheet("background-color: rgb(0, 224, 34)")
            self.light_1_b.setStyleSheet("background-color: rgb(222, 62, 38)")
        if self.lights_list[1].val is True:
            # light 1b green
            self.light_1_b.setStyleSheet("background-color: rgb(0, 224, 34)")
            self.light_1_a.setStyleSheet("background-color: rgb(222, 62, 38)")
        if self.lights_list[2].val is True:
            # light 2a green
            self.light_2_a.setStyleSheet("background-color: rgb(0, 224, 34)")
            self.light_2_b.setStyleSheet("background-color: rgb(222, 62, 38)")
        if self.lights_list[3].val is True:
            # light 2b green
            self.light_2_b.setStyleSheet("background-color: rgb(0, 224, 34)")
            self.light_2_a.setStyleSheet("background-color: rgb(222, 62, 38)")

    def manual_mode_dialogue(self):
        self.manual_mode_window = ManualMode(section=self.section)
        self.manual_mode_window.adjustSize()
        self.manual_mode_window.show()
        self.show()

    @pyqtSlot(bool)
    def activate_rr_crossing(self, active_bool: bool) -> None:
        if active_bool:
            self.rr_crossing.setText("Railroad Crossing Active")
            self.rr_crossing.setStyleSheet("background-color: rgb(222, 62, 38)")
        else:
            self.rr_crossing.setText("Railroad Crossing Inactive")
            self.rr_crossing.setStyleSheet("background-color: rgb(0, 224, 34)")

    def browse_files(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, 'Open PLC File', 'C:/Users/lucas')
        self.filename.setText(self.fname[-21:])
        self.filename.adjustSize()
        if self.section == 'A':
            self.signals.set_plc_filepath_A_signal.emit(self.fname)
        else:
            self.signals.set_plc_filepath_C_signal.emit(self.fname)

        print("filepath signal sent")

