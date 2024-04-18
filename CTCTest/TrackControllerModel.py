from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from Common import TrackSignal
from Common.GreenLine import *

VACANT = False
OCCUPIED = True


class TrackControllerModel(QObject):
    update_ctc_from_wayside_signal = pyqtSignal(dict, list, list, list)
    update_test_ui_speeds_authorities = pyqtSignal(list)

    def __init__(self):
        print("Track Controller Model init")
        super().__init__()
        self.block_occupancies: [int, bool] = {}
        self.switches = {}
        self.signals = {}
        self.rr_crossings = {}

        self.updated_railroad_crossing_states = []
        self.track_signals = {}

        for block in GREEN_LINE[BLOCKS]:
            self.block_occupancies[block] = VACANT

        for block in GREEN_LINE[BLOCKS]:
            self.track_signals[block] = TrackSignal(block, 0, 0)

        for switch in GREEN_LINE[SWITCHES]:
            self.switches[switch.block] = switch

        for signal in GREEN_LINE[LIGHTS]:
            self.signals[signal.block] = signal

        for rr_crossing in GREEN_LINE[CROSSINGS]:
            self.rr_crossings[rr_crossing.block] = rr_crossing

    def get_occupancy_updates(self) -> dict[int: bool]:
        return self.block_occupancies

    @pyqtSlot(list, bool, list, list)
    def update_wayside_from_ctc(self, track_signals: list[TrackSignal],
                                maintenance_mode_override: bool,
                                blocks_to_set_mode: list[tuple[int, bool]],
                                switches: list[Switch]):
        if track_signals.__len__() > 0:
            # print("wayside: updating track signals")
            for track_signal in track_signals:
                self.track_signals[track_signal.block_id] = track_signal
            self.update_test_ui_speeds_authorities.emit(track_signals)
            track_signals.clear()

        # self.update_ctc_from_wayside_signal.emit(self.block_occupancies, [], [], [])

    def update_block_occupancy(self, block_id: int, status: bool):
        self.block_occupancies[block_id] = status
        print(GREEN_LINE[BLOCKS][block_id].name, status)
        # self.updated_occupancies[block_id] = status
