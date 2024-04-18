from CTC.CTCConstants import *
from CTC.CTCSchedule import CTCSchedule
from CTC.Train import Train
from Common import TrackSignal
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from Common.GreenLine import *

import time as python_time

from Common.Lines import stop_name, get_line_blocks


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

        self.blocks_to_clear = set()
        self.blocks_set_to_occupied: set[int] = set()
        self.blocks_set_to_vacant: list[int] = []
        self.updated_switches: list[Switch] = []
        self.blocks_to_close_open: list[tuple[int, bool]] = []
        self.maintenance_mode_override_flag: bool = False
        self.authority_speed_update: list[TrackSignal] = []
        init_start_time = python_time.time()
        # print("CTC Init started t={0}".format(init_start_time))

        super().__init__()

        self.mode = AUTOMATIC_MODE

        self.wayside_update_list: list[tuple[int, int, float]] = []

        self.scheduled_trains = CTCSchedule()
        self.dispatched_trains = CTCSchedule()

        self.running_trains: list[Train] = []
        self.yard_queue: list[Train] = []

        # Holds the current Train in the yard.
        self.yard_train: Train | None = None
        self.yard: bool = False

        self.changed_blocks: set[int] = set()
        self.changed_blocks_count = 0

        self.authorities: dict[int, int] = {}
        self.blocks: dict[int, bool] = {}
        self.suggested_speeds: dict[int, float] = {}
        self.switches: dict[int: Switch] = {}
        self.lights: dict[int: bool] = {}
        self.rr_crossings: dict[int, bool] = {}

        for block in GREEN_LINE[BLOCKS]:
            self.authorities[block] = 0
            self.suggested_speeds[block] = 0
            self.blocks[block] = False

        for switch in GREEN_LINE[SWITCHES]:
            self.switches[switch.block] = switch

        for light in GREEN_LINE[LIGHTS]:
            self.lights[light.block] = light.val

        for crossing in GREEN_LINE[CROSSINGS]:
            self.rr_crossings[crossing] = False

        init_end_time = python_time.time()
        print("CTC Init finished. t={0}".format(init_end_time))
        print("CTC Init time elapsed t={0}".format(init_end_time - init_start_time))

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
            self.set_train_dispatch_track_signals(train_to_run)
            update = True

        # Move next train into yard when yard is open
        if self.yard is False and len(self.yard_queue) > 0:
            self.yard_train = self.yard_queue.pop(0)
            self.yard = True
            print(f"CTC: Train {self.yard_train.id} set to yard")
            self.set_train_dispatch_track_signals(self.yard_train)
            update = True
            # self.set_track_signals()

        if update:
            self.update_ui_running_trains_table_signal.emit()
            return True
        else:
            return False

    def get_scheduled_trains(self) -> list[Train]:
        trains = []
        for train in self.scheduled_trains.train_list:
            trains.append(train)
        return trains

    def get_running_trains(self) -> list[Train]:
        trains = []
        if self.yard is True:
            trains.append(self.yard_train)
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

    def set_track_signals(self) -> None:
        # print("CTC: Set Track Signals")
        # print(self.changed_blocks)
        # self.authority_speed_update.clear()
        for block in self.changed_blocks:
            print(f"CTC: Block {block} track signal set")
            self.authority_speed_update.append(TrackSignal(block, self.authorities[block], self.suggested_speeds[block]))
        self.clear_changed_blocks()

    # Sets the next block in the train's range
    def set_train_next_block_authority(self, train: Train):
        next_authorities = train.get_next_authorities()
        authority_to_set = next_authorities[-1]
        self.authorities[abs(authority_to_set[0])] = authority_to_set[1]

    def set_train_next_block_suggested_speed(self, train: Train):
        next_blocks = train.get_next_blocks()

        last_block = abs(next_blocks[-1])
        last_block_speed = get_line_blocks()[last_block].speed_limit * train.get_slowdown() / 3.6
        self.suggested_speeds[last_block] = last_block_speed

    def clear_train_previous_block(self, train: Train):
        last_block = abs(train.get_previous_block())
        if last_block != 0:
            self.authorities[last_block] = 0
            self.suggested_speeds[last_block] = 0
            self.authority_speed_update.append(TrackSignal(last_block,
                                                           self.authorities[last_block],
                                                           self.suggested_speeds[last_block]))

    # sets MSSD track signals when train is (re) dispatched
    # TODO add this to dispatch from dispatched trains too
    def set_train_dispatch_track_signals(self, train: Train):
        next_blocks = train.get_next_authorities()
        for block in next_blocks:
            # set authority
            self.authorities[abs(block[0])] = block[1]
            speed = get_line_blocks()[abs(block[0])].speed_limit * train.get_slowdown() / 3.6
            self.suggested_speeds[abs(block[0])] = speed
            self.set_block_track_signal(block[0])

    def set_block_track_signal(self, block: int):
        self.authority_speed_update.append(TrackSignal(abs(block),
                                                       self.authorities[abs(block)],
                                                       self.suggested_speeds[abs(block)]))

    def set_train_next_block_track_signal(self, train: Train):
        self.set_train_next_block_authority(train)
        self.set_train_next_block_suggested_speed(train)

        next_block_to_set = abs(train.get_next_blocks()[-1])
        self.authority_speed_update.append(TrackSignal(next_block_to_set,
                                                       self.authorities[next_block_to_set],
                                                       self.suggested_speeds[next_block_to_set]))

    # def set_block_authority(self, train) -> bool:
    #     update = False
    #     for block in train.get_next_authorities():
    #         if self.authorities[abs(block[0])] != block[1]:
    #             print(f"CTC: Block {block[0]} authority set to {block[1]}")
    #             self.authorities[abs(block[0])] = block[1]
    #             self.add_to_changed_blocks(abs(block[0]))
    #             update = True
    #
    #     previous_block = train.get_previous_block()
    #
    #     # No need to change previous blocks when the train is still in the yard.
    #     if previous_block != 0:
    #         # print(f"CTC: Train previous block {previous_block} authority set queued to 0")
    #         if self.authorities[train.get_previous_block()] != 0:
    #             self.authorities[train.get_previous_block()] = 0
    #             self.add_to_changed_blocks(train.get_previous_block())
    #             update = True
    #     # else:
    #     #     # print(f"CTC: Train previous block {previous_block} is 0. Not updating.")
    #     #     pass
    #
    #     # print(f"CTC: Authority update: {update}")
    #     return update

    def add_to_changed_blocks(self, block: int):
        if block == 0:
            raise
        self.changed_blocks.add(block)
        self.changed_blocks_count += 1

    def remove_from_changed_blocks(self, block: int):
        self.changed_blocks.remove(block)
        self.changed_blocks_count -= 1

    def clear_changed_blocks(self):
        self.changed_blocks.clear()

    # def set_block_suggested_speeds(self, train) -> bool:
    #     # print("CTC: Set Block Suggested Speeds")
    #     # breakpoint()
    #     update = False
    #     for block in train.get_next_blocks():
    #         block_speed_limit = GREEN_LINE[BLOCKS][block].speed_limit
    #
    #         # meters per second
    #         adjusted_speed_limit = block_speed_limit * train.get_slowdown() / 3.6
    #
    #         if self.suggested_speeds[block] != adjusted_speed_limit:
    #             self.suggested_speeds[block] = adjusted_speed_limit
    #             self.add_to_changed_blocks(block)
    #             update = True
    #
    #     previous_block = train.get_previous_block()
    #
    #     # No need to change previous blocks when the train is still in the yard.
    #     if previous_block != 0:
    #         # print(f"CTC: Train previous block {previous_block} authority set queued to 0")
    #         if self.suggested_speeds[train.get_previous_block()] != 0:
    #             self.suggested_speeds[train.get_previous_block()] = 0
    #             self.add_to_changed_blocks(train.get_previous_block())
    #             update = True
    #
    #     return update

    """
    Updates the position of each train based on the occupancies received from wayside
    
    Returns False if train hasn't moved and True if train has.
    """
    def update_train_position(self, train: Train) -> bool:
        # check if train is in yard - set authority in that case
        # if train.current_block == GREEN_LINE_YARD_SPAWN:
        #     return True
        # Check if train has moved blocks. Don't update if it hasn't
        # if self.blocks[train.current_block] is False and self.blocks[train.get_next_block()] is False:
        #     return False

        # set next track signal when train enters new block
        if train.get_next_block() in self.blocks_set_to_occupied:
            # acknowledge block
            self.blocks_set_to_occupied.remove(train.get_next_block())

            self.blocks_to_clear.add(train.current_block)


            # Train has moved from yard
            if self.yard is True and train is self.yard_train:
                print(f"CTC: Yard Train {train.id} has entered first block")
                self.running_trains.append(train)
                self.yard = False

            next_block_status = train.set_to_next_block()
            if next_block_status == 1:  # at station
                print(f"CTC: Train {train.id} has arrived at station.")
                self.running_trains.remove(train)
                self.dispatched_trains.schedule_train(train)
            elif next_block_status == 0:  # continue to next station
                print(f"CTC: Train {train.id} has entered next block.")
                self.set_train_next_block_track_signal(train)
            elif next_block_status == -1:  # yard is next
                self.dispatched_trains.schedule_train(train)
            elif next_block_status == -2:  # remove from lists
                self.running_trains.remove(train)

            return True
        # train leaves previous block
        # elif train.previous_block in self.blocks_set_to_vacant and self.blocks[train.current_block] is True:
        #     # Check if train has left yard - clear yard if so
        #     if self.yard is True and train is self.yard_train:
        #         print(f"CTC: Train {train.id} has left YARD")
        #         self.yard = False
        #
        #     # always clear the previous block when train enters a new block
        #     self.clear_train_previous_block(train)
        #
        #     return True
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
        self.blocks_set_to_vacant.clear()
        update = False
        for block in blocks:
            # Only update occupancy when block is changed
            if blocks[block] != self.blocks[block]:
                print(f"CTC: Block {block} occupancy set to {blocks[block]}")
                self.update_block_occupancy(block, blocks[block])
                update = True
        if update:
            self.update_ui_block_table.emit()

    def clear_block_track_signal(self, block: int):
        self.suggested_speeds[abs(block)] = 0
        self.authorities[abs(block)] = 0
        self.authority_speed_update.append(TrackSignal(abs(block), 0, 0))

    def update_block_occupancy(self, block_id: int, occupied: bool):
        if self.blocks[block_id] is True and occupied is False:
            self.blocks_set_to_vacant.append(block_id)
            # clear track signal in block
            if block_id in self.blocks_to_clear:
                self.blocks_to_clear.remove(block_id)
                self.clear_block_track_signal(block_id)
        else:
            self.blocks_set_to_occupied.add(block_id)
        self.blocks[block_id] = occupied
        occupied_str = "occupied" if occupied else "vacant"
        # print(f"CTC: Block {block_id} set to {occupied_str}.")

    # returns True when a track signal is to be updated
    def update_running_trains(self) -> bool:
        update = False

        # Update train in yard
        if self.yard is True:
            if self.update_train_position(self.yard_train):
                update = True
        for train in self.running_trains:
            if self.update_train_position(train):
                # print(f"CTC: Train {train.id} update.")
                update = True

        if update:
            self.update_ui_running_trains_table_signal.emit()
            # self.update_ui_block_table.emit()

        return update

    def update_railroad_crossing_statuses(self, rr_crossings: list[RRCrossing]):
        for rr_crossing in rr_crossings:
            self.update_railroad_crossing_status(rr_crossing.block, rr_crossing.val)

    def update_railroad_crossing_status(self, block_id: int, crossing_activated: bool):
        self.rr_crossings[block_id] = crossing_activated

    def update_ticket_sales(self, ticket_sales: int):
        pass

    def timer_handler(self):
        pass
