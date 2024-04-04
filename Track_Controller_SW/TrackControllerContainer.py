from PyQt6.QtCore import pyqtSlot, QObject, pyqtSignal

from Track_Controller_HW import TrackControllerHardware
from Track_Controller_SW import TrackController, Switch, Light
from Track_Model.Track_Model_Container import TrackModelContainer


class TrackControllerContainer(QObject):

    # Signals
    switch_toggled_signal = pyqtSignal(int)
    lights_updated_signal = pyqtSignal(int)
    rr_crossing_toggled_signal = pyqtSignal(int)
    occupancy_updated_signal = pyqtSignal(list)

    def __init__(self, track_model: TrackModelContainer):
        # initialize track data
        super().__init__()
        self.track_model = track_model

        self.occupancy_list = [False] * 150

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

        self.railway_crossing_blocks_list = [19, 108]
        self.railway_crossing_vals_list = [False, False]
        self.speed_list = [0.0] * 150
        self.zero_speed_flag_list = [False] * 150
        self.authority_list = [0] * 150

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

        # Connect external signals:
        self.track_model.new_block_occupancy_signal.connect(self.update_occupancy)

    # CTC Endpoints
    def command_speed(self, line_id: int, block_id: int, speed: float) -> None:
        # green line
        print(f"track controller speed received: {block_id}: {speed}")
        if line_id == 0:
            if self.zero_speed_flag_list[block_id] is False:
                self.speed_list[block_id] = speed
            else:
                self.speed_list[block_id] = 0
            self.track_model.update_speed(self.speed_list)
        print('track controller passed')

    def update_switch(self, line_id: int, block_id: int, switch_status: Switch) -> None:
        pass

    def set_block_maintenance(self, line_id: int, block_index: int, open: bool) -> None:
        pass
        # call self.track_model.open/close_block(block_index)

    def set_authority(self, line_id: int, block_id: int, authority: int) -> None:
        print(f"track controller authority received: {block_id}: {authority}")
        if line_id == 0:
            self.authority_list[block_id-1] = authority
            self.track_model.update_authority(self.authority_list)
        print("Authority sent to track model")


    # Track Model Endpoint
    @pyqtSlot(list)
    def update_occupancy(self, block_occupancy_list: list) -> None:
        print("track controller got the occupancy from track model")
        # update occupancy to ctc:
        self.occupancy_updated_signal.emit(block_occupancy_list)
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
        #print("zero speed flag list B: ", self.zero_speed_flag_list_B)
        #print("zero speed flag list B length: ", len(self.zero_speed_flag_list_B))
        #self.zero_speed_flag_list[28:78] = zero_speed_flag_list_B[0:50]
        #self.zero_speed_flag_list[101:len(self.occupancy_list_B)] = zero_speed_flag_list_B[51:len(self.occupancy_list_B)]
        # self.zero_speed_flag_list[77:(77 + len(self.occupancy_list_C))] = zero_speed_flag_list_C[
        #                                                                   0:len(self.occupancy_list_C)]

    @pyqtSlot(int)
    def update_track_switch(self, switch_block: int) -> None:
        print(f"Updating Track Model switch at block: {switch_block}")
        self.switch_toggled_signal.emit(switch_block)
        self.track_model.toggle_switch(switch_block)

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
            if lights_list[i].val != self.lights_list[i+4].val:
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
