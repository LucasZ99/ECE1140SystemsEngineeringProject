from PyQt6.QtCore import QObject, pyqtSlot
from CTCTest.CTCTestSignals import CTCTestSignals
from CTCTest.CTCTestUI import CTCTestUI
from CTCTest.TrackControllerModel import TrackControllerModel
from Common import Light, RRCrossing, Switch, TrackSignal
from TopLevelSignals import TopLevelSignals


class CTCTestContainer(QObject):
    def __init__(self):
        super().__init__()
        self.track_controller = TrackControllerModel()
        self.ui = CTCTestUI()
        self.track_controller.init_frontend()

        # connect to top level signal
        CTCTestSignals.update_ctc_from_wayside.connect(self.update_ctc_from_wayside)
        TopLevelSignals.update_wayside_from_ctc.connect(self.update_wayside_from_ctc)

    @pyqtSlot(dict, list, list, list)
    def update_ctc_from_wayside(self, block_occupancies: dict[int: bool], switches: list[Switch],
                                lights: list[Light], crossings: list[RRCrossing]):
        TopLevelSignals.update_ctc_from_wayside.emit(block_occupancies, switches, lights, crossings)

    @pyqtSlot(list, list, list)
    def update_wayside_from_ctc(self, track_signals: list[TrackSignal], blocks_to_open_close: list[tuple[int, bool]],
                                switch_positions: list[Switch]):
        self.track_controller.update_track_signals(track_signals)
