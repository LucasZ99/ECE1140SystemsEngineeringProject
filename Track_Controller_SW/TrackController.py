import sys
import threading

from PyQt6.QtWidgets import QApplication

from Track_Controller_SW.TestbenchContainer import TestbenchContainer
from Track_Controller_SW.TrackControllerUI import UI
from Track_Controller_SW.BusinessLogic import BusinessLogic
from Track_Controller_SW.PLC_Logic import PlcProgram
from Track_Controller_SW.switching import Switch


class TrackController(object):
    def __init__(self, occupancy_list: list, section: str):
        if section == "A":
            self.block_indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9,
                                  10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                                  20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                                  30, 31, 32,
                                  147, 148, 149, 150]
            self.switches_list = \
                [
                    Switch(13, 12, 1, 12),
                    Switch(28, 29, 150, 29)
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

        self.plc_logic = PlcProgram()
        self.occupancy_list = occupancy_list
        self.suggested_speed_list = [0]
        self.zero_speed_flag_list = [False] * len(self.occupancy_list)
        self.section = section

        self.business_logic = BusinessLogic(
            self.occupancy_list,
            self.switches_list,
            self.suggested_speed_list,
            self.plc_logic,
            self.block_indexes,
            self.section
        )
        self.testbench_container = TestbenchContainer(self.business_logic)

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
        self.zero_speed_flag_list = self.business_logic.occupancy_changed(block_occupancy_list)
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
