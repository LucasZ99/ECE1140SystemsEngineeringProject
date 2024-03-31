import os
import sys

from Track_Model import TrackModel


class TrackModelContainer(object):
    def __init__(self,
                 # track_model: Track_Model_New
                 ):
        self.track_model = TrackModel()

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
        self.occupancy_list_A = self.occupancy_list[0:32] + self.occupancy_list[147:]
        zero_speed_flag_list_A = self.trackControllerA.update_occupancy(self.occupancy_list_A)
        self.zero_speed_flag_list[0:32] = zero_speed_flag_list_A[0:32]
        self.zero_speed_flag_list[147:] = zero_speed_flag_list_A[32:]

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


# def main():
#     trackControllerContainer = TrackControllerContainer()
#     trackControllerContainer.update_occupancy([True] * 151)
#     trackControllerContainer.show_ui("A")
#
#
# if __name__ == "__main__":
#     main()
