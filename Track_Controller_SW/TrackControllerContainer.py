from typing import List

from TrackController import TrackController
from switching import Switch
from Track_Model import Track_Model

class TrackControllerContainer(object):
    def __init__(self):
        # initialize track data
        self.occupancy_list = [False] * 151
        self.switch_list = \
            [
                Switch(13, 12, 1, 12),
                Switch(28, 29, 150, 29),
                Switch(77, 76, 101, 76),
                Switch(85, 86, 100, 86)
            ]
        self.railway_crossing_blocks_list = [19, 108]
        self.speed_list = [0.0] * 150
        self.zero_speed_flag_list = [False] * 150
        # self.track_model = track_model

        # Controller specific initialization
        # Section A: blocks 1-32, 147-150
        self.occupancy_list_A = self.occupancy_list[0:32] + self.occupancy_list[147:]

        self.trackControllerA = TrackController(occupancy_list=self.occupancy_list_A, section="A")

        # self.trackControllerB = TrackController()
        #
        #
        # self.trackControllerC = TrackController()

    # CTC Endpoints
    def command_speed(self, line_id: int, block_id: int, speed: float) -> None:
        # green line
        if line_id == 0:
            if self.zero_speed_flag_list[block_id] is False:
                self.speed_list[block_id] = speed
            else:
                self.speed_list[block_id] = 0
            # self.track_model.updateSpeed(self.speed_list)


    def set_block_maintenance(self, line_id: int, block_index: int, open: bool) -> None:
        pass

    def set_authority(self, line_id: int, block_id: int, authority: int) -> None:
        # call self.track_model.update_authority endpoint directly
        pass

    # Track Model Endpoint
    def update_occupancy(self, block_occupancy_list: list) -> None:
        self.occupancy_list = block_occupancy_list
        # CTC.update_block_occupancy(0, self.occupancy_list)
        self.occupancy_list_A = self.occupancy_list[0:32] + self.occupancy_list[147:]
        zero_speed_flag_list_A = self.trackControllerA.update_occupancy(self.occupancy_list_A)
        self.zero_speed_flag_list[0:32] = zero_speed_flag_list_A[0:32]
        self.zero_speed_flag_list[147:] = zero_speed_flag_list_A[32:]

        # self.track_model.updateSpeed(self.speed_list)

    def show_ui(self, section : str):
        if section == "A":
            self.trackControllerA.show_ui()


def main():
    trackControllerContainer = TrackControllerContainer()
    trackControllerContainer.update_occupancy([True]*151)
    trackControllerContainer.show_ui("A")

if __name__ == "__main__":
    main()

