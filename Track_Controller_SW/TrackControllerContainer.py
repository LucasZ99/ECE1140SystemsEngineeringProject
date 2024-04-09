from PyQt6.QtCore import pyqtSlot, QObject, pyqtSignal

from Track_Controller_HW import TrackControllerHardware
from Track_Controller_SW import TrackController
from Common import Switch, Light, TrackSignal, RRCrossing
from Track_Model.Track_Model_Container import TrackModelContainer


class TrackControllerContainer(QObject):
    # Signals
    # Downstream
    update_track_model_from_wayside = pyqtSignal(list, list, list, list, list)
    # Upstream
    update_ctc_from_wayside = pyqtSignal(dict[int, bool], list, list, list)

    # switch_toggled_signal = pyqtSignal(int)
    # lights_updated_signal = pyqtSignal(int)
    # rr_crossing_toggled_signal = pyqtSignal(int)
    # occupancy_updated_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.occupancy_dict = {}
        self.zero_speed_flag_dict = {}
        self.safe_toggle_blocks = {}
        # Add values from 1 to 57
        for i in range(1, 58):
            self.occupancy_dict[i] = False
            self.zero_speed_flag_dict[i] = False
            self.safe_toggle_blocks[i] = True
        for i in range(62, 151):
            self.occupancy_dict[i] = False
            self.zero_speed_flag_dict[i] = False
            self.safe_toggle_blocks[i] = True

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
        # Section A: blocks 1-32
        # Switches at block 13 and 28
        self.occupancy_list_A = self.occupancy_list[0:32]
        # Section B: blocks: 25-80 , 101-150
        # change this to [28:78] to be able to observe the switch positions at sections G(b28) and N(b77)
        # remember python slicing is [inclusive:exclusive] which is why it's [28:78]
        # also change the other boundary to [101:]
        self.occupancy_list_B = self.occupancy_list[28:78] + self.occupancy_list[101:]
        # Section C: blocks 77:104
        # Switches at block 77(index 76) and 85
        self.occupancy_list_C = self.occupancy_list[76:105]

        self.trackControllerA = TrackController(occupancy_list=self.occupancy_list_A, section="A")

        self.trackControllerB = TrackControllerHardware(occupancy_list=self.occupancy_list_B, section="B")

        self.trackControllerC = TrackController(occupancy_list=self.occupancy_list_C, section="C")

        # Connect Internal Signals:
        self.trackControllerA.switch_changed_index_signal.connect(self.update_track_switch)
        self.trackControllerA.rr_crossing_signal.connect(self.update_rr_crossing_status_A)
        self.trackControllerA.lights_list_A_changed_signal.connect(self.update_lights_A_status)
        self.trackControllerC.lights_list_C_changed_signal.connect(self.update_lights_C_status)
        self.trackControllerB.rr_crossing_signal.connect(self.update_rr_crossing_status_B)
        self.trackControllerC.switch_changed_index_signal.connect(self.update_track_switch)

    # CTC Endpoint
    @pyqtSlot(list, bool, list, list)
    def update_wayside_from_ctc(self,
                                authority_speed_update: list[TrackSignal],
                                maintenance_mode_override_flag: bool,
                                blocks_to_close_open: list[tuple[int, bool]],
                                updated_switches: list[Switch]):

        self.check_safe_speed(authority_speed_update)
        safe_toggle_blocks = []
        if maintenance_mode_override_flag:
            safe_toggle_blocks = self.check_safe_toggle(blocks_to_close_open)

        # call downstream endpoint after processing of CTC data
        self.update_track_model_from_wayside.emit(
            [signal.to_tuple() for signal in authority_speed_update],
            [switch.to_tuple() for switch in self.switch_list],
            [light.to_tuple() for light in self.lights_list],
            [crossing.to_tuple() for crossing in self.rr_crossing_list],
            safe_toggle_blocks
        )

    # Track Model Endpoint
    @pyqtSlot(dict[int, bool])
    def update_wayside_from_track_model(self, block_occupancy_update: dict[int, bool]):
        pass

    def check_safe_speed(self, track_signal: list[TrackSignal]):
        for signal in track_signal:
            if self.zero_speed_flag_dict[signal.block_id]:
                signal.zero_speed()

    def check_safe_toggle(self, blocks_to_close_open: list[tuple[int, bool]]):
        safe_toggle_blocks = []
        for item in blocks_to_close_open:
            if item[1]:
                safe_toggle_blocks.append(item[0])
            elif not item[1] and self.safe_toggle_blocks[item[0]]:
                safe_toggle_blocks.append(item[0])
        return safe_toggle_blocks

    def update_switch(self, line_id: int, block_id: int, switch_status: Switch) -> None:
        pass

    def set_block_maintenance(self, line_id: int, block_index: int, open: bool) -> None:
        pass
        # call self.track_model.open/close_block(block_index)

    @pyqtSlot(list)
    def update_occupancy(self, block_occupancy_list: dict[int, bool]):
        print("track controller got the occupancy from track model")
        # update occupancy to ctc:
        print("occupancy updated signal sent to ctc")

        # update occupancy lists with new data
        self.occupancy_list = block_occupancy_list
        self.occupancy_list_A = self.occupancy_list[0:32]
        self.occupancy_list_B = self.occupancy_list[28:78] + self.occupancy_list[101:]
        self.occupancy_list_C = self.occupancy_list[77:105]

        # call the update occupancy functions to trigger plc logic and ui updates
        zero_speed_flag_list_A = self.trackControllerA.update_occupancy(self.occupancy_list_A)
        zero_speed_flag_list_B = self.trackControllerB.update_occupancy(self.occupancy_list_B)
        zero_speed_flag_list_C = self.trackControllerC.update_occupancy(self.occupancy_list_C)
        # self.zero_speed_flag_list[0:len(self.occupancy_list_A)] = zero_speed_flag_list_A[0:len(self.occupancy_list_A)]
        print("zero speed flag list length: ", len(self.zero_speed_flag_list))
        # print("zero speed flag list B: ", self.zero_speed_flag_list_B)
        # print("zero speed flag list B length: ", len(self.zero_speed_flag_list_B))
        # self.zero_speed_flag_list[28:78] = zero_speed_flag_list_B[0:50]
        # self.zero_speed_flag_list[101:len(self.occupancy_list_B)] = zero_speed_flag_list_B[51:len(self.occupancy_list_B)]
        # self.zero_speed_flag_list[77:(77 + len(self.occupancy_list_C))] = zero_speed_flag_list_C[
        #                                                                   0:len(self.occupancy_list_C)]

    @pyqtSlot(int)
    def update_track_switch(self, switch_block: int) -> None:
        print(f"Updating Track Model switch at block: {switch_block}")

    @pyqtSlot(bool)
    def update_rr_crossing_status_A(self, rr_crossing_status: bool) -> None:
        # if the previous status does not equal updated status, send the signal
        # and update the track model
        if self.railway_crossing_vals_list[0] != rr_crossing_status:
            self.railway_crossing_vals_list[0] = rr_crossing_status
            # emit for CTC
            self.rr_crossing_toggled_signal.emit(self.railway_crossing_blocks_list[0])
            # call track model endpoint
            self.track_model.toggle_crossing(self.railway_crossing_blocks_list[0])

    @pyqtSlot(bool)
    def update_rr_crossing_status_B(self, rr_crossing_status: bool) -> None:
        print("railway crossing status updated for section B")
        if self.railway_crossing_vals_list[1] != rr_crossing_status:
            self.railway_crossing_vals_list[1] = rr_crossing_status
            # emit for CTC
            self.rr_crossing_toggled_signal.emit(self.railway_crossing_blocks_list[1])
            # call track model endpoint
            self.track_model.toggle_crossing(self.railway_crossing_blocks_list[1])

    @pyqtSlot(list)
    def update_lights_A_status(self, lights_list: list[Light]) -> None:
        # emit new list to ctc
        # update changed signals to track model
        for i in range(len(lights_list)):
            if lights_list[i].val != self.lights_list[i].val:
                self.track_model.toggle_signal(lights_list[i].block)
                self.lights_updated_signal.emit(lights_list[i].block)

        self.lights_list[0:4] = lights_list[0:4]

    @pyqtSlot(list)
    def update_lights_C_status(self, lights_list: list[Light]) -> None:
        # emit new list to ctc
        # update changed signals to track model
        for i in range(len(lights_list)):
            if lights_list[i].val != self.lights_list[i + 4].val:
                self.track_model.toggle_signal(lights_list[i].block)
                self.lights_updated_signal.emit(lights_list[i].block)

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
    # trackControllerContainer.update_occupancy([True] * 151)
    trackControllerContainer.show_ui("A")


if __name__ == "__main__":
    main()
