from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication

from Track_Controller_SW.lighting import Light
from Track_Controller_SW.TestbenchContainer import TestbenchContainer
from Track_Controller_SW.TrackControllerUI import UI
from Track_Controller_SW.BusinessLogic import BusinessLogic
from Track_Controller_SW.PLC_Logic import PlcProgram
from Track_Controller_SW.switching import Switch




class TrackController(QObject):
    switch_changed_index_signal = pyqtSignal(int)
    light_changed_signal = pyqtSignal(int)

    def __init__(self, occupancy_list: list, section: str):
        super().__init__()
        if section == "A":
            self.block_indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9,
                                  10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                                  20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                                  30, 31, 32]
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
        elif section == "C":
            self.block_indexes = [73, 74, 75, 76, 77, 78, 79,
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
        self.occupancy_list = occupancy_list
        self.zero_speed_flag_list = [False] * len(self.occupancy_list)
        self.section = section

        self.business_logic = BusinessLogic(
            self.occupancy_list,
            self.switches_list,
            self.lights_list,
            self.plc_logic,
            self.block_indexes,
            self.section
        )
        self.testbench_container = TestbenchContainer(self.business_logic)
        self.business_logic.switch_changed_index_signal.connect(self.send_switch_changed_index)

    def send_switch_changed_index(self, switch_block: int):
        self.switch_changed_index_signal.emit(switch_block)
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
            self.zero_speed_flag_list[29:33] = self.business_logic.occupancy_changed(block_occupancy_list)
        # if self.section == "C":
        #     self.zero_speed_flag_list[]
        self.occupancy_list = block_occupancy_list
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
    track_controller = TrackController([False]*36, "A")
    track_controller.show_ui()


if __name__ == "__main__":
    main()
