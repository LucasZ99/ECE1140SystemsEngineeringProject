from TrackController import TrackController
from switching import Switch


class TrackControllerContainer(object):
    def __init__(self):
        # initialize track data
        self.occupancy_list = [False] * 150
        self.switch_list = \
            [
                Switch(13, 12, 1, 12),
                Switch(28, 29, 150, 29),
                Switch(77, 76, 101, 76),
                Switch(85, 86, 100, 85)
            ]
        self.railway_crossing_blocks_list = [19, 108]
        self.speed_list = [0.0] * 150
        self.zero_speed_flag_list = [False] * 150

        # Controller specific initialization
        # Section A: blocks 1-32, 147-150
        self.occupancy_list_A = self.occupancy_list[0:32] + self.occupancy_list[147:150]

        self.trackControllerA = TrackController(self.occupancy_list_A)

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
            # TrackModel.updateSpeed(speed_list)


    def set_block_maintenance(self, line_id: int, block_index: int, open: bool) -> None:
        pass

    def set_authority(self, line_id: int, block_id: int, authority: int) -> None:
        # call trackmodel.update_authority endpoint directly
        pass

    # Track Model Endpoint
    def update_occupancy(self, block_occupancy_list: list[bool]) -> None:
        self.occupancy_list = block_occupancy_list
        self.occupancy_list_A = self.occupancy_list[0:32] + self.occupancy_list[147:150]
        zero_speed_flag_list_A = self.trackControllerA.update_occupancy(self.occupancy_list_A)
        self.zero_speed_flag_list[0:32] = zero_speed_flag_list_A[0:32]
        self.zero_speed_flag_list[147:] = zero_speed_flag_list_A[32:]
