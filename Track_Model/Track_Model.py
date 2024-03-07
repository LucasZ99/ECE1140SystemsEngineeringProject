import pandas as pd
import numpy as np
import sys
import random


class TrackModel:
    def __init__(self, file_name):
        d = pd.read_excel(file_name, header=None)  # We will also load our header row, and block IDs will map to index
        self.data = d.to_numpy()
        self.check_data()
        self.line_name = self.data[0, 0]
        self.num_blocks = len(self.data)
        self.ticket_sales = 0
        self.environmental_temperature = 74
        # giving random embarking num and ticket sales
        for i in range(0, self.num_blocks):
            if self.data[i, 16] == 0:
                self.data[i, 16] = random.randint(1, 100)
                self.data[i, 17] = random.randint(1, self.data[i, 16])
        self.authority = []
        self.speed = []

    def get_data(self):
        return self.data

    def get_line_name(self):
        return self.line_name

    def get_num_blocks(self):
        return self.num_blocks

    def get_ticket_sales(self):
        return self.ticket_sales

    def get_section(self, section_id_start, section_id_end=None):
        if section_id_end is None:
            section_id_end = section_id_start
        first_index = self.data[:, 1].tolist().index(section_id_start)
        last_index = self.num_blocks - self.data[:, 1].tolist()[::-1].index(section_id_end)
        return self.data[first_index:last_index, :]

    def set_data(self, file_name):
        d = pd.read_excel(file_name, header=None)  # We will also load our header row, and block IDs will map to index
        self.data = d.to_numpy()
        self.check_data()
        self.line_name = self.data[0, 0]
        self.num_blocks = len(self.data)

    def set_block_occupancy(self, block, occupancy):
        self.data[block, 7] = occupancy

    def check_data(self):  # update this in future to validate data further
        if len(self.data) == 0:
            print('***\nExiting, Data input is empty\n***')
            exit()
    # is working for initialization but not for setting data

    def get_block_table(self, section_id):
        n = len(self.get_section(section_id))
        block_table = np.empty(shape=(n + 1, 7), dtype=object)
        # everything comes from data except occupancy (from train model) and temp (from temp controls)
        # but even those values will be stored in our data
        block_table[0, :] = ['Block', 'Length', 'Grade', 'Speed Limit', 'Elevation', 'Occupancy', 'Temperature']
        block_table[1:n+1, 0:7] = self.get_section(section_id)[:, 2:9]
        return block_table

    def get_station_table(self, section_id):
        relevant_section_data = self.get_section(section_id)[:, [9, 2, 10, 12, 16, 17]]
        arr = relevant_section_data.copy()
        filtered_arr = arr[np.array(['Station' in str(x) for x in arr[:, 0]])]

        return filtered_arr

    def get_infrastructure_table(self, section_id):
        arr = self.get_section(section_id)[:, [9, 2, 11]]
        filtered_arr = arr[~np.isnan(np.array([len(str(x)) if isinstance(x, str) else x for x in arr[:, 0]])) & (
                    np.char.find(arr[:, 0].astype(str), "Station") == -1)]
        return filtered_arr

    def set_env_temperature(self, temperature):
        self.environmental_temperature = temperature
        self.data[1:, 8] = temperature

    def set_heaters(self, value):  # For now acts instantaneously, but may need to stimulate heating over time
        heaters = self.data[1:, 12]
        if value:
            heaters[heaters == 0] = 1
        else:
            heaters[heaters == 1] = 0
        for i in range(0, len(heaters)):
            if heaters[i] == 1:
                self.data[i+1, 8] = 90

    def set_power_failure(self, block, value):
        self.data[block, 13] = value
        self.set_occupancy_from_failures(block)

    def set_track_circuit_failure(self, block, value):
        self.data[block, 14] = value
        self.set_occupancy_from_failures(block)

    def set_broken_rail_failure(self, block, value):
        self.data[block, 15] = value
        self.set_occupancy_from_failures(block)
        # this block can no longer be occupied if value = 1

    def set_occupancy_from_failures(self, block):
        # broken rail takes priority as it is infinite resistance
        # sets to 0 if no failures, so must account for train presence afterwords whenever using this function
        p = self.data[block, 13]
        tc = self.data[block, 14]
        br = self.data[block, 15]

        if br:
            self.set_block_occupancy(block, 0)
        elif p or tc:
            self.set_block_occupancy(block, 1)
        else:
            self.set_block_occupancy(block, 0)

    def set_occupancy_from_train_presence(self, block, presence):
        br = self.data[block, 15]
        if br:
            self.set_block_occupancy(block, 0)
        else:
            self.set_block_occupancy(block, presence)

    #
    #
    # Communication for other modules
    #
    #

    # RECEIVING (setters)

    # track controller

    def update_authority(self, authority: list[int]):
        self.authority = authority

    def update_speed(self, speed: list[float]):
        self.speed = speed

    def toggle_switch(self, block_id: int):
        pass

    def toggle_signal(self, block_id: int):
        pass

    def toggle_crossing(self, block_id: int):
        pass

    # train model

    def train_spawned(self):
        pass

    def train_presence_changed(self, train_id: int):
        pass

    def set_disembarking_passengers(self, station_id: int, disembarking_passengers: int):
        pass

    # SENDING (getters)

    # track controller

    def get_tc_block_occupancy(self, starting_block: int, ending_block: int):
        pass

    # train model

    def get_tm_authority(self, train_id: int) -> list[int]:
        return self.authority

    def get_tm_speed(self, train_id: int) -> list[float]:
        return self.speed
    
    def get_tm_beacon(self, train_id: int) -> str:
        pass

    def get_tm_grade(self, train_id: int) -> int:
        pass

    def get_tm_elevation(self, train_id: int) -> float:
        pass

    def get_tm_underground_status(self, train_id: int) -> bool:
        pass

    def get_tm_embarking_passengers(self, station_block: int) -> int:
        pass

    # ctc
