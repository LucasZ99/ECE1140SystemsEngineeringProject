import sys

from PyQt6.QtWidgets import QApplication

from BusinessLogic import BusinessLogic
import PLC_Logic
from switching import Switch
import TrackControllerUI


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

        self.plc_logic = PLC_Logic.PlcProgram()
        self.occupancy_list = occupancy_list
        self.authority = 0
        self.suggested_speed_list = [0]
        self.zero_speed_flag_list = [False] * len(self.occupancy_list)
        self.section = section

        self.business_logic = BusinessLogic(
            self.occupancy_list,
            self.switches_list,
            self.authority,
            self.suggested_speed_list,
            self.plc_logic,
            self.block_indexes,
            self.section
        )

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
        app = QApplication(sys.argv)
        ui = TrackControllerUI.UI(self.business_logic)
        ui.show()
        app.exec()

# def main():
#     track_controller = TrackController()
#     track_controller.show_ui()
#
#
# if __name__ == "__main__":
#     main()
