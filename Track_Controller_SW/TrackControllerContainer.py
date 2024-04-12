import itertools

from PyQt6.QtCore import pyqtSlot, QObject, pyqtSignal

from Track_Controller_HW import TrackControllerHardware
from Track_Controller_SW import TrackController
from Common import Switch, Light, TrackSignal, RRCrossing


class TrackControllerContainer(QObject):
    # Signals
    # Downstream
    update_track_model_from_wayside = pyqtSignal(list, list, list, list, list)
    # Upstream
    update_ctc_from_wayside = pyqtSignal(dict, list, list, list)

    def __init__(self):
        super().__init__()

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
        # self.trackControllerB = TrackControllerHardware(occupancy_dict=self.occupancy_dict_B, section="B")
        self.trackControllerC = TrackController(occupancy_dict=self.occupancy_dict_C, section="C")

        # # Connect Internal Signals:
        self.trackControllerA.switch_changed_index_signal.connect(self.update_track_switch)
        self.trackControllerA.rr_crossing_signal.connect(self.update_rr_crossing_status_A)
        self.trackControllerA.lights_list_A_changed_signal.connect(self.update_lights_A_status)

        # self.trackControllerB.rr_crossing_signal.connect(self.update_rr_crossing_status_B)

        self.trackControllerC.lights_list_C_changed_signal.connect(self.update_lights_C_status)
        self.trackControllerC.switch_changed_index_signal.connect(self.update_track_switch)

    # CTC Endpoint
    @pyqtSlot(list, bool, list, list)
    def update_wayside_from_ctc(self,
                                authority_speed_update: list[TrackSignal],
                                maintenance_mode_override_flag: bool,
                                blocks_to_close_open: list[tuple[int, bool]],
                                updated_switches: list[Switch]):

        # print(f"authority speed update received in wayside: {authority_speed_update[0]}")
        # self.check_safe_speed(authority_speed_update)
        #
        # safe_toggle_blocks = []
        # if maintenance_mode_override_flag:
        #     safe_toggle_blocks = self.check_safe_toggle_block(blocks_to_close_open)
        #     self.toggle_switch_if_safe(updated_switches)
        #
        # # call downstream endpoint after processing of CTC data
        self.update_track_model_from_wayside.emit(
            [track_signal.to_tuple() for track_signal in authority_speed_update],
            [switch.to_tuple() for switch in self.switch_list],
            [light.to_tuple() for light in self.lights_list],
            [crossing.to_tuple() for crossing in self.rr_crossing_list],
            []
        )

    # Track Model Endpoint
    @pyqtSlot(dict)
    def update_wayside_from_track_model(self, block_occupancy_update: dict[int, bool]):
        print(f"block occupancy update from wayside received, block 62 status: {block_occupancy_update[62]}")
        # self.update_occupancy(block_occupancy_update)
        self.update_ctc_from_wayside.emit(
            block_occupancy_update,
            self.switch_list,
            self.lights_list,
            self.rr_crossing_list
        )

    def check_safe_speed(self, track_signal: list[TrackSignal]):
        for signal in track_signal:
            if self.zero_speed_flag_dict[signal.block_id]:
                signal.zero_speed()

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
        for index in range(len(self.safe_toggle_switch)):
            # if it's safe to toggle that switch, just reassign the switch value to the new one, even if it's the same
            if self.safe_toggle_switch[index]:
                self.switch_list[index] = switches_to_toggle[index]



    def update_switch(self, line_id: int, block_id: int, switch_status: Switch) -> None:
        pass

    def set_block_maintenance(self, line_id: int, block_index: int, open: bool) -> None:
        pass
        # call self.track_model.open/close_block(block_index)

    @pyqtSlot(list)
    def update_occupancy(self, block_occupancy_dict: dict[int, bool]):
        print("TrackControllerContainer.update_occupancy called")

        # update occupancy dicts with new data
        self.occupancy_dict.update(block_occupancy_dict)
        self.occupancy_dict_A.update(dict(itertools.islice(self.occupancy_dict.items(), 32)))
        self.occupancy_dict_B.update(dict(itertools.islice(self.occupancy_dict.items(), 28, 72)))
        self.occupancy_dict_B.update(dict(itertools.islice(self.occupancy_dict.items(), 96, 146)))
        self.occupancy_dict_C.update(dict(itertools.islice(self.occupancy_dict.items(), 72, 100)))

        # call the update occupancy functions to trigger plc logic and ui updates
        update_occupancy_A_result = self.trackControllerA.update_occupancy(self.occupancy_dict_A)
        zero_speed_flag_dict_A = update_occupancy_A_result[0]
        for key in zero_speed_flag_dict_A.keys():
            self.zero_speed_flag_dict[key] = zero_speed_flag_dict_A[key]

        unsafe_close_blocks_A = update_occupancy_A_result[1]
        for block in unsafe_close_blocks_A:
            self.safe_close_blocks[block + 1] = False

        unsafe_toggle_switch = update_occupancy_A_result[2]
        for switch_index in unsafe_toggle_switch:
            self.safe_toggle_switch[switch_index] = False

        update_occupancy_C_result = self.trackControllerC.update_occupancy(self.occupancy_dict_C)
        zero_speed_flag_dict_C = update_occupancy_C_result[0]
        for key in zero_speed_flag_dict_C.keys():
            self.zero_speed_flag_dict[key] = zero_speed_flag_dict_C[key]

        unsafe_close_blocks_C = update_occupancy_C_result[1]
        for block in unsafe_close_blocks_C:
            self.safe_close_blocks[block + 1] = False

        unsafe_toggle_switch = update_occupancy_C_result[2]
        for switch_index in unsafe_toggle_switch:
            self.safe_toggle_switch[switch_index+2] = False

        # update_occupancy_B_result = self.trackControllerB.update_occupancy(self.occupancy_dict_B)
        update_occupancy_C_result = self.trackControllerC.update_occupancy(self.occupancy_dict_C)
        # self.zero_speed_flag_list[0:len(self.occupancy_list_A)] = zero_speed_flag_list_A[0:len(self.occupancy_list_A)]
        print("zero speed flag list length: ", len(self.zero_speed_flag_list))
        # print("zero speed flag list B: ", self.zero_speed_flag_list_B)
        # print("zero speed flag list B length: ", len(self.zero_speed_flag_list_B))
        # self.zero_speed_flag_list[28:78] = zero_speed_flag_list_B[0:50]
        # self.zero_speed_flag_list[101:len(self.occupancy_list_B)] = zero_speed_flag_list_B[51:len(self.occupancy_list_B)]
        # self.zero_speed_flag_list[77:(77 + len(self.occupancy_list_C))] = zero_speed_flag_list_C[
        #                                                                   0:len(self.occupancy_list_C)]

        print("TrackControllerContainer.update_occupancy finished")


    @pyqtSlot(int)
    def update_track_switch(self, switch_block: int) -> None:
        print(f"Updating switch at block: {switch_block}")
        for switch in self.switch_list:
            if switch.block == switch_block:
                switch.toggle()

    @pyqtSlot(bool)
    def update_rr_crossing_status_A(self, rr_crossing_status: bool) -> None:
        # if the previous status does not equal updated status, toggle the signal
        if self.rr_crossing_list[0].val != rr_crossing_status:
            self.rr_crossing_list[0].toggle()
            print("railway crossing status updated for section A")

    @pyqtSlot(bool)
    def update_rr_crossing_status_B(self, rr_crossing_status: bool) -> None:
        if self.rr_crossing_list[1].val != rr_crossing_status:
            self.rr_crossing_list[1].toggle()
            print("railway crossing status updated for section B")

    @pyqtSlot(list)
    def update_lights_A_status(self, lights_list: list[Light]) -> None:
        self.lights_list[0:4] = lights_list[0:4]

    @pyqtSlot(list)
    def update_lights_C_status(self, lights_list: list[Light]) -> None:
        self.lights_list[4:7] = lights_list[0:4]

    def show_ui(self, section: str):
        if section == "A":
            print("Section A UI called")
            self.trackControllerA.show_ui()
        if section == "C":
            print("Section C UI called")
            self.trackControllerC.show_ui()

    def show_testbench_ui(self, section: str):
        if section == "A":
            self.trackControllerA.show_testbench_ui()
        if section == "B":
            self.trackControllerB.show_testbench_ui()
        if section == "C":
            self.trackControllerC.show_testbench_ui()


def main():
    trackControllerContainer = TrackControllerContainer()
    trackControllerContainer.show_ui("C")

if __name__ == "__main__":
    main()
