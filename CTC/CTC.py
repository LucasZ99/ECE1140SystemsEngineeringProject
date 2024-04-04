import threading

from CTC.CTCSchedule import CTCSchedule
from CTC.Train import Train
from CTC.Track import *
from SystemTime import SystemTime
from Track_Controller_SW.switching import Switch
from Track_Controller_SW import TrackControllerContainer
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class CTC(QObject):
    update_ui_signal = pyqtSignal()

    def __init__(self, system_time: SystemTime, track_controller_container_ref: TrackControllerContainer):
        super().__init__()
        self.system_time = system_time
        self.track_controller_ref = track_controller_container_ref

        self.scheduled_trains = CTCSchedule(system_time)
        self.dispatched_trains = CTCSchedule(system_time)

        self.running_trains: list[Train] = []

        self.authorities: dict[int, int] = {}
        for block in TRACK[GREEN_LINE]:
            self.authorities[block] = 0

        self.changed_authorities: list[int] = []
        self.suggested_speeds: dict[int, float] = {}
        for block in TRACK[GREEN_LINE]:
            self.suggested_speeds[block] = 0

        self.changed_speeds: list[int] = []

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

        self.system_time.update_time_signal.connect(self.update_ctc_queues)

    @pyqtSlot()
    def update_ctc_queues(self):
        for train_to_dispatch in self.scheduled_trains.dispatch_trains():
            self.dispatched_trains.schedule_train(train_to_dispatch)

        for train_to_run in self.dispatched_trains.dispatch_trains():
            self.running_trains.append(train_to_run)
            self.set_block_authority()
            self.set_block_suggested_speeds()

        self.update_track_controller()
        self.update_ui_signal.emit()

    def update_track_controller(self):
        for block in self.changed_authorities:
            self.track_controller_ref.set_authority(GREEN_LINE, block, self.authorities[block])
            self.changed_authorities.remove(block)

        for block in self.changed_speeds:
            self.track_controller_ref.command_speed(GREEN_LINE, block, self.suggested_speeds[block])
            self.changed_speeds.remove(block)

    def get_scheduled_trains(self) -> list[Train]:
        trains = []
        for train in self.scheduled_trains.train_list:
            trains.append(train)

        return trains

    def get_running_trains(self) -> list[Train]:
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
        print("authority function")
        for train in self.get_running_trains_sorted_by_priority():
            for block in train.get_next_authorities():
                print(f"Block {block[0]} authority set to : {block[1]}")
                self.authorities[block[0]] = block[1]
                self.changed_authorities.append(block[0])
            self.authorities[train.get_previous_block()] = 0
            self.changed_authorities.append(train.get_previous_block())

    def set_block_suggested_speeds(self):
        for train in self.get_running_trains_sorted_by_priority():
            for block in train.get_next_blocks():
                block_speed_limit = LENGTHS_SPEED_LIMITS[train.line_id][block][SPEED_LIMIT]
                adjusted_speed_limit = block_speed_limit * train.get_slowdown()

                self.suggested_speeds[block] = adjusted_speed_limit
                self.changed_speeds.append(block)
            self.suggested_speeds[train.get_previous_block()] = 0
            self.changed_speeds.append(train.get_previous_block())

    """
    Updates the position of each train based on the occupancies received from wayside
    """
    def update_train_position(self, train: Train):
        for train in self.running_trains:
            if self.blocks[train.current_block] is False and self.blocks[train.get_next_block()] is True:
                next_block_status = train.set_to_next_block()

                if next_block_status == 1:  # at station
                    self.dispatched_trains.schedule_train(train)
                elif next_block_status == 0:  # continue to next station
                    pass
                elif next_block_status == -1:  # yard is next
                    self.dispatched_trains.schedule_train(train)
                elif next_block_status == -2:  # remove from lists
                    self.running_trains.remove(train)
                    print("Train %d reached yard.", train.id)

    def update_switch_position(self, line_id: int, block_id: int, position: int):
        self.switches[block_id].current_pos = position

    def update_signal_status(self, line_id: int, block_id: int, signal_green: bool):
        self.lights[block_id] = signal_green

    def update_block_occupancy(self, line_id: int, block_id: int, occupied: bool):
        self.blocks[block_id] = occupied
        for train in [running_train for running_train in self.running_trains if abs(running_train.current_block) == block_id]:
            self.update_train_position(line_id, train)
            self.set_block_authority()
            self.set_block_suggested_speeds()

        self.update_track_controller()
        self.update_ui_signal.emit()

    def update_railroad_crossing_status(self, line_id: int, block_id: int, crossing_activated: bool):
        self.rr_crossings[block_id] = crossing_activated

    def update_ticket_sales(self, line_id: int, sales: int):
        pass

    def timer_handler(self):
        pass
