import itertools
import sys

from PyQt6.QtCore import pyqtSlot, QObject, QThread
from PyQt6.QtWidgets import QApplication

from Common import Switch, Light, TrackSignal, RRCrossing
from TopLevelSignals import TopLevelSignals as top_level_signals
from Track_Controller_HW import TrackControllerHardware
from Track_Controller_SW import TrackController
from Track_Controller_SW.TrackControllerSignals import TrackControllerSignals as signals
from Track_Controller_SW.TrackControllerUI import UI
import TrackControllerTest


class TrackControllerContainer(QObject):

    def __init__(self):
        super().__init__()

        self.top_level_signals = top_level_signals
        self.signals = signals

        self.occupancy_dict = {}
        self.zero_speed_flag_dict = {}
        self.safe_close_blocks = {}
        self.safe_toggle_switch = [True, True, True, True]
        # Add values from 1 to 57
        for i in range(1, 58):
            self.occupancy_dict[i] = False
            self.zero_speed_flag_dict[i] = False
            self.safe_close_blocks[i] = True
        for i in range(62, 151):
            self.occupancy_dict[i] = False
            self.zero_speed_flag_dict[i] = False
            self.safe_close_blocks[i] = True

        self.switch_list = \
            [
                Switch(13, 12, 1, 12),
                Switch(28, 29, 150, 29),
                Switch(77, 76, 101, 76),
                Switch(85, 86, 100, 86)
            ]

        self.lights_list = \
            [
                Light(12, True),
                Light(1, False),
                Light(29, True),
                Light(150, False),
                Light(76, True),
                Light(101, False),
                Light(86, True),
                Light(100, False)
            ]

        self.rr_crossing_list = \
            [
                RRCrossing(19, False),
                RRCrossing(108, False)
            ]

        # Controller specific initialization
        # THIS HAS BEEN VERIFIED
        # Section A: blocks 1-32
        # overlap: blocks 29, 30, 31, 32
        self.occupancy_dict_A = dict(itertools.islice(self.occupancy_dict.items(), 32))
        # Section B: blocks: 25-80 , 101-150
        # -4 blocks to account for missing blocks 58, 59, 60, 61
        self.occupancy_dict_B = dict(itertools.islice(self.occupancy_dict.items(), 28, 72))
        self.occupancy_dict_B.update(dict(itertools.islice(self.occupancy_dict.items(), 96, 146)))
        # Section C: blocks 77 through 104
        # overlap: blocks 101, 102, 103, 104
        self.occupancy_dict_C = dict(itertools.islice(self.occupancy_dict.items(), 72, 100))

        self.trackControllerA = TrackController(occupancy_dict=self.occupancy_dict_A, section="A")
        self.trackControllerB = TrackControllerHardware(occupancy_dict=self.occupancy_dict_B, section="B")
        self.trackControllerB.slots_sigs.mode = True
        self.trackControllerC = TrackController(occupancy_dict=self.occupancy_dict_C, section="C")

        # # Connect Internal Signals:
        self.signals.track_controller_A_switch_changed_signal.connect(self.update_track_switch)
        self.signals.track_controller_A_rr_crossing_signal.connect(self.update_rr_crossing_status_A)
        self.signals.track_controller_A_lights_changed_signal.connect(self.update_lights_A_status)

        self.signals.track_controller_B_rr_crossing_signal.connect(self.update_rr_crossing_status_B)

        self.signals.track_controller_C_switch_changed_signal.connect(self.update_track_switch)
        self.signals.track_controller_C_lights_changed_signal.connect(self.update_lights_C_status)

        # Connect top level signals:
        # from test bench
        self.top_level_signals.test_update_wayside_from_ctc.connect(self.update_wayside_from_ctc)
        self.top_level_signals.test_update_wayside_from_track_model.connect(self.update_wayside_from_track_model)

        # self.top_level_signals.update_wayside_from_testbench.connect(self.test_continuous_update)

        # from actual modules
        self.top_level_signals.update_wayside_from_ctc.connect(self.update_wayside_from_ctc)
        self.top_level_signals.update_wayside_from_track_model.connect(self.update_wayside_from_track_model)

    # @pyqtSlot()
    # def test_continuous_update(self):
    #     print("WAYSIDE: continuous update")
    #     self.top_level_signals.update_testbench_from_wayside.emit()

    # CTC Endpoint
    @pyqtSlot(list, list, list)
    def update_wayside_from_ctc(self,
                                authority_speed_update: list[TrackSignal],
                                blocks_to_close_open: list[tuple[int, bool]],
                                updated_switches: list[Switch]):

        print("WAYSIDE: update_wayside_from_ctc called")

        self.check_safe_speed(authority_speed_update)

        safe_toggle_blocks = []
        if len(blocks_to_close_open) > 0:
            safe_toggle_blocks = self.check_safe_toggle_block(blocks_to_close_open)
            print(f"safe_toggle_blocks: {safe_toggle_blocks}")
        if len(updated_switches) > 0:
            self.toggle_switch_if_safe(updated_switches)

        print(f"WAYSIDE: update_track_model_from_wayside:\n")
              # f"track signal: {[str(item) for item in authority_speed_update]}\n"
              # f"switch list: {[str(item) for item in self.switch_list]}\n"
              # f"light list: {[str(item) for item in self.lights_list]}\n"
              # f"crossing list: {[str(item) for item in self.rr_crossing_list]}")

        # self.top_level_signals.update_testbench_from_wayside.emit()

        # call downstream endpoint after processing of CTC data
        self.top_level_signals.update_track_model_from_wayside.emit(
            [track_signal.to_tuple() for track_signal in authority_speed_update],
            [switch.to_tuple() for switch in self.switch_list],
            [light.to_tuple() for light in self.lights_list],
            [crossing.to_tuple() for crossing in self.rr_crossing_list],
            safe_toggle_blocks
        )

    # Track Model Endpoint
    @pyqtSlot(dict)
    def update_wayside_from_track_model(self, block_occupancy_update: dict[int, bool]):
        print(f"WAYSIDE: update_wayside_from_track_model received:\n")
              # f"block 62 status: {block_occupancy_update[62]}")

        if self.occupancy_dict != block_occupancy_update:
            self.update_occupancy(block_occupancy_update)

        print(f"WAYSIDE: update_ctc_from_wayside sent:\n")
              # f"block occupancy: {block_occupancy_update}\n"
              # f"switch list: {[str(item) for item in self.switch_list]}\n"
              # f"lights_list: {[str(item) for item in self.lights_list]}\n"
              # f"rr_crossing_list: {[str(item) for item in self.rr_crossing_list]}")

        self.top_level_signals.update_ctc_from_wayside.emit(
            block_occupancy_update,
            self.switch_list,
            self.lights_list,
            self.rr_crossing_list
        )

    def check_safe_speed(self, track_signal: list[TrackSignal]):
        for signal in track_signal:
            if self.zero_speed_flag_dict[signal.block_id]:
                signal.zero_speed()
                print(f"WAYSIDE: Signal for block {signal.block_id} speed has been zeroed")

    def check_safe_toggle_block(self, blocks_to_close_open: list[tuple[int, bool]]):
        safe_toggle_blocks = []
        for item in blocks_to_close_open:
            if item[1]:
                safe_toggle_blocks.append(item[0])
            elif not item[1] and self.safe_close_blocks[item[0]]:
                safe_toggle_blocks.append(item[0])
        return safe_toggle_blocks

    def toggle_switch_if_safe(self, switches_to_toggle: list[Switch]):
        # check if each switch is safe to be toggled
        for switch in switches_to_toggle:
            if switch.block == 13:
                if self.safe_toggle_switch[0] is True:
                    self.signals.maintenance_switch_changed_A_signal.emit(0)
            elif switch.block == 28:
                if self.safe_toggle_switch[1] is True:
                    self.signals.maintenance_switch_changed_A_signal.emit(1)
            elif switch.block == 77:
                if self.safe_toggle_switch[2] is True:
                    self.signals.maintenance_switch_changed_C_signal.emit(0)
            elif switch.block == 85:
                if self.safe_toggle_switch[3] is True:
                    self.signals.maintenance_switch_changed_C_signal.emit(1)

    def update_occupancy(self, block_occupancy_dict: dict[int, bool]):
        print("WAYSIDE: TrackControllerContainer.update_occupancy called")

        # update occupancy dicts with new data
        self.occupancy_dict.update(block_occupancy_dict)
        self.occupancy_dict_A.update(dict(itertools.islice(self.occupancy_dict.items(), 32)))
        self.occupancy_dict_B.update(dict(itertools.islice(self.occupancy_dict.items(), 28, 72)))
        self.occupancy_dict_B.update(dict(itertools.islice(self.occupancy_dict.items(), 96, 146)))
        self.occupancy_dict_C.update(dict(itertools.islice(self.occupancy_dict.items(), 72, 100)))

        # call the update occupancy functions to trigger plc logic and ui updates
        update_occupancy_A_result = self.trackControllerA.update_occupancy(self.occupancy_dict_A)
        zero_speed_flag_dict_A = update_occupancy_A_result[0]
        self.zero_speed_flag_dict.update(zero_speed_flag_dict_A)

        unsafe_close_blocks_A = update_occupancy_A_result[1]
        for block in unsafe_close_blocks_A:
            self.safe_close_blocks[block + 1] = False

        unsafe_toggle_switch = update_occupancy_A_result[2]
        for switch_index in unsafe_toggle_switch:
            self.safe_toggle_switch[switch_index] = False

        update_occupancy_B_result = self.trackControllerB.update_occupancy(self.occupancy_dict_B)
        self.zero_speed_flag_dict_B = update_occupancy_B_result
        for key in self.zero_speed_flag_dict_B.keys():
            self.zero_speed_flag_dict[key] = self.zero_speed_flag_dict_B[key]

        update_occupancy_C_result = self.trackControllerC.update_occupancy(self.occupancy_dict_C)
        zero_speed_flag_dict_C = update_occupancy_C_result[0]
        self.zero_speed_flag_dict.update(zero_speed_flag_dict_C)

        unsafe_close_blocks_C = update_occupancy_C_result[1]
        for block in unsafe_close_blocks_C:
            self.safe_close_blocks[block + 1] = False

        unsafe_toggle_switch = update_occupancy_C_result[2]
        for switch_index in unsafe_toggle_switch:
            self.safe_toggle_switch[switch_index + 2] = False

        print("WAYSIDE: TrackControllerContainer.update_occupancy finished")

    @pyqtSlot(int)
    def update_track_switch(self, switch_block: int) -> None:
        print(f"WAYSIDE: Updating switch at block: {switch_block}")
        for switch in self.switch_list:
            if switch.block == switch_block:
                switch.toggle()

        self.top_level_signals.maintenance_mode_update.emit([switch.to_tuple() for switch in self.switch_list],
                                                            [light.to_tuple() for light in self.lights_list])


    @pyqtSlot(bool)
    def update_rr_crossing_status_A(self, rr_crossing_status: bool) -> None:
        # if the previous status does not equal updated status, toggle the signal
        if self.rr_crossing_list[0].val != rr_crossing_status:
            self.rr_crossing_list[0].toggle()
            print("WAYSIDE: railway crossing status updated for section A")

    @pyqtSlot(bool)
    def update_rr_crossing_status_B(self, rr_crossing_status: bool) -> None:
        if self.rr_crossing_list[1].val != rr_crossing_status:
            self.rr_crossing_list[1].toggle()
            print("WAYSIDE: railway crossing status updated for section B")

    @pyqtSlot(list)
    def update_lights_A_status(self, lights_list: list[Light]) -> None:
        self.lights_list[0:4] = lights_list[0:4]

    @pyqtSlot(list)
    def update_lights_C_status(self, lights_list: list[Light]) -> None:
        self.lights_list[4:7] = lights_list[0:4]


def main():

    app = QApplication(sys.argv)

    # Instantiate the module and move it to its own thread
    track_controller_container = TrackControllerContainer()
    track_controller_thread = QThread()
    track_controller_container.moveToThread(track_controller_thread)

    # Instantiate the testbench to simulate inputs from other modules (use this to verify wayside operation)
    track_controller_test_container = TrackControllerTest.TrackControllerTestBenchContainer()
    track_controller_test_thread = QThread()
    track_controller_test_container.moveToThread(track_controller_test_thread)

    track_controller_A_ui = UI("A")
    track_controller_C_ui = UI("C")
    track_controller_test_ui = TrackControllerTest.TestUi()

    # start the threads
    track_controller_thread.start()
    track_controller_test_thread.start()

    track_controller_A_ui.show()
    track_controller_C_ui.show()
    track_controller_test_ui.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
