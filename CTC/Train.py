from CTC.Route import Stop
import CTC.Route as Route
from SystemTime import SystemTime
from Common.Constants import MSSD
from Common.GreenLine import *


class Train:
    def __init__(self, id: int, line_id: int, route: list[Stop]):
        self.id = id
        self.route = route
        self.line_id = line_id
        self.next_stop = 1
        self.current_stop = 0
        self.current_block = GREEN_LINE_YARD_SPAWN
        self.authority = 0
        self.at_yard = True
        self.at_last_stop = False

        self.previous_block = 0
        self.progress = 0
        self.time_to_departure = 0

        # determine slowdown of route

        # TODO fix this with route refactor
        self.speed_factor = Route.get_route_travel_time(
            Route.get_route_stops(self.line_id, [stop.block for stop in self.route])
        ) / Route.get_route_travel_time(self.route)

    def get_slowdown(self) -> float:
        return self.speed_factor

    def get_next_block(self) -> int:
        return self.next_block(self.current_block)

    def departure_time(self) -> float:
        return self.route[self.current_stop].departure_time

    def arrival_time(self) -> float:
        return self.route[self.next_stop].arrival_time

    def blocks_to_next_stop(self) -> int:
        return len(Route.find_path(self.line_id, self.current_block, self.route[self.next_stop].block))

    """
    Sets the train to the next block.
    :returns 0 for continuing to next station, 1 for at next station, -1 for last station - dispatch to yard, or -2 for reached yard.
    """
    def set_to_next_block(self) -> int:
        self.previous_block = self.current_block
        self.current_block = self.get_next_block()
        self.progress += 1

        # check if at next stop
        if self.route[self.next_stop].block == self.current_block:
            # check if route is delayed
            if SystemTime.time() > self.route[self.next_stop].arrival_time:
                delay = SystemTime.time() - self.route[self.next_stop].arrival_time
                self.route[self.next_stop].departure_time += delay
                for stop in self.route[self.next_stop + 1:]:
                    stop.arrival_time += delay
                    stop.departure_time += delay

            self.current_stop += 1
            self.next_stop += 1

            # at yard
            if self.current_stop == self.route.__len__() - 1:
                self.at_last_stop = True
                return -2
            # last stop - yard next
            elif self.current_stop == self.route.__len__() - 2:
                return -1
            # otherwise, intermediate stop
            else:
                return 1

        # not at stop
        else:
            return 0

    def next_block(self, block: int) -> int:
        curr_block_idx = GREEN_LINE[ROUTE].index(block)
        return GREEN_LINE[ROUTE][curr_block_idx+1]

    def get_next_stop(self) -> int:
        return self.next_stop

    def get_destination(self) -> Stop:
        # route[-1] is the yahd.
        return self.route[-2]

    def add_stop(self, stop: Stop):
        self.route.append(stop)

        if self.at_last_stop:
            self.at_last_stop = False
            self.next_stop += 1

    def add_stops(self, stops: list[Stop]):
        for stop in stops:
            self.route.append(stop)

        if self.at_last_stop:
            self.at_last_stop = False
            self.next_stop += 1

    # returns the next MSSD blocks OR blocks until next stop (including current block)
    def get_next_blocks(self) -> list[int]:
        next_blocks = [self.current_block]
        prev_block = self.current_block

        for i in range(1, min(MSSD + 1, self.blocks_to_next_stop())):
            next_block = self.next_block(prev_block)
            if next_block == self.route[self.next_stop].block:
                next_blocks.append(next_block)

                return next_blocks

            else:
                next_blocks.append(next_block)
                prev_block = next_block

        return next_blocks

    """
    Returns the train's authorities for the next MSSD blocks or the blocks until the next stop (whichever is shorter),
    including the current block.
    """
    def get_next_authorities(self) -> list[tuple[int, int]]:
        authorities = []
        next_blocks = self.get_next_blocks()
        for i in range(0, min(MSSD + 1, self.blocks_to_next_stop())):
            authorities.append((next_blocks[i], self.blocks_to_next_stop() - i - 1))

        # print("CTC.Train: get_next_authorities")
        # print(f"\t{authorities}\n")

        return authorities

    # def get_next_speeds(self):
    #     speeds = []
    #     next_blocks = self.get_next_blocks()
    #     for i in range(0, min(MSSD + 1, self.blocks_to_next_stop())):
    #         speeds.append((next_blocks[i], ))

    def get_previous_block(self) -> int:
        return self.previous_block

    def __str__(self):
        s = ""

        # Train Number
        s += f"Train: {self.id}\n"
        # Line Number
        s += f"Line: {self.line_id}\n"

        # Current Stop
        s += f"Current Stop: {self.current_stop}\n"

        # Current Block
        s += f"Current Block: {self.current_block}\n"

        # Next Block
        s += f"Next Block: {self.next_block(self.current_block)}\n"

        # List of Stops
        s += f"Stops:"

        for stop in self.route:
            s += stop.__str__() + "\n"

        return s
