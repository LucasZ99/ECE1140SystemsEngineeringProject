from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication

from Track_Controller_SW import RRCrossing
from Track_Controller_SW.lighting import Light
from Track_Controller_SW.TestbenchContainer import TestbenchContainer
from Track_Controller_SW.TrackControllerUI import UI
from Track_Controller_SW.BusinessLogic import BusinessLogic
from Track_Controller_SW.PLC_Logic import PlcProgram
from Track_Controller_SW.switching import Switch


class TrackController(QObject):
    switch_changed_index_signal = pyqtSignal(int)
    rr_crossing_signal = pyqtSignal(bool)
    lights_list_A_changed_signal = pyqtSignal(list)
    lights_list_C_changed_signal = pyqtSignal(list)

    def __init__(self, occupancy_dict: dict[int, bool], section: str):
        super().__init__()
        if section == "A":
            self.block_indexes = occupancy_dict.keys()
            print(f"Block indexes for section A: {self.block_indexes}")
            self.switches_list = \
                [
                    Switch(13, 12, 1, 12),
                    Switch(28, 29, 150, 29)
                ]
            self.lights_list = \
                [
                    Light(12, True),
                    Light(1, False),
                    Light(29, True),
                    Light(150, False)
                ]
            self.rr_crossing = \
                [
                    RRCrossing(19, False)
                ]
        elif section == "C":
            self.block_indexes = [77, 78, 79,
                                  80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
                                  90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
                                  100, 101, 102, 103, 104]
            self.switches_list = \
                [
                    Switch(77, 76, 101, 76),
                    Switch(85, 86, 100, 86)
                ]
            self.lights_list = \
                [
                    Light(76, True),
                    Light(101, False),
                    Light(86, True),
                    Light(100, False)
                ]

        self.plc_logic = PlcProgram()
        self.occupancy_dict = occupancy_dict
        self.zero_speed_flag_list = [False] * len(self.occupancy_dict)
        self.section = section

        self.business_logic = BusinessLogic(
            self.occupancy_dict,
            self.switches_list,
            self.lights_list,
            self.plc_logic,
            self.block_indexes,
            self.section
        )
        self.testbench_container = TestbenchContainer(self.business_logic)

        self.business_logic.switch_changed_index_signal.connect(self.send_switch_changed_index)
        self.business_logic.rr_crossing_signal.connect(self.rr_crossing_updated)
        self.business_logic.lights_list_signal.connect(self.lights_list_updated)

    @pyqtSlot(int)
    def send_switch_changed_index(self, switch_block: int):
        self.switch_changed_index_signal.emit(switch_block)

    @pyqtSlot(bool)
    def rr_crossing_updated(self, rr_crossing_active: bool):
        self.rr_crossing_signal.emit(rr_crossing_active)

    @pyqtSlot(list)
    def lights_list_updated(self, lights_list: list):
        self.lights_list = lights_list
        if self.section == "A":
            self.lights_list_A_changed_signal.emit(lights_list)
        elif self.section == "C":
            self.lights_list_C_changed_signal.emit(lights_list)

    def run(self) -> None:
        pass

    # CTC endpoints
    def update_switch(self, line_id: int, block_id: int, switch_status: Switch) -> None:
        pass

    def set_block_maintenance(self, line_id: int, block_index: int, open: bool) -> None:
        pass

    def set_authority(self, line_id: int, block_id: int, authority: int) -> None:
        pass

    # Track Model endpoints
    def update_occupancy(self, block_occupancy_list: list[bool]):
        if self.section == "A":
            # update the zero_speed flag list
            self.zero_speed_flag_list[23:27] = self.business_logic.occupancy_changed(block_occupancy_list)
        if self.section == "C":
            self.zero_speed_flag_list[77:81] = self.business_logic.occupancy_changed(block_occupancy_list)
        self.occupancy_dict = block_occupancy_list
        return self.zero_speed_flag_list

    def show_ui(self):
        app = QApplication.instance()  # Get the QApplication instance

        # app_flag = False
        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one
            # app_flag = True

        print("before ui call")
        self.ui = UI(self.business_logic)
        print("before ui show")
        self.ui.show()
        print("After ui show")

        # if app_flag is True:
        app.exec()

    def show_testbench_ui(self):
        self.testbench_container.show_ui()


def main():
    track_controller = TrackController([False] * 36, "A")
    track_controller.show_ui()


if __name__ == "__main__":
    main()
