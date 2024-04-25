import pandas as pd
import numpy as np
import sys
import random
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication
import time
import openpyxl
from Track_Model.TrackModelSignals import TrackModelSignals as signals


class TrackModel(QObject):
    # external signals
    # new_block_occupancy_signal = pyqtSignal(list)
    # new_ticket_sales_signal = pyqtSignal(int)
    # internal signals (to UI)
    refresh_ui_signal = pyqtSignal()
    map_add_train_signal = pyqtSignal()
    map_move_train_signal = pyqtSignal(int, int)

    def __init__(self, file_name):
        super().__init__()
        # d = pd.read_excel(file_name, header=None)  # We will also load our header row, and block IDs will map to index
        # self.data = d.to_numpy()
        # self.check_data()
        start = time.time()
        self.data = self.set_data(file_name)
        # self.output_data_as_excel()
        end = time.time()
        print(f'set_data time = {end - start}')
        # self.output_data_as_excel()
        self.line_name = self.data[0, 0]
        self.num_blocks = len(self.data) - 1
        self.ticket_sales = 0
        self.environmental_temperature = 74
        # giving random embarking num and ticket sales
        for i in range(0, self.num_blocks):
            if self.data[i, 16] == 0:
                self.data[i, 16] = random.randint(1, 100)
                self.data[i, 17] = random.randint(1, int(self.data[i, 16]))
        self.authority_dict = {}
        self.speed_dict = {}

        self.train_dict_relative = {}
        self.train_dict = {}
        self.train_dict_meters = {}
        self.train_count = 0
        self.remove_train = -1

        self.closed_blocks = {i: False for i in range(1, 151)}


        # hardcoded
        # Step 1: 12 to 1
        path_12_to_1 = list(range(12, 0, -1))
        # Step 2: 13 to 57
        path_13_to_57 = list(range(13, 59))
        # Step 3: 0
        # Step 4: 63 to 100
        path_62_to_100 = list(range(62, 101))
        # Step 5: 85 to 77
        path_85_to_77 = list(range(85, 76, -1))
        # Step 6: 101 to 150
        path_101_to_150 = list(range(101, 151))
        # Step 7: 28 to 13
        path_28_to_13 = list(range(28, 12, -1))
        # Combining all paths, with explicit jumps where needed
        self.full_path = (path_62_to_100 + path_85_to_77 + path_101_to_150 + path_28_to_13 + path_12_to_1 +
                          path_13_to_57)
        # print(self.full_path)
        # cumulative distance (train_dict_meters reference)
        self.cumulative_distance = self.full_path.copy()
        cumulative_distance = 0
        for i in range(0, len(self.cumulative_distance)):
            cumulative_distance += int(self.data[self.full_path[i], 3])
            self.cumulative_distance[i] = cumulative_distance
        # print(self.cumulative_distance)

        # Connect Signals to Slots:
        self.signals = signals
        self.signals.get_data_signal.connect(self.get_data)
        self.signals.get_block_info_signal.connect(self.get_block_info)
        self.signals.get_train_dict_signal.connect(self.get_train_dict)
        self.signals.get_full_path_signal.connect(self.get_full_path)

    def get_train_dict(self):
        self.signals.send_train_dict_signal.emit(self.train_dict)
        return self.train_dict

    def get_full_path(self):
        self.signals.send_full_path_signal.emit(self.full_path)
        return self.full_path

    def get_data(self):
        self.signals.send_data_signal.emit(self.data)
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

    # long runtimes
    def set_data(self, file_name):
        start = time.time()
        d = pd.read_excel(file_name,
                          header=None)  # We will also load our header row, and block IDs will map to index
        end = time.time()
        print(f'pandas read time = {end-start}')
        data = d.to_numpy()
        end = time.time()
        print(f'pandas time = {end-start}')
        start = time.time()
        false_col = np.full((data.shape[0], 1), False, dtype=bool)
        temp = np.full((data.shape[0], 1), 74, dtype=int)
        new_data = np.hstack((data[:, 0:7], np.copy(false_col)))
        new_data = np.hstack((new_data[:, 0:8], temp))
        new_data = np.hstack((new_data, data[:, 7:]))
        nan_array = np.full((data.shape[0], 1), np.nan, dtype=object)
        new_data = np.hstack((new_data, nan_array))
        new_data = np.hstack((new_data, np.copy(false_col)))
        new_data = np.hstack((new_data, np.copy(false_col)))
        new_data = np.hstack((new_data, np.copy(false_col)))
        new_data = np.hstack((new_data, np.copy(nan_array)))
        new_data = np.hstack((new_data, np.copy(nan_array)))
        new_data = np.hstack((new_data, np.copy(nan_array)))
        new_data = np.hstack((new_data, np.copy(nan_array)))
        new_data = np.hstack((new_data, np.copy(false_col)))
        new_data = np.hstack((new_data, np.copy(nan_array)))
        new_data = np.hstack((new_data, np.copy(nan_array)))
        end = time.time()
        print(f'hstack time = {end-start}')
        # initialize signals from switch info
        start = time.time()
        for i in range(1, new_data.shape[0]):
            inf_list = str(new_data[i, 9]).lower().split(';')
            for s in inf_list:
                if 'switch' in s:
                    s = s.lstrip('switch (,').rstrip(')')
                    num_list = s.replace(',', '-').replace(' ', '').split('-')
                    unique, counts = np.unique(num_list, return_counts=True)
                    num_dict = dict(zip(unique, counts))
                    for n in unique:
                        num = int(n)
                        if num_dict[n] == 1:
                            new_data[num, 21] = False
            if 'station' in str(new_data[i, 9]).lower():
                new_data[i, 12] = False
                new_data[i, 16] = 0
                new_data[i, 17] = 0
                new_data[i, 18] = 0
                if i != 0:
                    new_data[i - 1, 12] = False
                if i != new_data.shape[0] - 2:
                    new_data[i + 1, 12] = False
            if 'underground' in str(new_data[i, 9]).lower():
                new_data[i, 20] = True
            if 'switch' in str(new_data[i, 9]).lower():
                new_data[i, 19] = False
            if 'railway crossing' in str(new_data[i, 9]).lower():
                new_data[i, 22] = False
        end = time.time()
        print(f'loops time = {end-start}')

        new_data[0, 7] = 'Block Occupancy'
        new_data[0, 8] = 'Temperature'
        new_data[0, 12] = 'Heaters'
        new_data[0, 13] = 'Power Failure'
        new_data[0, 14] = 'Track Circuit Failure'
        new_data[0, 15] = 'Broken Rail Failure'
        new_data[0, 16] = 'Ticket Sales'
        new_data[0, 17] = 'Embarking'
        new_data[0, 18] = 'Disembarking'
        new_data[0, 19] = 'Switch Values'
        new_data[0, 20] = 'Underground Status'
        new_data[0, 21] = 'Signal Values'
        new_data[0, 22] = 'RxR Values'

        # set empty beacon column
        for i in range(1, new_data.shape[0]):
            if str(new_data[i, 11]) == 'nan':
                new_data[i, 11] = '0' * 128
        return new_data

    def output_data_as_excel(self):
        # Convert the NumPy array to a pandas DataFrame
        df = pd.DataFrame(self.data)

        # Define the filename for the Excel file
        excel_filename = "testing_output.xlsx"

        # Export the DataFrame to an Excel file
        df.to_excel(excel_filename, index=False,
                    header=False)  # index=False, header=False to exclude row and column labels

        print("Array data has been exported to:", excel_filename)

    def set_block_occupancy(self, block: int, occupancy: bool):
        # print(block)
        self.data[block, 7] = occupancy

    def check_data(self):  # update this in future to validate data further
        if len(self.data) == 0:
            print('***\nExiting, Data input is empty\n***')
            exit()

    def set_env_temperature(self, temperature):
        self.environmental_temperature = temperature
        self.data[1:, 8] = temperature

    def get_env_temperature(self, temperature):
        return self.environmental_temperature

    def set_heaters(self, value):  # For now acts instantaneously, but may need to stimulate heating over time
        heaters = self.data[1:, 12]
        if value:
            heaters[heaters == 0] = 1
        else:
            heaters[heaters == 1] = 0
        for i in range(0, len(heaters)):
            if heaters[i] == 1:
                self.data[i + 1, 8] = 90

    def set_power_failure(self, block, value):
        self.data[block, 13] = value
        self.set_occupancy_from_failures(block)

    def set_track_circuit_failure(self, block, value):
        self.data[block, 14] = value
        self.set_occupancy_from_failures(block)

    def set_broken_rail_failure(self, block, value):
        self.data[block, 15] = value
        self.set_occupancy_from_failures(block)

    def set_occupancy_from_failures(self, block):
        p = self.data[block, 13]
        tc = self.data[block, 14]
        br = self.data[block, 15]
        if p or tc or br:
            self.set_block_occupancy(block, True)
        else:
            self.set_block_occupancy(block, False)

    def set_occupancy_from_train_presence(self):
        # set all occupancy false
        self.data[1:, 7] = np.full((self.data.shape[0]-1), False, dtype=bool)

        # Failures
        for i in range(0, self.num_blocks):
            self.set_occupancy_from_failures(i)

        # Trains
        # key = train id, value = block id
        for key in self.train_dict:
            self.set_block_occupancy(self.train_dict[key], True)

        # Closed Blocks
        # for key, value in self.closed_blocks.items():
        #     if value:
        #         self.set_block_occupancy(key, True)

    # communication to ui

    def refresh_ui(self):
        self.refresh_ui_signal.emit()

    #
    #
    # Communication for other modules
    #
    #

    # RECEIVING (setters)

    # track controller

    def update_authority(self, authority: list[int]):
        self.authority = authority
        print("self authority updated in track model")

    def update_speed(self, speed: list[float]):
        self.speed = speed
        print("self speed updated in track model")

    def toggle_switch(self, block_id: int):
        self.data[block_id, 19] = not self.data[block_id, 19]

    def toggle_signal(self, block_id: int):
        self.data[block_id, 21] = not self.data[block_id, 21]

    def toggle_crossing(self, block_id: int):
        self.data[block_id, 22] = not self.data[block_id, 22]

    def open_block(self, block_id: int):
        self.set_power_failure(block_id, False)
        self.set_track_circuit_failure(block_id, False)
        self.set_broken_rail_failure(block_id, False)

    def close_block(self, block_id: int):
        self.set_power_failure(block_id, True)
        self.set_track_circuit_failure(block_id, True)
        self.set_broken_rail_failure(block_id, True)

    # train model

    def train_spawned(self):
        print("train spawned from track model")
        self.train_count += 1
        self.train_dict_relative[self.train_count] = 0
        self.train_dict[self.train_count] = self.full_path[0]
        self.train_dict_meters[self.train_count] = 0
        print(f'new train spawned, train_count = {self.train_count}')
        self.signals.map_add_train_signal.emit()  # refresh map ui

    # def train_presence_changed(self, train_id: int):
    #     if self.train_dict_relative[train_id] >= 170:
    #         # train goes back to yard
    #         print('train going back to yard...')
    #         self.train_count -= 1
    #         del self.train_dict_relative[train_id]
    #         del self.train_dict[train_id]
    #     else:
    #         self.train_dict_relative[train_id] += 1
    #         self.train_dict[train_id] = self.full_path[self.train_dict_relative[train_id]]
    #         self.set_occupancy_from_train_presence()
    #         print(f'train {train_id} moved to {self.train_dict[train_id]}')

    def set_remove_train(self, train_id):
        self.remove_train = train_id

    def get_remove_train(self):
        return self.remove_train

    def update_delta_x_dict(self, delta_x_dict):
        print('train dict relative:')
        for key, val in self.train_dict_relative.items():
            print(f'key = {key}')
            print(f'val = {val}')
            print()
        print('train dict relative:')
        for key, val in self.train_dict_relative.items():
            print(f'key = {key}')
            print(f'val = {val}')
            print()
        self.remove_train = -1
        # meters
        for key, value in delta_x_dict.items():
            self.train_dict_meters[key] = value
        # relative based meters
        for key, value in self.train_dict_meters.items():
            if value > self.cumulative_distance[self.train_dict_relative[key]]:
                self.train_dict_relative[key] += 1
                self.signals.map_move_train_signal.emit(key, self.full_path[self.train_dict_relative[key]])  # refresh map ui
            if self.train_dict_relative[key] > 170:  # check if we should remove trains
                self.remove_train = key
            print(f'train_dict_relative[key] = {self.train_dict_relative[key]}')
        # actual block based on relative
        for key, value in self.train_dict_relative.items():
            self.train_dict[key] = self.full_path[value]
        self.set_occupancy_from_train_presence()
        # remove trains
        if self.remove_train != -1:
            del self.train_dict_meters[self.remove_train]
            del self.train_dict_relative[self.remove_train]
            del self.train_dict[self.remove_train]
            self.train_count -= 1

    def set_disembarking_passengers(self, station_id: int, disembarking_passengers: int):
        self.data[station_id, 21] = disembarking_passengers

    # SENDING (getters)

    # track controller

    def get_occupancy_list(self):
        return self.data[1:, 7].tolist()

    def update_infrastructure(self, switch_changed_indexes, signal_changed_indexes, rr_crossing_indexes, toggle_block_indexes):
        print('TRACK MODEL: update_infrastructure called')
        print(f'TRACK MODEL: toggle_block_indexes = {toggle_block_indexes}')
        for index, val in switch_changed_indexes:
            self.data[index, 19] = val
        for index, val in signal_changed_indexes:
            self.data[index, 21] = val
        for index, val in rr_crossing_indexes:
            self.data[index, 22] = val
        for block_id in toggle_block_indexes:  # FOR RN Just toggles occupancy
            if self.closed_blocks[block_id]:
                self.closed_blocks[block_id] = False
                self.open_block(block_id)
            else:
                self.closed_blocks[block_id] = True
                self.close_block(block_id)

    # new UI getters
    def get_block_info(self, block_id):
        # # length, grade, speed lim, elevation
        # self.data[block_id, (3, 4, 5, 6)]
        # # occupied, beacon, track heated, underground
        # self.data[block_id, (7, 11, 12, 20)]
        # # failures 13 14 15
        # self.data[block_id, (13, 14, 15)]
        # TODO: add station info
        # self.data[block_id, ]
        # print(self.data[block_id, (3, 4, 5, 6, 7, 11, 12, 20, 13, 14, 15)])
        self.signals.send_block_info_signal.emit(self.data[block_id, (3, 4, 5, 6, 7, 11, 12, 20, 13, 14, 15, 19, 21, 22)])

    def get_block_info_for_train(self, train_id):
        block = self.train_dict[train_id]
        return self.data[block, (4, 6, 20, 11)].tolist()
        # grade elevation underground_status beacon

    def update_authority_and_safe_speed(self, authority_safe_speed_update):
        for i in range(0, len(authority_safe_speed_update)):
            block_id = authority_safe_speed_update[i][0]
            authority = authority_safe_speed_update[i][1]
            safe_speed = authority_safe_speed_update[i][2]
            self.authority_dict[block_id] = authority
            self.speed_dict[block_id] = safe_speed

    def get_authority_dict(self):
        return self.authority_dict

    def get_speed_dict(self):
        return self.speed_dict

# temp main
# t = TrackModel('Blue Line.xlsx')
# print(t.get_data())
