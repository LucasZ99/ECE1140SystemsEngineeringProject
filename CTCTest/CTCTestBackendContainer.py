from PyQt6.QtCore import QObject, pyqtSlot

from CTC import CTCSignals
from CTCTest.CTCTestSignals import CTCTestSignals
from CTCTest.TrackControllerModel import TrackControllerModel
from Common import TrackSignal, Switch, Light, RRCrossing
from TopLevelSignals import TopLevelSignals


class CTCTestBackendContainer(QObject):
    def __init__(self):
        super().__init__()
        self.track_controller_model = TrackControllerModel()
        TopLevelSignals.update_wayside_from_ctc.connect(self.update_wayside_from_ctc)
        CTCTestSignals.update_ctc_from_wayside.connect(self.update_ctc_from_wayside)
        print("Track Controller Backend init")

    @pyqtSlot(list, list, list)
    def update_wayside_from_ctc(self, track_signals: list[TrackSignal], blocks_to_close_open: list[tuple[int, bool]],
                                switch_positions: list[Switch]):
        print("CTCTestBackendContainer: update wayside from ctc")
        CTCTestSignals.update_wayside_from_ctc.emit(track_signals, blocks_to_close_open, switch_positions)

    @pyqtSlot(dict, list, list, list)
    def update_ctc_from_wayside(self, block_occupancies: dict[int, bool],
                                switch_positions: list[Switch],
                                light_states: list[Light],
                                rr_crossing_states: list[RRCrossing]):
        TopLevelSignals.update_ctc_from_wayside.emit(block_occupancies, switch_positions, light_states,
                                                     rr_crossing_states)
