import sys

from PyQt6.QtWidgets import QApplication

from BusinessLogic import BusinessLogic
import PLC_Logic
from switching import Switch
import TrackControllerUI


class TrackController(object):
    def __init__(self):
        self.switches_list = \
            [
                Switch(5, 6, 11, 6),
            ]

        self.plc_logic = PLC_Logic.PlcProgram()
        self.occupancy_list = [False] * 16
        self.authority = 0
        self.suggested_speed_list = [0]

        self.business_logic = BusinessLogic(
            self.occupancy_list,
            self.switches_list,
            self.authority,
            self.suggested_speed_list,
            self.plc_logic)

    def run(self) -> None:
        pass

    # Calling track model endpoints

    # Calling ctc endpoints
    def update_ctc_occupancy(self):
        pass

    # CTC endpoints
    def update_switch(self, line_id: int, block_id: int, switch_status: Switch) -> None:
        pass

    def set_block_maintenance(self, line_id: int, block_index: int, open: bool) -> None:
        pass

    def command_speed(self, line_id: int, block_id: int, speed: float) -> None:
        pass

    def set_authority(self, line_id: int, block_id: int, authority: int) -> None:
        pass

    # Track Model endpoints
    def update_occupancy(self, block_occupancy_list: list[bool]) -> None:
        pass

    def show_ui(self):
        app = QApplication(sys.argv)
        ui = TrackControllerUI.UI(self.business_logic)
        ui.show()
        app.exec()


def main():
    track_controller = TrackController()
    track_controller.show_ui()


if __name__ == "__main__":
    main()
