from CTC.CTCSchedule import CTCSchedule
from CTC.BlockModel import BlockModel


class CTC:
    def __init__(self, schedule:CTCSchedule, block_list:list[list[BlockModel]]):
        self.schedule = schedule
        self.block_list = block_list
        self.lines = self.get_lines()

        self.line_stations = []

        # Keep track of all the blocks for a line to use .index to search for block's index in block list.
        self.block_ids = []

        # find stations in each line
        for line_idx in range(len(self.lines)):
            line_stations = []
            block_ids = []
            for block in self.block_list[line_idx]:
                block_ids.append(block.id)
                line_stations.append(block.station_name)
            self.block_ids.append(block_ids)
            self.line_stations.append(line_stations)

    def get_lines(self)->list[str]:
        lines = []
        for line in self.block_list:
            lines.append(line[0].line)
    
        return lines[:]
    
    def get_blocks(self, line_id:int)->list[str]:
        return self.block_ids[line_id]
    
    def get_block_and_station(self, line_id:int, block_id:str)->list[str]:
        block_index = self.block_ids[line_id].index(block_id)

        return self.get_blocks_and_stations(line_id)[block_index]

    def get_blocks_and_stations(self, line_id:int)->list[list[str]]:
        blocks_and_stations = []
        for block_id, station_name in zip(self.block_ids[line_id], self.line_stations[line_id]):
            blocks_and_stations.append([block_id, station_name])

        return blocks_and_stations




    # def get_station_block_id(self, station)
    
    def get_stations(self, line_id:int)->list[str]:
        return self.line_stations[line_id][:]
    
    def get_travel_time_between_blocks_s(self, line_id:int, block_a:str, block_b:str)->float:
        distances = self.get_distances_between_blocks(line_id, block_a, block_b)

        block_a_id = self.block_ids[line_id].index(block_a)
        block_b_id = self.block_ids[line_id].index(block_b)

        block_travel_times_h = [(distances[id] / 1000) / block.speed_limit_kph for (id, block) in enumerate(self.block_list[line_id][block_a_id:(block_b_id + 1)])]
        block_travel_times_s = [travel_time * 3600 for travel_time in block_travel_times_h]
        return sum(block_travel_times_s)


    """
    Calculates the distance between the center points of block_a and block_b. Returns the distance in meters.
    """
    def get_distances_between_blocks(self, line_id:int, block_a:str, block_b:str)->list[float]:
        block_a_id = self.block_ids[line_id].index(block_a)
        block_b_id = self.block_ids[line_id].index(block_b)

        distances = [] 
        distances.append(self.block_list[line_id][block_a_id].length_m / 2)

        for block in self.block_list[line_id][(block_a_id + 1):block_b_id]:
            distances.append(block.length_m)
        
        distances.append(self.block_list[line_id][block_b_id].length_m / 2)

        return distances
