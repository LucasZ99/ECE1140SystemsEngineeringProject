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

        self.blocks = np.array([])
        for i in range(1, self.num_blocks + 1):
            self.blocks = np.append(self.blocks, Block(self.data[i, 1:10]))
        # defaults
        self.ticket_sales = 0
        self.environmental_temperature = 74
        self.authority = []
        self.speed = []
        self.trains = []

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

    def get_environmental_temperature(self):
        return self.environmental_temperature

    def get_speed(self):
        return self.speed

    def get_authority(self):
        return self.authority

    def get_blocks(self):
        return self.blocks

    # communication w/ other modules
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

    def get_tm_embarking_passengers(self, train_id: int) -> int:
        block_infrastructure = self.blocks[self.trains[train_id].get_block_id()].get_infrastructure()

    # ctc
    def get_ctc_ticket_sales(self):
        pass


# temp main
t = TrackModel('Green Line.xlsx')
print(t.get_blocks[])

