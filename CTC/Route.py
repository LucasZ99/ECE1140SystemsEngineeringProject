from CTC.Track import *

class Stop:
    def __init__(self, block:int, arrival_time:float, departure_time:float):
        self.block = block
        self.arrival_time = arrival_time
        self.departure_time = departure_time

class Route:
    def __dfs_find_route(self, line_id, start:int, end:int, path=[])->list[int] | None:
        path = path + [start]
        if start == end:
            return path
        for block in TRACK[line_id][start]:
            if block not in path:
                newpath = self.__dfs_find_route(line_id, block, end, path)
                if newpath:
                    return newpath

    def find_route(self, line_id:int, block1:int, block2:int)->list[int]:
        route = self.__dfs_find_route(line_id, block1, block2)
        if route is not None:
            stops = [route[0]]

            # train will only stop at station stops until final block
            for block in route[1:-1]:
                if block in STATIONS[line_id]:
                    stops.append(block)
            stops.append(route[-1])
            return stops
        else:
            return []
        
    # get the route from a list of blocks
    def get_times_through_route(self, line_id:int, route:list[int])->list[Stop]:
        # first block departure
        # Block #, Arrival Time, Departure Time
        minimum_time_between_stops = [Stop(route[0], 0, 0)]

        for stop1, stop2 in zip(route[:-1], route[1:]):
            # get route between the two blocks:
            route_slice = self.__dfs_find_route(line_id, stop1, stop2)

            time_between_blocks = 0

            # get the time to travel between stops
            if route_slice is not None:
                for block1, block2 in zip(route_slice[:-1], route_slice[1:]):       

                    # calculate travel time - hr
                    time_between_blocks += ((LENGTHS_SPEED_LIMITS[line_id][block1][LENGTH] / (LENGTHS_SPEED_LIMITS[line_id][block1][SPEED_LIMIT] * 1000)) / 2.0) \
                            + ((LENGTHS_SPEED_LIMITS[line_id][block2][LENGTH] / (LENGTHS_SPEED_LIMITS[line_id][block2][SPEED_LIMIT] * 1000)) / 2.0)
                    
                    # convert hr to seconds
                time_between_blocks *= 3600

            previous_stop_departure_time = minimum_time_between_stops[-1].departure_time
            minimum_time_between_stops.append(Stop(stop2, time_between_blocks, time_between_blocks + 60))

        return minimum_time_between_stops

    # Returns the minimum travel time through a given set of stops
    def get_route_travel_time(self, route:list[Stop])->float:
        travel_time = 0
        for stop in route:
            travel_time += stop.arrival_time

        return travel_time
    
    def is_route_schedulable(self, line_id, route:list[Stop], departure_time:float, arrival_time:float)->bool:
        proposed_travel_time = arrival_time - departure_time
        minimum_travel_time = self.get_route_travel_time(route)

        # route[-1].arrival time is going to be the time through the end of the route
        if proposed_travel_time < minimum_travel_time:
            return False
        else:
            return True

    # returns 0 if proposed departure/arrival time pair are not possible. 1 if scheduled
    def schedule_route(self, line_id, route:list[Stop], departure_time:float, arrival_time:float)->list[Stop]:
        proposed_travel_time = arrival_time - departure_time
        minimum_travel_time = self.get_route_travel_time(route)

        # route[-1].arrival time is going to be the time through the end of the route
        if proposed_travel_time > minimum_travel_time:
            # figure out slowdown:
            route_slowdown_factor = proposed_travel_time / minimum_travel_time

            total_travel_time = departure_time

            scheduled_route:list[Stop] = []

            # Yard
            scheduled_route.append(Stop(0, departure_time, departure_time))

            # Rest of stops
            for stop in route[1:]:
                arrival_time = (stop.arrival_time * route_slowdown_factor) + total_travel_time
                scheduled_route.append(Stop(stop.block, arrival_time, arrival_time + 60))

                total_travel_time += (stop.arrival_time * route_slowdown_factor) + 60

            return scheduled_route
        
        else:

            scheduled_route:list[Stop] = []

            # Yard
            scheduled_route.append(Stop(0, departure_time, departure_time))

            total_travel_time = departure_time

            for stop in route[1:]:
                arrival_time = stop.arrival_time + total_travel_time
                scheduled_route.append(Stop(stop.block, arrival_time, arrival_time + 60))

                total_travel_time = stop.arrival_time + 60

            return scheduled_route
