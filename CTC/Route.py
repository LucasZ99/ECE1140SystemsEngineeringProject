from time import localtime, strftime

from Common.GreenLine import *


class Stop:
    def __init__(self, block: int, arrival_time: float, departure_time: float):
        self.block = block
        self.arrival_time = arrival_time
        self.departure_time = departure_time

    def __str__(self):
        s = f"{self.block}"
        if get_block(self.block) in GREEN_LINE[STATIONS]:
            s += f": " + GREEN_LINE[STATIONS][get_block(self.block)]

        arrival_time_str = strftime("%H:%m", localtime(self.arrival_time))
        departure_time_str = strftime("%H:%m", localtime(self.departure_time))

        s += f" {arrival_time_str} {departure_time_str}"

        return s


def get_block(block: int) -> int:
    if block in GREEN_LINE[TWO_WAY_BLOCKS].keys():
        return GREEN_LINE[TWO_WAY_BLOCKS][block]
    else:
        return block


def find_path(line_id: int, block1: int, block2: int) -> list[int]:
    start_idx = GREEN_LINE[ROUTE].index(block1)
    end_idx = GREEN_LINE[ROUTE].index(block2)

    return GREEN_LINE[ROUTE][start_idx:end_idx + 1]


def find_route(line_id: int, block1: int, block2: int) -> list[int]:
    route = find_path(line_id, block1, block2)
    if route is not None:
        stops = [route[0]]

        # train will only stop at station stops until final block
        for block in route[1:-1]:
            if get_block(block) in GREEN_LINE[STATIONS]:
                stops.append(block)
        stops.append(route[-1])
        return stops
    else:
        return []


def get_block_pair_travel_time(line_id: int, block1: int, block2: int) -> float:
    route_block1_to_block2 = find_path(line_id, block1, block2)

    time_between_blocks = 0

    # get the time to travel between stops
    if route_block1_to_block2 is not None:
        for block1, block2 in zip(route_block1_to_block2[:-1], route_block1_to_block2[1:]):
            # calculate travel time - hr

            print(GREEN_LINE[BLOCKS][get_block(block1)])

            time_between_blocks += ((GREEN_LINE[BLOCKS][get_block(block1)].length / (
                    GREEN_LINE[BLOCKS][get_block(block1)].speed_limit * 1000)) / 2.0) \
                                   + ((GREEN_LINE[BLOCKS][get_block(block2)].length / (
                    GREEN_LINE[BLOCKS][get_block(block2)].speed_limit * 1000)) / 2.0)

            # convert hr to seconds
        time_between_blocks *= 3600

    return time_between_blocks


# get the route from a list of blocks
def get_times_through_route(line_id: int, route: list[int]) -> list[Stop]:
    # first block departure
    # Block #, Arrival Time, Departure Time
    minimum_time_between_stops = [Stop(route[0], 0, 0)]

    for stop1, stop2 in zip(route[:-1], route[1:]):
        # get route between the two blocks:
        time_between_blocks = get_block_pair_travel_time(line_id, stop1, stop2)

        previous_stop_departure_time = minimum_time_between_stops[-1].departure_time
        minimum_time_between_stops.append(Stop(stop2, time_between_blocks, time_between_blocks + 60))

    return minimum_time_between_stops


# Returns the minimum travel time through a given set of stops
def get_route_travel_time(route: list[Stop]) -> float:
    travel_time = 0
    for stop in route:
        travel_time += stop.arrival_time

    return travel_time


def is_route_schedulable(line_id, route: list[Stop], departure_time: float, arrival_time: float) -> bool:
    proposed_travel_time = arrival_time - departure_time
    minimum_travel_time = get_route_travel_time(route)

    # route[-1].arrival time is going to be the time through the end of the route
    if proposed_travel_time < minimum_travel_time:
        return False
    else:
        return True


# returns 0 if proposed departure/arrival time pair are not possible. 1 if scheduled
def schedule_route(line_id, route: list[Stop], departure_time: float, arrival_time: float) -> list[Stop]:
    proposed_travel_time = arrival_time - departure_time
    minimum_travel_time = get_route_travel_time(route)

    route.append(Stop(GREEN_LINE_YARD_DELETE, route[-1].departure_time,
                      get_block_pair_travel_time(line_id, route[-1].block, GREEN_LINE_YARD_DELETE)))

    # route[-1].arrival time is going to be the time through the end of the route
    if proposed_travel_time > minimum_travel_time:
        # figure out slowdown:
        route_slowdown_factor = proposed_travel_time / minimum_travel_time

        total_travel_time = departure_time

        # Yard
        scheduled_route: list[Stop] = [Stop(GREEN_LINE_YARD_SPAWN, departure_time, departure_time)]

        # Rest of stops
        for stop in route[1:]:
            arrival_time = (stop.arrival_time * route_slowdown_factor) + total_travel_time
            scheduled_route.append(Stop(stop.block, arrival_time, arrival_time + 60))

            total_travel_time += (stop.arrival_time * route_slowdown_factor) + 60

        return scheduled_route

    else:
        # Yard
        scheduled_route: list[Stop] = [Stop(GREEN_LINE_YARD_SPAWN, departure_time, departure_time)]

        total_travel_time = departure_time

        for stop in route[1:]:
            arrival_time = stop.arrival_time + total_travel_time
            scheduled_route.append(Stop(stop.block, arrival_time, arrival_time + 60))

            total_travel_time = stop.arrival_time + 60

        return scheduled_route
