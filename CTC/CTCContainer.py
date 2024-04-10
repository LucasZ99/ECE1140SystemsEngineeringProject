from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QApplication
from CTC import CTC, GREEN_LINE, TRACK
from CTC.CTC_UI_Main import CTCMainWindow
from SystemTime import SystemTimeContainer
from Common import Switch, Light, RRCrossing

import time as python_time


class CTCContainer(QObject):
    update_wayside_from_ctc_signal = pyqtSignal(list, bool, list, list)

    def __init__(self, system_time_container: SystemTimeContainer):
        init_start_time = python_time.time()
        print("Initializing CTCContainer t={0}".format(init_start_time))

        super().__init__()
        self.system_time = system_time_container.system_time
        self.ctc = CTC(self.system_time)
        self.ctc.update_wayside_from_ctc_signal.connect(self.update_wayside_from_ctc_signal)

        init_end_time = python_time.time()
        print("Initializing CTCContainer Done. t={0}".format(init_end_time))
        print("CTCContainer Initialization time t={0}".format(init_end_time - init_start_time))

    def show_ui(self):
        app = QApplication.instance()  # Get the QApplication instance

        # app_flag = False
        if app is None:
            app = QApplication([])  # If QApplication instance doesn't exist, create a new one
            # app_flag = True

        print("before ui call")
        self.ui = CTCMainWindow(self.ctc, self.system_time)
        print("before ui show")
        self.ui.show()
        print("After ui show")

        # if app_flag is True:
        app.exec()

    @pyqtSlot(list, bool, list, list)
    def update_wayside_from_ctc(self, authority_speed_update: list[tuple[int, int, float]],
                                maintenance_mode_override_flag: bool,
                                blocks_to_close_open: list[tuple[int, bool]],
                                updated_switches: list[Switch]):
        print("CTCContainer: update_wayside_from_ctc")
        # TODO: Update authority_speed_update to be a TrackSignal before emitting the signal
        # TODO: Define the types for this signal at the top of this file
        self.update_wayside_from_ctc_signal.emit(authority_speed_update,
                                                 maintenance_mode_override_flag,
                                                 blocks_to_close_open,
                                                 updated_switches)

    @pyqtSlot(dict, list, list, list)
    def update_ctc_from_wayside(self,
                                block_occupancy_update: dict[int, bool],
                                switch_positions: list[Switch],
                                light_states: list[Light],
                                rr_crossing_states: list[RRCrossing]):
        self.ctc.update_switch_positions(switch_positions)
        self.ctc.update_signal_statuses(light_states)
        self.ctc.update_railroad_crossing_statuses(rr_crossing_states)
        self.ctc.update_block_occupancies(block_occupancy_update)

        track_signals_to_wayside = self.ctc.set_track_signals()

        # send update to wayside
        self.update_wayside_from_ctc_signal.emit(track_signals_to_wayside,
                                                 False,
                                                 [],
                                                 [])

    @pyqtSlot(int)
    def update_ctc_from_track_model(self, ticket_sales:int):
        self.ctc.update_ticket_sales(ticket_sales)
