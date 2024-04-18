from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QApplication
from CTC import CTC
from CTC.CTC_UI_Main import CTCMainWindow
from Common import Switch, Light, RRCrossing

import time as python_time


class CTCContainer(QObject):
    update_wayside_from_ctc_signal = pyqtSignal(list, bool, list, list)

    def __init__(self):
        self.ui = None
        init_start_time = python_time.time()
        print("Initializing CTCContainer t={0}".format(init_start_time))
        super().__init__()
        self.ctc = CTC()
        # self.ctc.update_wayside_from_ctc_signal.connect(self.update_wayside_from_ctc)
        print("CTC wired to CTC container")

        # self.ctc.send_initial_message()
        self.ui = CTCMainWindow(self.ctc)

        init_end_time = python_time.time()
        print("Initializing CTCContainer Done. t={0}".format(init_end_time))
        print("CTCContainer Initialization time t={0}".format(init_end_time - init_start_time))

    def show_ui(self):
        print("before ui show")
        self.ui.show()
        print("CTCContainer.show_ui: After ui show")

    # @pyqtSlot(list, bool, list, list)
    # def update_wayside_from_ctc(self, authority_speed_update: list[tuple[int, int, float]],
    #                             maintenance_mode_override_flag: bool,
    #                             blocks_to_close_open: list[tuple[int, bool]],
    #                             updated_switches: list[Switch]):
    #def update_wayside_from_ctc(self, track_controller_ref):
    def update_wayside_from_ctc(self):
        # print("CTCContainer: update_wayside_from_ctc")
        # TODO: Update authority_speed_update to be a TrackSignal before emitting the signal
        # TODO: Define the types for this signal at the top of this file
        # print(f"\t{self.ctc.authority_speed_update.__len__()}")
        self.update_wayside_from_ctc_signal.emit(self.ctc.authority_speed_update,
                                                 self.ctc.maintenance_mode_override_flag,
                                                 self.ctc.blocks_to_close_open,
                                                self.ctc.updated_switches)
        # track_controller_ref.update_test_container_from_ctc_slot(self.ctc.authority_speed_update, False, [], [])
        # switch_positions = track_controller_ref.track_controller.switches
        # light_states = track_controller_ref.track_controller.signals
        # rr_crossing_states = track_controller_ref.track_controller.rr_crossings

        # track_controller_ref.update_test_container_from_ctc_slot(self.ctc.authority_speed_update, False, [], [])
        # block_occupancy_update = track_controller_ref.track_controller.block_occupancies
        # switch_positions = []
        # rr_crossing_states = []
        # light_states = []
        #
        # self.ctc.authority_speed_update.clear()
        # self.ui.update_time()
        # self.ctc.update_ctc_queues()
        # #print("update running trains")
        # self.ctc.update_block_occupancies(block_occupancy_update)
        # running_trains_updated = self.ctc.update_running_trains()
        # print("update switch positions")
        #self.ctc.update_switch_positions(switch_positions)
        # print("update signals")
        #self.ctc.update_signal_statuses(light_states)
        # print("update rr crossings")
        #self.ctc.update_railroad_crossing_statuses(rr_crossing_states)
        # print("update block occupancies")
        #print("set track signals")
        #if update_track_signals:
        # if running_trains_updated:
        #     self.ctc.set_track_signals()

    @pyqtSlot(dict, list, list, list)
    def update_ctc_from_wayside(self,
                                block_occupancy_update: dict[int, bool],
                                switch_positions: list[Switch],
                                light_states: list[Light],
                                rr_crossing_states: list[RRCrossing]):
        self.ctc.authority_speed_update.clear()
        self.ui.update_time()
        self.ctc.update_ctc_queues()
        # print("update running trains")
        self.ctc.update_block_occupancies(block_occupancy_update)
        self.ctc.update_running_trains()
        # self.ui.update_time()
        # #print("update ctc queues")
        #queues_updated = self.ctc.update_ctc_queues()
        # #print("update running trains")
        # update_track_signals = self.ctc.update_running_trains()
        #self.ui.refresh_ctc_schedule_data()
        # #print("update switch positions")
        # self.ctc.update_switch_positions(switch_positions)
        # #print("update signals")
        # self.ctc.update_signal_statuses(light_states)
        # #print("update rr crossings")
        # self.ctc.update_railroad_crossing_statuses(rr_crossing_states)
        # #print("update block occupancies")
        # self.ctc.update_block_occupancies(block_occupancy_update)
        # #print("set track signals")
        # if update_track_signals:
        #      self.ctc.set_track_signals()

    @pyqtSlot(int)
    def update_ctc_from_track_model(self, ticket_sales:int):
        self.ctc.update_ticket_sales(ticket_sales)
