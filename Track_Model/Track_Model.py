import pandas as pd
import numpy as np
import sys


class TrackModel:
    def __init__(self, file_name):
        d = pd.read_excel(file_name, header=None)  # We will also load our header row, and block IDs will map to index
        self.data = d.to_numpy()
        self.check_data()
        self.line_name = self.data[0, 0]
        self.num_blocks = len(self.data)
        self.ticket_sales = 0

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

    def set_block_occupancy(self, block_id, occupancy):
        self.data[block_id, 10] = occupancy

    def check_data(self):  # update this in future to validate data further
        if len(self.data) == 0:
            print('***\nExiting, Data input is empty\n***')
            exit()
    # is working for initialization but not for setting data

    def get_block_table(self, section_id):
        n = len(self.get_section(section_id))
        print(n)
        print(self.get_section(section_id))
        block_table = np.empty(shape=(n + 1, 7), dtype=object)
        # everything comes from data except occupancy (from train model) and temp (from temp controls)
        # but even those values will be stored in our data
        block_table[0, :] = ['Block ID', 'Length', 'Grade', 'Speed Limit', 'Elevation', 'Occupancy', 'Temp']
        block_table[1:n+1, 0:7] = self.get_section(section_id)[:, 2:9]
        print()
        print(block_table)
        print(block_table.shape)
        return block_table




