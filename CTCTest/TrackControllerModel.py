from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from Common import TrackSignal
from Common.GreenLine import *

VACANT = False
OCCUPIED = True


class TrackControllerModel(QObject):
    update_ctc_from_wayside_signal = pyqtSignal(dict, list, list, list)
    update_test_ui_speeds_authorities = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.block_occupancies = {}
        self.switches = {}
        self.signals = {}
        self.rr_crossings = {}

        self.updated_occupancies = {}
        self.updated_switches = []
        self.updated_lights = []
        self.updated_railroad_crossing_states = []

        for block in GREEN_LINE[BLOCKS]:
            self.block_occupancies[block] = VACANT

        for switch in GREEN_LINE[SWITCHES]:
            self.switches[switch.block] = switch

        for signal in GREEN_LINE[LIGHTS]:
            self.signals[signal.block] = signal

        for rr_crossing in GREEN_LINE[CROSSINGS]:
            self.rr_crossings[rr_crossing.block] = rr_crossing

    # define to/from CTC endpoints
    # @pyqtSlot(list, bool, list, list)
    # def update_wayside_from_ctc(self,
    #                             authority_speed_update: list[TrackSignal],
    #                             maintenance_mode_override_flag: bool,
    #                             blocks_to_close_open: list[tuple[int, bool]],
    #                             updated_switches: list[Switch]):
    #     self.update_test_ui_speeds_authorities.emit(authority_speed_update)
    #     self.update_ctc_from_wayside(self.changed_occupancies, self.updated_switches, self.updated_lights, self.updated_railroad_crossing_states)

    def update_ctc_from_wayside(self,
                                block_occupancy_update: dict[int, bool],
                                switch_positions: list[Switch],
                                light_states: list[Light],
                                rr_crossing_states: list[RRCrossing]):
        self.update_ctc_from_wayside_signal.emit(block_occupancy_update, switch_positions, light_states, rr_crossing_states)

    def update_block_occupancy(self, block_id: int, status: bool):
        self.block_occupancies[block_id] = status
        print(GREEN_LINE[BLOCKS][block_id].name, status)
        self.update_ctc_from_wayside_signal.emit({block_id: status}, [], [], [])
