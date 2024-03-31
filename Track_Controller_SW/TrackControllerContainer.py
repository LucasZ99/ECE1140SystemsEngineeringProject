from PyQt6.QtCore import pyqtSlot, QObject

# from Track_Controller_HW.TrackControllerHW import TrackControllerHardware
from Track_Controller_SW import TrackController, Switch


# from Track_Model import Track_Model_New

class TrackControllerContainer(QObject):
    def __init__(self):
        # initialize track data
        super().__init__()
        self.occupancy_list = [False] * 151
        self.switch_list = \
            [
                Switch(13, 12, 1, 12),
                Switch(28, 29, 150, 29),
                Switch(77, 76, 101, 76),
                Switch(85, 86, 100, 86)
            ]
        self.railway_crossing_blocks_list = [19, 108]
        self.speed_list = [0.0] * 151
        self.zero_speed_flag_list = [False] * 151
        # self.track_model = track_model
        self.authority_list = [0] * 151

        # Controller specific initialization
        # Section A: blocks 1-32, 147-150
        self.occupancy_list_A = self.occupancy_list[0:32]
        # Section B: blocks: 25-80 , 101-150
        self.occupancy_list_B = self.occupancy_list[24:80] + self.occupancy_list[100:]
        # Section C: blocks 73:104
        self.occupancy_list_C = self.occupancy_list[76:104]

        self.trackControllerA = TrackController(occupancy_list=self.occupancy_list_A, section="A")

        # self.trackControllerB = TrackControllerHardware(occupancy_list=self.occupancy_list_B, section="B")

        self.trackControllerC = TrackController(occupancy_list=self.occupancy_list_C, section="C")

        # Connect Signals:

        self.trackControllerA.switch_changed_index_signal.connect(self.update_track_switch)

    # CTC Endpoints
    def command_speed(self, line_id: int, block_id: int, speed: float) -> None:
        # green line
        if line_id == 0:
            if self.zero_speed_flag_list[block_id] is False:
                self.speed_list[block_id] = speed
            else:
                self.speed_list[block_id] = 0
            # self.track_model.update_speed(self.speed_list)

    def update_switch(self, line_id: int, block_id: int, switch_status: Switch) -> None:
        pass

    def set_block_maintenance(self, line_id: int, block_index: int, open: bool) -> None:
        pass
        # call self.track_model.open/close_block(block_index)

    def set_authority(self, line_id: int, block_id: int, authority: int) -> None:
        if line_id == 0:
            self.authority_list[block_id] = authority
            # self.track_model.update_authority(self.authority_list)
        pass

    # Track Model Endpoint
    def update_occupancy(self, block_occupancy_list: list) -> None:
        self.occupancy_list = block_occupancy_list
        # CTC.update_block_occupancy(0, self.occupancy_list)
        self.occupancy_list_A = self.occupancy_list[0:33]
        zero_speed_flag_list_A = self.trackControllerA.update_occupancy(self.occupancy_list_A)
        self.zero_speed_flag_list[0:33] = zero_speed_flag_list_A[0:33]

    @pyqtSlot(int)
    def update_track_switch(self, switch_block: int) -> None:
        print(f"Updating Track Model switch at block: {switch_block}")
        # self.track_model.toggle_switch(switch_block)

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
        # if section == "B":
        #     # self.trackControllerB.show_testbench_ui()
        if section == "C":
            self.trackControllerC.show_testbench_ui()


# def main():
#     trackControllerContainer = TrackControllerContainer()
#     trackControllerContainer.update_occupancy([True] * 151)
#     trackControllerContainer.show_ui("A")
#
#
# if __name__ == "__main__":
#     main()
