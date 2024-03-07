import pandas as pd
import numpy as np
import random

from Subclasses import Station, Signal, Crossing, Switch, Block, Train


class TrackModel:
    def __init__(self, file_name):
        # data from excel
        d = pd.read_excel(file_name, header=None)  # We will also load our header row, and block IDs will map to index
        self.data = d.to_numpy()
        self.check_data()
        self.line_name = self.data[0, 0]
        self.num_blocks = len(self.data) - 1

        # blocks and infrastructure objects arrays
        self.blocks = np.array([])
        self.stations = np.array([])
        self.signals = np.array([])
        self.crossings = np.array([])
        self.switches = np.array([])
        for i in range(1, self.num_blocks + 1):
            block = Block(self.data[i, 1:10])
            infrastructure_list = block.get_infrastructure_list()
            self.blocks = np.append(self.blocks, block)
            for j in range(0, len(infrastructure_list)):
                s = infrastructure_list[j].strip()
                if 'STATION' in s:
                    station_side = block.get_station_side()
                    self.stations = np.append(self.stations, Station(i, s, station_side))
                elif s == 'RAILWAY CROSSING':
                    self.crossings = np.append(self.crossings, Crossing(i))
                elif 'SWITCH' in s:
                    self.switches = np.append(self.switches, Switch(i, s))
                    b = s.lstrip('SWITCH (').rstrip(')').replace('-', ',').split(',')  # blocks involved in switch
                    for k in range(len(b)):  # adding signals
                        if b.count(b[k]) == 1:
                            self.signals = np.append(self.signals, Signal(b[k]))  # TODO: REFORMAT YARD SWITCHES IN XSL

        # defaults
        self.ticket_sales = 0
        self.environmental_temperature = 74
        self.authority = []
        self.speed = []
        self.trains = []
        self.waysides = []

    def check_data(self):  # update this in future to validate data further
        if len(self.data) == 0:
            print('***\nExiting, Data input is empty\n***')
            exit()
    # is working for initialization but not for setting data

    def get_line_name(self):
        return self.line_name

    def get_num_blocks(self):
        return self.num_blocks

    def get_ticket_sales(self):
        return self.ticket_sales

    def get_section(self, section_id_start, section_id_end=None):
        pass

    def get_blocks(self):
        return self.blocks

    def set_data(self, file_name: str):
        pass  # object completely reinitialized

    def set_block_occupancy(self, block_id: int, occupancy: bool):
        self.blocks[block_id-1] = occupancy

    def get_environmental_temperature(self):
        return self.environmental_temperature

    def get_stations(self):
        return self.stations

    def get_switches(self):
        return self.switches

    def get_crossings(self):
        return self.crossings

    def get_signals(self):
        return self.signals

    # communication w/ other modules

    # setters
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

    def train_spawned(self):
        pass

    def train_presence_changed(self, train_id):
        pass

    def set_disembarking_passengers(self, train_id, disembarking_passengers):
        pass

    # getters
    def get_tc_block_occupancy(self, starting_block: int, ending_block: int):
        result = []
        for i in range(starting_block, ending_block + 1):
            result.append(self.blocks[i].get_occupancy())
        return result

    def get_tm_authority(self, train_id: int) -> list[int]:
        return self.authority[self.trains[train_id].get_block_id()]

    def get_tm_speed(self, train_id: int) -> list[float]:
        return self.speed[self.trains[train_id].get_block_id()]

    def get_tm_beacon(self, train_id: int) -> str:
        return self.blocks[self.trains[train_id].get_block_id()].get_beacon_msg()

    def get_tm_grade(self, train_id: int) -> int:
        return self.blocks[self.trains[train_id].get_block_id()].get_grade()

    def get_tm_elevation(self, train_id: int) -> float:
        return self.blocks[self.trains[train_id].get_block_id()].get_elevation()

    def get_tm_underground_status(self, train_id: int) -> bool:
        return self.blocks[self.trains[train_id].get_block_id()].get_underground()

    def get_tm_embarking_passengers(self, train_id: int) -> int:  # relies on stations being first entry in table
        return self.blocks[self.trains[train_id].get_block_id()].get_infrastructure()[0].get_embarking()

    def get_ctc_ticket_sales(self):
        pass


# temp main
t = TrackModel('Green Line.xlsx')
