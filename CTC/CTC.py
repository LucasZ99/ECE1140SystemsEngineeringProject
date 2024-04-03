from CTC.CTCSchedule import CTCSchedule
from CTC.Train import Train
from CTC.Block import Block
from CTC.Track import *
from SystemTime import SystemTime
from Track_Controller_SW.switching import Switch
from Track_Controller_SW import TrackController
from PyQt6.QtCore import QObject


class CTC(QObject):
    def __init__(self, system_time: SystemTime, track_controller_ref: TrackController):
        super().__init__()
        self.system_time = system_time
        self.track_controller_ref = track_controller_ref

        self.scheduled_trains = CTCSchedule(system_time)
        self.dispatched_trains = CTCSchedule(system_time)

        self.running_trains: list[Train] = []

        # Initialize all blocks to false
        self.blocks: dict[int, bool] = {}
        for block in TRACK[GREEN_LINE]:
            self.blocks[block] = False

        self.switches: dict[int, Switch] = {}

        for switch in track_controller_ref.switches_list:
            self.switches[switch.block] = switch

        self.lights: dict[int:bool] = {}
        for light in track_controller_ref.lights_list:
            self.lights[light.block] = light.val

        self.rr_crossings: dict[int, bool] = {}
        for crossing in CROSSINGS:
            self.rr_crossings[crossing] = CROSSINGS[crossing]

    def set_block_to_maintenance_mode(self, line_id: int, block_id: int):
        pass

    def set_switch_position(self, line_id: int, block_id: int, switch: Switch):
        pass

    def set_block_authority(self, train: Train):
        pass

    def set_block_suggested_speeds(self, train: Train):
        pass

    def update_switch_position(self, line_id: int, block_id: int, switch: Switch):
        pass

    def update_signal_status(self, line_id: int, block_id: int, signal_green: bool):
        pass

    def update_block_occupancy(self, line_id: int, block_id: int, occupied: bool):
        pass

    def update_railroad_crossing_status(self, line_id: int, block_id: int, crossing_activated: bool):
        pass

    def update_ticket_sales(self, line_id: int, sales: int):
        pass

    def timer_handler(self):
        pass
