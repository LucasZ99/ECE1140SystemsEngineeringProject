from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from CTCTest.CTCTestSignals import CTCTestSignals
from Common import TrackSignal
from Common.GreenLine import *

VACANT = False
OCCUPIED = True


class TrackControllerModel(QObject):
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

        self.connect_to_frontend_signals()

    def get_occupancy_updates(self) -> dict[int: bool]:
        return self.block_occupancies

    @pyqtSlot(list, list, list)
    def update_wayside_from_ctc(self, track_signals: list[TrackSignal],
                                blocks_to_set_mode: list[tuple[int, bool]],
                                switches: list[Switch]):
        if track_signals.__len__() > 0:
            # print("wayside: updating track signals")
            for track_signal in track_signals:
                self.track_signals[track_signal.block_id] = track_signal
                CTCTestSignals.ui_update_track_signal.emit(track_signal)
            track_signals.clear()

        # self.update_ctc_from_wayside_signal.emit(self.block_occupancies, [], [], [])

    @pyqtSlot(int, bool)
    def update_block_occupancy(self, block_id: int, status: bool):
        print("block occupancy received")
        self.block_occupancies[block_id] = status
        print(GREEN_LINE[BLOCKS][block_id].name, status)
        self.update_ctc_from_wayside()

    def update_ctc_from_wayside(self):
        CTCTestSignals.update_ctc_from_wayside.emit(self.block_occupancies, list(self.switches.values()), list(self.signals.values()), list(self.rr_crossings.values()))

    def connect_to_frontend_signals(self):
        CTCTestSignals.wayside_update_block_occupancy.connect(self.update_block_occupancy)

    def init_frontend(self):
        for block in GREEN_LINE[BLOCKS]:
            print("track signal for block {0} sent".format(GREEN_LINE[BLOCKS][block].id()))
            CTCTestSignals.ui_update_track_signal.emit(TrackSignal(GREEN_LINE[BLOCKS][block].id(), 0, 0))

