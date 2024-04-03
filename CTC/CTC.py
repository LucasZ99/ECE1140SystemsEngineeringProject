from CTC.CTCSchedule import CTCSchedule
from CTC.Train import Train
from CTC.Track import *
from SystemTime import SystemTime
from Track_Controller_SW.switching import Switch
from Track_Controller_SW import TrackControllerContainer
from PyQt6.QtCore import QObject


class CTC(QObject):
    def __init__(self, system_time: SystemTime, track_controller_container_ref: TrackControllerContainer):
        super().__init__()
        self.system_time = system_time
        self.track_controller_ref = track_controller_container_ref

        self.scheduled_trains = CTCSchedule(system_time)
        self.dispatched_trains = CTCSchedule(system_time)

        self.running_trains: list[Train] = []

        self.authorities: dict[int, int] = {}
        self.set_speed_limits: dict[int, float] = {}

        # Initialize all blocks to false
        self.blocks: dict[int, bool] = {}
        for block in TRACK[GREEN_LINE]:
            self.blocks[block] = False

        self.switches: dict[int, Switch] = {}

        for switch in track_controller_container_ref.switch_list:
            self.switches[switch.block] = switch

        self.lights: dict[int:bool] = {}
        for light in track_controller_container_ref.lights_list:
            self.lights[light.block] = light.val

        self.rr_crossings: dict[int, bool] = {}
        for crossing in CROSSINGS[GREEN_LINE]:
            self.rr_crossings[crossing] = False

    def get_scheduled_trains(self) -> list[Train]:
        trains = []
        for train in self.scheduled_trains.train_list:
            trains.append(train)

        return trains

    def get_running_train(self) -> list[Train]:
        trains = []
        for train in self.running_trains:
            trains.append(train)
        for train in self.dispatched_trains.train_list:
            trains.append(train)

        trains.sort(key=lambda train: train.get_destination().arrival_time)
        return trains

    def set_block_to_maintenance_mode(self, line_id: int, block_id: int):
        pass

    def set_switch_position(self, line_id: int, block_id: int, switch: Switch):
        pass

    def get_running_trains_sorted_by_priority(self):
        sort_by_next_stop_arrival_time = sorted(self.running_trains, key=lambda train: train.arrival_time)
        sort_by_destination_arrival_time = sorted(sort_by_next_stop_arrival_time,
                                                  key=lambda train: train.get_destination().arrival_time)
        return sort_by_destination_arrival_time

    def set_block_authority(self):
        for train in self.get_running_trains_sorted_by_priority():
            for block in train.get_next_authorities():
                self.authorities[block[0]] = block[1]
                self.authorities[train.get_previous_block()] = 0

    def set_block_suggested_speeds(self):
        for train in self.get_running_trains_sorted_by_priority():
            for block in train.get_next_blocks():
                block_speed_limit = LENGTHS_SPEED_LIMITS[train.line_id][block][SPEED_LIMIT]
                adjusted_speed_limit = block_speed_limit * train.get_slowdown()

                self.speed_limits[block] = adjusted_speed_limit
                self.speed_limits[train.get_previous_block()] = 0

    """
    Updates the position of each train based on the occupancies received from wayside
    """
    def update_train_positions(self):
        for train in self.running_trains:
            if self.blocks[train.current_block] == False and self.blocks[train.get_next_block()] == True:
                next_block_status = train.set_to_next_block()

                if next_block_status == 1:  # at station
                    self.dispatched_trains.schedule_train(train)
                elif next_block_status == 0:  # continue to next station
                    pass
                elif next_block_status == -1:  # yard is next
                    self.dispatched_trains.schedule_train(train)
                elif next_block_status == -2:  # remove from lists
                    self.running_trains.remove(train)

    def update_switch_position(self, line_id: int, block_id: int, position: int):
        self.switches[block_id].current_pos = position

    def update_signal_status(self, line_id: int, block_id: int, signal_green: bool):
        self.lights[block_id] = signal_green

    def update_block_occupancy(self, line_id: int, block_id: int, occupied: bool):
        self.blocks[block_id] = occupied

    def update_railroad_crossing_status(self, line_id: int, block_id: int, crossing_activated: bool):
        self.rr_crossings[block_id] = crossing_activated

    def update_ticket_sales(self, line_id: int, sales: int):
        pass

    def timer_handler(self):
        pass
