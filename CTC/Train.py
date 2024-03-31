from CTC.Route import Route, Stop
from SystemTime import SystemTime
from Track import MSSD, TRACK

class Train():
    def __init__(self, system_time:SystemTime, id:int, route:Route):
        self.id = id
        self.route = route
        self.line_id = route.line_id
        self.next_stop = 1
        self.current_stop = 0
        self.current_block = -1
        self.authority = 0

        self.system_time = system_time

    def get_next_block(self)->int:
        return self.next_block(self.current_block)
    
    def departure_time(self):
        return self.route.route[self.current_stop].departure_time

    def set_to_next_block(self):
        self.current_block = self.get_next_block()

        if self.route.route[self.next_stop].block == self.current_block:
            # check if route is delayed
            if self.system_time.time() > self.route.route[self.next_stop].arrival_time:
                delay = self.system_time.time() - self.route.route[self.next_stop].arrival_time
                self.route.route[self.next_stop].departure_time += delay
                for stop in self.route.route[self.next_stop + 1:]:
                    stop.arrival_time += delay
                    stop.departure_time += delay

            self.current_stop += 1
            self.next_stop += 1

            if self.next_stop >= self.route.route.__len__():
                self.at_last_stop = True

    def next_block(self, block:int)->int:
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

    def get_next_stop(self)->int:
        return self.next_stop

    def get_destination(self)->Stop:
        return self.route.route[-1]
    
    def add_stop(self, stop:Stop):
        self.route.route.append(stop)

        if self.at_last_stop:
            self.at_last_stop = False
            self.next_stop += 1

    def add_stops(self, stops:list[Stop]):
        for stop in stops:
            self.route.route.append(stop)

        if self.at_last_stop:
            self.at_last_stop = False
            self.next_stop += 1
    
    # returns the next MSSD blocks OR blocks until next stop (including current block)
    def get_next_blocks(self)->list[int]:
        
        next_blocks = [self.current_block]

        prev_block = self.current_block

        for i in range(1, MSSD + 1):
            next_block = self.next_block(prev_block)

            if next_block == self.route.route[self.next_stop].block:
                next_blocks.append(next_block)

                return next_blocks
        
            else:
                next_blocks.append(next_block)
                prev_block = next_block

        return next_blocks
    