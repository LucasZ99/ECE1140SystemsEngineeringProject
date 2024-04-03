from CTC.Route import Stop, Route
from SystemTime import SystemTime
from CTC.Track import MSSD, TRACK, GREEN_LINE_YARD_SPAWN, GREEN_LINE_YARD_DELETE


class Train():
    def __init__(self, system_time: SystemTime, id: int, line_id: int, route: list[Stop]):
        self.id = id
        self.route = route
        self.line_id = line_id
        self.next_stop = 1
        self.current_stop = 0
        self.current_block = GREEN_LINE_YARD_SPAWN
        self.authority = 0
        self.at_last_stop = False

        # determine slowdown of route
        self.speed_factor = Route().get_route_travel_time(
            Route().get_times_through_route(self.line_id, [stop.block for stop in self.route])
        ) / Route().get_route_travel_time(self.route)

        self.system_time = system_time

    def get_slowdown(self) -> float:
        return self.speed_factor

    def get_next_block(self) -> int:
        return self.next_block(self.current_block)

    def departure_time(self) -> float:
        return self.route[self.current_stop].departure_time

    def arrival_time(self) -> float:
        return self.route[self.next_stop].arrival_time

    def blocks_to_next_stop(self) -> int:
        return len(Route().dfs_find_route(self.line_id, self.current_block, self.route[self.next_stop]))

    """
    Sets the train to the next block.
    :returns 0 for continuing to next station, 1 for at next station, -1 for last station - dispatch to yard, or -2 for reached yard.
    """

    def set_to_next_block(self) -> int:
        self.current_block = self.get_next_block()

        # check if at next stop
        if self.route[self.next_stop].block == self.current_block:
            # check if route is delayed
            if self.system_time.time() > self.route[self.next_stop].arrival_time:
                delay = self.system_time.time() - self.route[self.next_stop].arrival_time
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
        next_blocks = TRACK[self.line_id][block]

        # For bi-directional blocks, next_blocks = [current_block, next_block]
        if block in next_blocks:
            if next_blocks[0] == block:
                next_block = next_blocks[1]
            else:
                next_block = next_blocks[0]
        else:
            next_block = next_blocks[0]

        return next_block

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

    # returns the next MSSD blocks OR blocks until next stop (excluding current block)
    def get_next_blocks(self) -> list[int]:

        next_blocks = []

        prev_block = self.current_block

        for i in range(1, MSSD + 1):
            next_block = self.next_block(prev_block)
            if next_block == self.route[self.next_stop].block:
                next_blocks.append(next_block)

                return next_blocks

            else:
                next_blocks.append(next_block)
                prev_block = next_block

        return next_blocks
