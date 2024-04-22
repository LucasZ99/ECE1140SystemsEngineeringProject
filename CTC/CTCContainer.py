from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QApplication
from CTC import CTCSignals, CTC
from CTC.CTC_UI_Main import CTCMainWindow
from Common import Switch, Light, RRCrossing, TrackSignal
from TopLevelSignals import TopLevelSignals

import time as python_time


class CTCContainer(QObject):
    def __init__(self):
        self.ui = None
        init_start_time = python_time.time()
        print("Initializing CTCContainer t={0}".format(init_start_time))
        super().__init__()

        TopLevelSignals.update_ctc_from_wayside.connect(self.update_ctc_from_wayside_slot)

        self.ctc = CTC()
        self.ctc.update_wayside_from_ctc_signal.connect(self.update_wayside_from_ctc_slot)

        # self.ctc.update_wayside_from_ctc_signal.connect(self.update_wayside_from_ctc)
        print("CTC wired to CTC container")

        # self.ctc.send_initial_message()
        # self.ui = CTCMainWindow()

        init_end_time = python_time.time()
        print("Initializing CTCContainer Done. t={0}".format(init_end_time))
        print("CTCContainer Initialization time t={0}".format(init_end_time - init_start_time))

    # def show_ui(self):
    #     print("before ui show")
    #     self.ui.show()
    #     print("CTCContainer.show_ui: After ui show")

    @pyqtSlot(list, list, list)
    def update_wayside_from_ctc_slot(self, track_signals: list[TrackSignal],
                                     blocks_to_close_open: list[tuple[int, bool]],
                                     updated_switches: list[Switch]):
        print("CTCContainer: update_wayside_from_ctc")
        # TODO: Update authority_speed_update to be a TrackSignal before emitting the signal
        # TODO: Define the types for this signal at the top of this file

        TopLevelSignals.update_wayside_from_ctc.emit(track_signals, blocks_to_close_open, updated_switches)

    @pyqtSlot(dict, list, list, list)
    def update_ctc_from_wayside_slot(self,
                                block_occupancy_update: dict[int, bool],
                                switch_positions: list[Switch],
                                light_states: list[Light],
                                rr_crossing_states: list[RRCrossing]):
        print("CTCContainer: Block occupancy update received from Wayside")
        self.ctc.wayside_event_handler(block_occupancy_update, switch_positions, light_states, rr_crossing_states)

    @pyqtSlot(int)
    def update_ctc_from_track_model(self, ticket_sales: int):
        self.ctc.update_ticket_sales(ticket_sales)
