from CTC.CTCConstants import *
from CTC.CTCSchedule import CTCSchedule
from CTC.Train import Train
from Common import TrackSignal
from PyQt6.QtCore import pyqtSlot, QObject, pyqtSignal, QTimer
from Common.GreenLine import *
from CTC.CTCSignals import CTCSignals
import time as python_time

from Common.Lines import get_line_blocks
from SystemTime import SystemTime


class CTC(QObject):
    # update_wayside_from_ctc_signal = pyqtSignal(list, list, list)

    def __init__(self):
        self.track_signals_to_clear: set[int] = set()
        self.track_signals_to_set: set[int] = set()

        self.track_signals_set: set[int] = set()  # to track when a track circuit breaks

        self.set_switches: dict[int, Switch] = {}
        self.closed_blocks: list[int] = []  # maintain list of closed blocks

        # Maintenance mode: holds list of switches to set. A switch can only be set when the switch's block is not in
        # track_signals_set.
        self.switches_to_set: set[Switch] = set()

        # tracks depature times for throughput tracking. Each time a train leaves the yard throughput increases
        self.departure_times: list[float] = []
        self.throughput = 0

        self.ticket_sales = 0

        self.blocks_set_to_occupied: set[int] = set()
        self.updated_switches: list[Switch] = []
        self.blocks_to_close_open: list[tuple[int, bool]] = []

        self.track_signals: dict[int: TrackSignal] = {}

        init_start_time = python_time.time()

        super().__init__()

        self.connect_frontend_signals()

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
        self.lights: dict[int: Light] = {}
        self.rr_crossings: dict[int, RRCrossing] = {}

        for block in GREEN_LINE[BLOCKS]:
            self.authorities[block] = 0
            self.suggested_speeds[block] = 0
            self.blocks[block] = False

        for switch in GREEN_LINE[SWITCHES]:
            self.switches[switch.block] = switch

        for light in GREEN_LINE[LIGHTS]:
            self.lights[light.block] = light

        for crossing in GREEN_LINE[CROSSINGS]:
            self.rr_crossings[crossing] = crossing

        for block in GREEN_LINE[BLOCKS]:
            self.track_signals[block] = TrackSignal(block, 0, 0)

        self.emit_frontend_signals()

        self.ctc_update_timer = QTimer()
        # self.ctc_update_timer.timeout.connect(self.timer_handler)
        # self.ctc_update_timer.start()

        init_end_time = python_time.time()
        print("CTC Init finished. t={0}".format(init_end_time))
        print("CTC Init time elapsed t={0}".format(init_end_time - init_start_time))

    # TODO this gets called from UI when a train is scheduled;
    # TODO this gets called with update from track controller
    @pyqtSlot()
    def update_ctc_queues(self) -> bool:
        # print("CTC: Updating Queues")
        update_running_trains = False
        update_scheduled_trains = False

        # add dispatched trains to yard queue
        trains_to_dispatch = self.scheduled_trains.dispatch_trains()

        update_throughput = False

        if len(trains_to_dispatch) > 0:
            print("Trains to dispatch")
            update_scheduled_trains = True
            update_running_trains = True
            for train_to_dispatch in trains_to_dispatch:
                self.departure_times.append(SystemTime.time())
                self.throughput += 1
                update_throughput = True
                # self.dispatched_trains.schedule_train(train_to_dispatch)
                self.yard_queue.append(train_to_dispatch)
                print(f"CTC: Train {train_to_dispatch.id} added to Yard Queue")

        trains_to_run = self.dispatched_trains.dispatch_trains()

        if len(trains_to_run) > 0:
            update_running_trains = True
            # add moving trains back to running queue
            for train_to_run in trains_to_run:
                self.running_trains.append(train_to_run)
                self.set_train_track_signals(train_to_run)

        # Move next train into yard when yard is open
        if self.yard is False and len(self.yard_queue) > 0:
            self.yard_train = self.yard_queue.pop(0)
            self.yard = True
            print(f"CTC: Train {self.yard_train.id} set to yard")
            self.set_train_track_signals(self.yard_train)
            print(f"CTC: Track signal set: {self.track_signals.__len__()}")

        if update_running_trains:
            self.get_running_trains_signal_handler()
            self.get_scheduled_trains_signal_handler()
        if len(self.scheduled_trains.train_list) > 0:
            self.get_scheduled_trains_signal_handler()


        if len(self.departure_times) > 0:
            # update throughput - remove all entries that are greater than 1 hr old
            while self.departure_times[0] < SystemTime.time() - 3600:
                if len(self.departure_times) > 0:
                    self.departure_times.pop(0)
                    self.throughput -= 1
                else:
                    break
                update_throughput = True

        if update_throughput:
            self.get_throughput_signal_handler()

        # when this is true, there is a change in CTC state.
        return update_running_trains or update_scheduled_trains

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

        # print(f"CTC: get_running_trains: {trains}")

        trains.sort(key=lambda running_train: running_train.get_destination().arrival_time)
        return trains

    def set_block_to_maintenance_mode(self, line_id: int, block_id: int):
        pass

    def set_switch_position(self, line_id: int, block_id: int, switch: Switch):
        pass

    def get_running_trains_sorted_by_priority(self):
        # sort_by_next_stop_arrival_time = sorted(self.running_trains, key=lambda train: train.arrival_time)
        # sort_by_destination_arrival_time = sorted(sort_by_next_stop_arrival_time,
        #                                           key=lambda train: train.get_destination().arrival_time)
        sort_by_descending_progress = sorted(self.get_running_trains(), key=lambda train: train.progress, reverse=True)

        return sort_by_descending_progress

    def set_track_signals(self) -> None:
        for block in self.track_signals_to_set:
            print(f"CTC: Block {block} track signal set")
            self.track_signals[block] = TrackSignal(abs(block), self.authorities[abs(block)],
                                                    self.suggested_speeds[abs(block)])
            self.track_signals_set.add(abs(block))

        self.track_signals_to_set.clear()

    # Sets the next block in the train's range
    def set_block_authority(self, block: int):
        next_authorities = train.get_next_authorities()
        authority_to_set = next_authorities[-1]
        self.authorities[abs(authority_to_set[0])] = authority_to_set[1]

    def set_train_next_block_suggested_speed(self, train: Train):
        next_blocks = train.get_next_blocks()

        last_block = abs(next_blocks[-1])
        # last_block_speed = get_line_blocks()[last_block].speed_limit * train.get_slowdown() / 3.6
        last_block_speed = get_line_blocks()[last_block].speed_limit / 3.6
        self.suggested_speeds[last_block] = last_block_speed

    # def clear_train_previous_block(self, train: Train):
    #     last_block = abs(train.get_previous_block())
    #     if last_block != 0:
    #         self.authorities[last_block] = 0
    #         self.suggested_speeds[last_block] = 0
    #         self.track_signals.append(TrackSignal(last_block,
    #                                               self.authorities[last_block],
    #                                               self.suggested_speeds[last_block]))

    # sets MSSD track signals when train is (re) dispatched
    # TODO add this to dispatch from dispatched trains too
    def set_train_dispatch_track_signals(self, train: Train):
        next_blocks = train.get_next_authorities()
        for block in next_blocks:
            # set authority
            self.authorities[abs(block[0])] = block[1]
            # speed = get_line_blocks()[abs(block[0])].speed_limit * train.get_slowdown() / 3.6
            speed = get_line_blocks()[abs(block[0])].speed_limit / 3.6
            self.suggested_speeds[abs(block[0])] = speed
            self.track_signals_to_set.add(abs(block[0]))

    def set_train_track_signals(self, train: Train):
        train_next_blocks = train.get_next_blocks()

        # find track signals that are not already set

        next_authorities = train.get_next_authorities()
        next_speeds = [get_line_blocks()[abs(block)].speed_limit / 3.6 for block in train_next_blocks]

        # set values
        for i, block in enumerate(train.get_next_blocks()):
            self.authorities[abs(block)] = next_authorities[i][1]
            self.suggested_speeds[abs(block)] = next_speeds[i]

        for block in train_next_blocks:
            self.track_signals_to_set.add(block)

    def update_train_position(self, train: Train) -> bool:
        """
        Updates the position of each train based on the occupancies received from wayside

        Returns False if train hasn't moved and True if train has.
        """
        # set next track signal when train enters new block
        if abs(train.get_next_block()) in self.blocks_set_to_occupied:
            print("CTC Train {0}: has entered next block".format(train.id))
            self.blocks_set_to_occupied.remove(abs(train.get_next_block()))
            self.track_signals_to_clear.add(abs(train.current_block))

            # Train has moved from yard
            if self.yard is True and train is self.yard_train:
                print(f"CTC: Yard Train {train.id} has entered first block")
                self.running_trains.append(train)
                self.yard = False
                self.set_train_track_signals(train)

            next_block_status = train.set_to_next_block()
            if next_block_status == 1:  # at station
                print(f"\tTrain {train.id} has arrived at station.")
                self.running_trains.remove(train)
                self.dispatched_trains.schedule_train(train)
            elif next_block_status == 0:  # continue to next station
                print(f"\tTrain {train.id} is continuing to the next station")
                self.set_train_track_signals(train)
            elif next_block_status == -1:  # yard is next
                self.running_trains.remove(train)
                self.dispatched_trains.schedule_train(train)
            elif next_block_status == -2:  # at yard. remove from list and clear track signal
                self.track_signals_to_clear.add(GREEN_LINE_YARD_DELETE)
                self.running_trains.remove(train)
            return True
        else:
            return False or self.yard

    def update_switch_positions(self, switches: list[Switch]) -> bool:
        update = False
        for switch in switches:
            if self.update_switch_position(switch.block, switch.current_pos):
                update = True

        if update:
            self.get_switch_positions_signal_handler()

        return update

    def update_switch_position(self, block_id: int, position: int) -> bool:
        if self.switches[block_id].current_pos != position:
            self.switches[block_id].current_pos = position
            return True
        else:
            return False

    def update_signal_statuses(self, signals: list[Light]):
        update = False
        for signal in signals:
            if self.update_signal_status(signal.block, signal.val):
                update = True

        if update:
            self.get_lights_signal_handler()

        return update

    def update_signal_status(self, block_id: int, signal_green: bool):
        if self.lights[block_id] != signal_green:
            self.lights[block_id].val = signal_green
            return True
        else:
            return False

    def update_block_occupancies(self, blocks: dict[int, bool]):
        update = False
        for block in blocks:
            # Only update occupancy when block is changed
            # if blocks[block] != self.blocks[block]:
            self.update_block_occupancy(block, blocks[block])
            update = True
        self.get_blocks_signal_handler()

        return update

    def clear_track_signals(self):
        track_signals_cleared = set()
        for block in self.track_signals_to_clear:
            if block not in self.track_signals_to_set:
                self.track_signals[abs(block)] = TrackSignal(abs(block), 0, 0)
                self.authorities[abs(block)] = 0
                self.suggested_speeds[abs(block)] = 0
                track_signals_cleared.add(abs(block))
        for block in track_signals_cleared:
            self.track_signals_to_clear.remove(block)

    def update_block_occupancy(self, block_id: int, occupied: bool):
        if self.blocks[block_id] is True and occupied is False:
            print("CTC: Block {0} set to false".format(block_id))
        elif self.blocks[block_id] is False and occupied is True:
            print("CTC: Block {0} set to true".format(block_id))
            self.blocks_set_to_occupied.add(abs(block_id))
        self.blocks[block_id] = occupied

    # returns True when a track signal is to be updated
    def update_running_trains(self) -> bool:
        # print("CTC: Update running trains")
        update_running_trains = False

        # Update train in yard
        if self.yard is True:
            if self.update_train_position(self.yard_train):
                update_running_trains = True
        for train in self.running_trains:
            if self.update_train_position(train):
                # print(f"CTC: Train {train.id} update.")
                update_running_trains = True

        # send data to UI
        if update_running_trains:
            self.get_running_trains_signal_handler()
            # self.update_ui_block_table.emit()

        return update_running_trains

    def update_railroad_crossing_statuses(self, rr_crossings: list[RRCrossing]):
        for rr_crossing in rr_crossings:
            self.update_railroad_crossing_status(rr_crossing.block, rr_crossing.val)

    def update_railroad_crossing_status(self, block_id: int, crossing_activated: bool):
        self.rr_crossings[block_id] = crossing_activated

    def get_next_train_number(self):
        return self.scheduled_trains.get_next_train_number()

    def update_ticket_sales(self, ticket_sales: int):
        pass

    def track_signal_update(self) -> bool:
        update = False
        if self.track_signals_to_clear.__len__() > 0:
            self.clear_track_signals()
            update = True
        if self.track_signals_to_set.__len__() > 0:
            self.set_track_signals()
            update = True

        self.get_track_signals_signal_handler()

        return update

    @pyqtSlot()
    def timer_handler(self):
        if self.update_ctc_queues():
            self.update_running_trains()

    # Whole list sent for each
    @pyqtSlot(dict, list, list, list)
    def wayside_event_handler(self, block_occupancy_update: dict[int, bool], switch_positions: list[Switch],
                              light_states: list[Light],
                              rr_crossing_states: list[RRCrossing]):
        self.update_block_occupancies(block_occupancy_update)
        self.update_ctc_queues()
        self.update_switch_positions(switch_positions)
        self.update_signal_statuses(light_states)
        self.update_railroad_crossing_statuses(rr_crossing_states)
        self.update_running_trains()
        self.track_signal_update()
        self.update_wayside()

    def update_wayside(self):
        print("CTC: updating wayside")
        CTCSignals.update_wayside_from_ctc_signal.emit(list(self.track_signals.values()), self.closed_blocks,
                                                 list(self.set_switches.values()))

    # TODO update queues, and if queues are updated, update wayside
    @pyqtSlot(object)
    def schedule_train_signal_handler(self, train: Train):
        print("CTC: Schedule train")
        self.scheduled_trains.schedule_train(train)
        self.get_scheduled_trains_signal_handler()
        self.update_ctc_queues()

        self.get_next_train_number_signal_handler()

        self.track_signal_update()

        if len(self.track_signals) > 0:
            self.update_wayside()

    @pyqtSlot(int)
    def set_mode_signal_handler(self, mode: int):
        self.mode = mode

    @pyqtSlot()
    def update_queues_signal_handler(self):
        self.update_ctc_queues()

    @pyqtSlot()
    def get_running_trains_signal_handler(self):
        CTCSignals.ui_running_trains_signal.emit(self.get_running_trains())

    @pyqtSlot()
    def get_scheduled_trains_signal_handler(self):
        CTCSignals.ui_scheduled_trains_signal.emit(self.get_scheduled_trains())

    @pyqtSlot()
    def get_next_train_number_signal_handler(self):
        print("Next train number: {0}".format(self.get_next_train_number()))
        CTCSignals.ui_next_train_number_signal.emit(self.get_next_train_number())

    @pyqtSlot()
    def get_mode_signal_handler(self):
        CTCSignals.ui_mode_signal.emit(self.mode)

    @pyqtSlot()
    def get_blocks_signal_handler(self):
        CTCSignals.ui_blocks_signal.emit(self.blocks)

    @pyqtSlot()
    def get_track_signals_signal_handler(self):
        CTCSignals.ui_track_signals_signal.emit(self.track_signals)

    @pyqtSlot()
    def get_authorities_signal_handler(self):
        # print("CTC: sending authorities to UI")
        CTCSignals.ui_authorities_signal.emit(self.authorities)

    @pyqtSlot()
    def get_suggested_speeds_signal_handler(self):
        CTCSignals.ui_suggested_speeds_signal.emit(self.suggested_speeds)

    @pyqtSlot()
    def get_switch_positions_signal_handler(self):
        CTCSignals.ui_switch_positions_signal.emit(list(self.switches.values()))

    @pyqtSlot()
    def get_lights_signal_handler(self):
        CTCSignals.ui_lights_signal.emit(list(self.lights.values()))

    @pyqtSlot()
    def get_railroad_crossings_signal_handler(self):
        CTCSignals.ui_railroad_crossings_signal.emit(list(self.rr_crossings.values()))

    @pyqtSlot()
    def get_throughput_signal_handler(self):
        CTCSignals.ui_throughput_signal.emit(self.throughput)

    @pyqtSlot()
    def get_ticket_sales_signal_handler(self):
        CTCSignals.ui_ticket_sales.emit(self.ticket_sales)

    def connect_frontend_signals(self):
        CTCSignals.ctc_get_scheduled_trains_signal.connect(self.get_running_trains_signal_handler)
        CTCSignals.ctc_get_next_train_number_signal.connect(self.get_next_train_number_signal_handler)
        CTCSignals.ctc_get_running_trains_signal.connect(self.get_running_trains_signal_handler)
        CTCSignals.ctc_get_mode_signal.connect(self.get_mode_signal_handler)
        CTCSignals.ctc_get_blocks_signal.connect(self.get_blocks_signal_handler)
        CTCSignals.ctc_get_authority_signal.connect(self.get_authorities_signal_handler)
        CTCSignals.ctc_get_suggested_speeds_signal.connect(self.get_suggested_speeds_signal_handler)
        CTCSignals.ctc_get_switch_positions_signal.connect(self.get_switch_positions_signal_handler)
        CTCSignals.ctc_get_lights_signal.connect(self.get_lights_signal_handler)
        CTCSignals.ctc_get_railroad_crossings_signal.connect(self.get_railroad_crossings_signal_handler)
        CTCSignals.ctc_get_track_signals_signal.connect(self.get_track_signals_signal_handler)

        CTCSignals.ctc_schedule_train_signal.connect(self.schedule_train_signal_handler)
        CTCSignals.ctc_set_mode_signal.connect(self.set_mode_signal_handler)
        CTCSignals.ctc_update_queues_signal.connect(self.update_queues_signal_handler)
        CTCSignals.ctc_get_throughput_signal.connect(self.get_throughput_signal_handler)

    def emit_frontend_signals(self):
        self.get_next_train_number_signal_handler()
        self.get_running_trains_signal_handler()
        self.get_scheduled_trains_signal_handler()
        self.get_blocks_signal_handler()
        self.get_lights_signal_handler()
        self.get_throughput_signal_handler()
        self.get_mode_signal_handler()
        self.get_ticket_sales_signal_handler()
        self.get_railroad_crossings_signal_handler()
        self.get_switch_positions_signal_handler()
