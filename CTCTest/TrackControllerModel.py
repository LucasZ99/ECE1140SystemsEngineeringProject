from PyQt6.QtCore import QObject

from Common import TrackSignal
from Common.GreenLine import *



VACANT = "VACANT"
OCCUPIED = "OCCUPIED"
MAINTENANCE = "MAINTENANCE"

BLOCK_MODES = [VACANT, OCCUPIED, MAINTENANCE]


class TrackControllerModel(QObject):
    def __init__(self):
        super().__init__()
        self.block_occupancies = {}
        self.switches = {}
        self.signals = {}
        self.rr_crossings = {}

        for block in GREEN_LINE[BLOCKS]:
            self.block_occupancies[block] = VACANT

        for switch in GREEN_LINE[SWITCHES]:
            self.switches[switch.block] = switch

        for signal in GREEN_LINE[LIGHTS]:
            self.signals[signal.block] = signal

        for rr_crossing in GREEN_LINE[CROSSINGS]:
            self.rr_crossings[rr_crossing.block] = rr_crossing

    # define to/from CTC endpoints
    def update_wayside_from_ctc(self,
                                authority_speed_update: list[TrackSignal],
                                maintenance_mode_override_flag: bool,
                                blocks_to_close_open: list[tuple[int, bool]],
                                updated_switches: list[Switch]):
        pass

