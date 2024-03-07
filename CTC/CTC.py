from collections.abc import MutableSet
from CTC.CTCSchedule import CTCSchedule, Train
from CTC.BlockModel import BlockModel

class RunningTrain(Train):
    def __init__(self, train:Train):
        self.departure_time = train.departure_time
        self.destination = train.destination
        self.line = train.line
        self.route = train.route
        self.number = train.number

        self.next_stop = self.route[0]



class CTC:
    def __init__(self, schedule:CTCSchedule, block_list:list[list[BlockModel]]):
        self.schedule = schedule
        self.block_list = block_list
        self.lines = self.get_lines()

        self.line_stations = []

        # Keep track of all the blocks for a line to use .index to search for block's index in block list.
        self.block_ids = []

        self.track = [{
            "YARD": ["A1"],
            "A1": ["YARD", "A2"],
            "A2": ["A2", "A3"],
            "A3": ["A2", "A4"],
            "A4": ["A3", "A5"],
            "A5": ["A4", "B6", "C11"],
            "B6": ["B7", "A5"],
            "B7": ["B8", "B6"],
            "B8": ["B9"],
            "B9": ["B8", "B10"],
            "B10": ["B9"],
            "C11": ["A5", "C12"],
            "C12": ["C11", "C13"],
            "C13": ["C12", "C14"],
            "C14": ["C13", "C15"],
            "C15": ["C14"]
        }]

        # add yard to each block list
        for blist in self.block_list:
            blist.insert(0, BlockModel("", "YARD", "", False, [], 0, 25)) 

        # find stations in each line
        for line_idx in range(len(self.lines)):
            line_stations = []
            block_ids = []
            for block in self.block_list[line_idx]:
                block_ids.append(block.id)
                line_stations.append(block.station_name)
            self.block_ids.append(block_ids)
            self.line_stations.append(line_stations)

    # The yard is inserted at index 0, so take the line number from index 1.
    def get_lines(self)->list[str]:
        lines = []
        for line in self.block_list:
            lines.append(line[1].line)
    
        return lines[:]
    
    def get_block_data(self, line_id:int)->list[BlockModel]:
        return self.block_list[line_id]
    
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

    # def get_distance_from_yard(self, line_id:int, block_id:str):



    # def get_station_block_id(self, station)
    
    def get_stations(self, line_id:int)->list[str]:
        return self.line_stations[line_id][:]

    def get_station_name(self, line_id:int, block_id:str)->str:
        if block_id == "YARD":
            idx = 0
        else:
            idx = int(block_id[1:])

        return self.line_stations[line_id][idx]
    
    def get_route_to_block(self, line_id:int, origin_block_id:str, destination_block_id:str)->list[str]:
        # print(self.track)
        print(origin_block_id, destination_block_id)

        # paths = sorted(self.find_paths(line_id, origin_block_id, destination_block_id, visited), key=len)
        path = self.find_path(line_id, origin_block_id, destination_block_id)
        print(path)

        return path

    def find_path(self, line_id:int, start:str, end:str, path=[])->list[str]:
        path = path + [start]
        if start == end:
            return path
        for node in self.track[line_id][start]:
            if node not in path:
                newpath = self.find_path(line_id, node, end, path)
                if newpath:
                    return newpath


    # find all paths from start block to end block.
    def find_paths(self, line_id:int, start:str, end:str, path:list[str]=[])->list[list[str]]:
        path = []
        path.append(start)

        if start == end:
            return [path]
        paths = []
        for block in self.track[line_id][start]:
            if block not in path:
                newpaths = self.find_paths(line_id, block, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    
    def get_travel_time_between_blocks_s(self, line_id:int, block_a:str, block_b:str)->float:
        
        distances = self.get_distances_between_blocks(line_id, block_a, block_b)

        block_a_id = self.block_ids[line_id].index(block_a)
        block_b_id = self.block_ids[line_id].index(block_b)

        block_travel_times_s = []
        block_travel_times_s.append(self.get_block_travel_time_s(line_id, block_a_id) / 2)

        for block in range(block_a_id + 1, block_b_id):
            block_travel_times_s.append(self.get_block_travel_time_s(line_id, block))

        block_travel_times_s.append(self.get_block_travel_time_s(line_id, block_b_id) / 2)

        return sum(block_travel_times_s)

    def get_block_travel_time_s(self, line_id:int, block_id:int):
        if block_id == "YARD":
            return 0
        else:
            # block_index = self.block_ids[line_id].index(block_id)
            block_travel_time = ((self.block_list[line_id][block_id].length_m / 1000) / self.block_list[line_id][block_id].speed_limit_kph) * 3600

            return block_travel_time

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
