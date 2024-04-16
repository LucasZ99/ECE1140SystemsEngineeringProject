from CTC.CTCConstants import *
from CTC.CTCSchedule import CTCSchedule
from CTC.Train import Train
from Common import TrackSignal
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from Common.GreenLine import *

import time as python_time

from Common.Lines import stop_name


class CTC(QObject):
    update_ui_signal = pyqtSignal()
    update_wayside_from_ctc_signal = pyqtSignal(list, bool, list, list)
    update_ui_running_trains_table_signal = pyqtSignal()
    update_ui_block_table = pyqtSignal()

    ui_update_rr_crossings = pyqtSignal()
    ui_update_signals = pyqtSignal()
    ui_update_block_occupancies = pyqtSignal()
    ui_update_switches = pyqtSignal()
    ui_update_schedule = pyqtSignal()
    ui_update_ticket_sales = pyqtSignal()
    ui_update_throughput = pyqtSignal()

    def __init__(self):
        self.updated_switches: list[Switch] = []
        self.blocks_to_close_open: list[tuple[int, bool]] = []
        self.maintenance_mode_override_flag: bool = False
        self.authority_speed_update: list[TrackSignal] = []
        init_start_time = python_time.time()
        print("CTC Init started t={0}".format(init_start_time))

        super().__init__()

        self.mode = AUTOMATIC_MODE

        self.wayside_update_list: list[tuple[int, int, float]] = []

        self.scheduled_trains = CTCSchedule()
        self.dispatched_trains = CTCSchedule()

        self.running_trains: list[Train] = []
        self.yard_queue: list[Train] = []

        # Holds the current Train in the yard.
        self.yard: Train | None = None

        self.authorities: dict[int, int] = {}
        for block in GREEN_LINE[BLOCKS]:
            self.authorities[block] = 0

        self.changed_authorities: list[int] = []
        self.suggested_speeds: dict[int, float] = {}
        for block in GREEN_LINE[BLOCKS]:
            self.suggested_speeds[block] = 0

        self.changed_speeds: list[int] = []

        # Initialize all blocks to false
        self.blocks: dict[int, bool] = {}
        for block in GREEN_LINE[BLOCKS]:
            self.blocks[block] = False

        self.switches: dict[int, Switch] = {}
        for switch in GREEN_LINE[SWITCHES]:
            self.switches[switch.block] = switch

        self.lights: dict[int:bool] = {}
        for light in GREEN_LINE[LIGHTS]:
            self.lights[light.block] = light.val

        self.rr_crossings: dict[int, bool] = {}
        for crossing in GREEN_LINE[CROSSINGS]:
            self.rr_crossings[crossing] = False

        init_end_time = python_time.time()
        print("CTC Init finished. t={0}".format(init_end_time))
        print("CTC Init time elapsed t={0}".format(init_end_time - init_start_time))

    def send_initial_message(self):
        print("CTC: send initial message")
        self.update_wayside_from_ctc_signal.emit([TrackSignal(GREEN_LINE_YARD_SPAWN, 0, 0)], False, [], [])

    @pyqtSlot()
    def update_ctc_queues(self) -> bool:
        # print("CTC: Updating Queues")
        update = False

        # add dispatched trains to yard queue
        for train_to_dispatch in self.scheduled_trains.dispatch_trains():
            # self.dispatched_trains.schedule_train(train_to_dispatch)
            self.yard_queue.append(train_to_dispatch)
            print(f"CTC: Train {train_to_dispatch.id} added to Yard Queue")
            update = True

        # add moving trains back to running queue
        for train_to_run in self.dispatched_trains.dispatch_trains():
            self.running_trains.append(train_to_run)
            update = True

        # Move next train into yard when yard is open
        if self.yard is None:
            if len(self.yard_queue) > 0:
                self.yard = self.yard_queue.pop(0)
                print(f"CTC: Train {self.yard.id} set to yard")
                update = True

        if update:
            self.update_ui_running_trains_table_signal.emit()
            return True
        else:
            return False

    def update_track_controller(self):
        self.wayside_update_list.clear()

        # take union of authorities and speeds to update
        blocks_to_update = sorted(list(set(self.changed_authorities) | set(self.changed_speeds)))

        for block in blocks_to_update:
            self.wayside_update_list.append((block, self.authorities[block], self.suggested_speeds[block]))

        self.changed_authorities.clear()
        self.changed_speeds.clear()

        print('CTC: update track controller from ctc object')
        self.update_wayside_from_ctc_signal.emit(self.wayside_update_list, False, [],[])
        print('CTC: update track controller from ctc object called')

    def get_scheduled_trains(self) -> list[Train]:
        trains = []
        for train in self.scheduled_trains.train_list:
            trains.append(train)

        return trains

    def get_running_trains(self) -> list[Train]:
        trains = []
        for train in self.yard_queue:
            trains.append(train)
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

    def set_track_signals(self) -> list[TrackSignal]:
        wayside_track_signal_updates = []
        for block in list(set(self.changed_authorities) | set(self.changed_authorities)):
            wayside_track_signal_updates.append(TrackSignal(block, self.authorities[block], self.suggested_speeds[block]))
        return wayside_track_signal_updates

    def set_block_authority(self, train) -> bool:
        print("CTC: set_block_authority")
        print(f"CTC: Train {train.id} is in block {train.current_block}.")
        for block in train.get_next_authorities():
            if self.authorities[block[0]] != block[1]:
                print(f"CTC: Block {block[0]} authority set to : {block[1]}")
                self.authorities[block[0]] = block[1]
                self.changed_authorities.append(block[0])

            previous_block = train.get_previous_block()

            # No need to change previous blocks when the train is still in the yard.
            if previous_block != 0:
                if self.authorities[train.get_previous_block()] != 0:
                    self.authorities[train.get_previous_block()] = 0
                    self.changed_authorities.append(train.get_previous_block())

        return self.changed_authorities.__len__() > 0

    def set_block_suggested_speeds(self, train) -> bool:
        for block in train.get_next_blocks():
            block_speed_limit = GREEN_LINE[BLOCKS][block].speed_limit

            # meters per second
            adjusted_speed_limit = block_speed_limit * train.get_slowdown() / 3.6

            self.suggested_speeds[block] = adjusted_speed_limit
            self.changed_speeds.append(block)
        self.suggested_speeds[train.get_previous_block()] = 0
        self.changed_speeds.append(train.get_previous_block())

        return self.changed_speeds.__len__() > 0

    """
    Updates the position of each train based on the occupancies received from wayside
    
    Returns False if train hasn't moved and True if train has.
    """
    def update_train_position(self, train: Train) -> bool:
        # check if train is in yard - set authority in that case
        # if train.current_block == GREEN_LINE_YARD_SPAWN:
        #     return True
        # Check if train has moved blocks. Don't update if it hasn't
        if self.blocks[train.current_block] is False and self.blocks[train.get_next_block()] is False:
            return False
        elif self.blocks[train.current_block] is True and self.blocks[train.get_next_block()] is False:
            return False
        elif self.blocks[train.current_block] is False and self.blocks[train.get_next_block()] is True:
            # Check if train has moved from yard
            if train is self.yard:
                print(f"CTC: Train {train.id} has left YARD")
                self.running_trains.append(self.yard)
                self.yard = None

            print(f"CTC: Train {train.id} position updating. Current block: {train.current_block}. Next Block: {train.get_next_block()}.")
            next_block_status = train.set_to_next_block()
            print(f"CTC: Train {train.id} position updated. Current block: {train.current_block}. Next Block: {train.get_next_block()}.")

            if next_block_status == 1:  # at station
                self.running_trains.remove(train)
                print(f"CTC: {train.id} arrived at station {stop_name(train.line_id, train.current_stop)}")
                self.dispatched_trains.schedule_train(train)
            elif next_block_status == 0:  # continue to next station
                pass
            elif next_block_status == -1:  # yard is next
                self.dispatched_trains.schedule_train(train)
            elif next_block_status == -2:  # remove from lists
                self.running_trains.remove(train)
                print("CTC: Train %d reached yard.", train.id)

            self.update_ui_running_trains_table_signal.emit()
            return True
        else:
            return False

    def update_switch_positions(self, switches: list[Switch]):
        for switch in switches:
            self.update_switch_position(switch.block, switch.current_pos)

    def update_switch_position(self, block_id: int, position: int):
        self.switches[block_id].current_pos = position

    def update_signal_statuses(self, signals: list[Light]):
        for signal in signals:
            self.update_signal_status(signal.block, signal.val)

    def update_signal_status(self, block_id: int, signal_green: bool):
        self.lights[block_id] = signal_green

    def update_block_occupancies(self, blocks: dict[int, bool]):
        update = False
        for block in blocks:
            # Only update occupancy when block is changed
            if blocks[block] != self.blocks[block]:
                print("CTC: Block {0} occupancy set to {1}".format(block, blocks[block]))
                self.update_block_occupancy(block, blocks[block])
                update = update | True

        if update:
            self.update_ui_block_table.emit()

    def update_block_occupancy(self, block_id: int, occupied: bool):
        update = False
        self.blocks[block_id] = occupied
        occupied_str = "occupied" if occupied else "vacant"
        print(f"CTC: Block {block_id} set to {occupied_str}.")

    def update_running_trains(self):
        # Move first train in yard queue into yard
        if self.yard is not None:
            # Send authority to yard
            if self.set_block_authority(self.yard) or self.set_block_suggested_speeds(self.yard):
                self.update_ui_block_table.emit()
        for train in self.running_trains:
            if self.update_train_position(train):
                print(f"CTC: Train {train.id} update.")
                if self.set_block_authority(train) or self.set_block_suggested_speeds(train):
                    self.update_ui_block_table.emit()

    def update_railroad_crossing_statuses(self, rr_crossings: list[RRCrossing]):
        for rr_crossing in rr_crossings:
            self.update_railroad_crossing_status(rr_crossing.block, rr_crossing.val)

    def update_railroad_crossing_status(self, block_id: int, crossing_activated: bool):
        self.rr_crossings[block_id] = crossing_activated

    def update_ticket_sales(self, ticket_sales: int):
        pass

    def timer_handler(self):
        pass
