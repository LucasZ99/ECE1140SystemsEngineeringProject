import numpy as np


class Train:
    def __init__(self, train_id: int):
        self.train_id = train_id  # will match index in our trains list
        self.block_id = 0

    def set_block_id(self, block_id: int):
        self.block_id = block_id  # We will have to implement a linked list that is updated every time a switch toggled

    def get_train_id(self):
        return self.train_id

    def get_block_id(self):
        return self.block_id


class Station:
    def __init__(self, block_id: int, s: str, station_side: str):
        self.block_id = block_id
        self.name = s
        self.side = station_side
        self.embarking = 0
        self.disembarking = 0
        self.ticket_sales = 0

    # getters
    def get_block_id(self):
        return self.block_id

    def get_name(self):
        return self.name

    def get_side(self):
        return self.side

    def get_embarking(self):
        return self.embarking

    def get_disembarking(self):
        return self.disembarking

    def get_ticket_sales(self):
        return self.ticket_sales

    # setters
    def set_embarking(self, x: int):
        self.embarking = x

    def set_disembarking(self, x: int):
        self.disembarking = x

    def set_ticket_sales(self, x: int):
        self.ticket_sales = x


class Signal:
    def __init__(self, block_id: int):
        self.block_id = block_id
        self.value = False  # (F,T) --> (Red, Green)

    def get_block_id(self):
        return self.block_id

    def get_value(self):
        return self.value

    def toggle_value(self):
        self.value = not self.value


class Crossing:
    def __init__(self, block_id):
        self.block_id = block_id
        self.value = False  # (F,T) --> (Inactive, Active)

    # getters
    def get_block_id(self):
        return self.block_id

    def get_value(self):
        return self.value

    # setters
    def toggle_value(self, x: bool):
        self.value = x


class Switch:
    def __init__(self, block_id: int, s: str):
        self.block_id = block_id
        self.value = False  # (F,T) --> (Left, Right)
        self.s = s.lstrip('SWITCH (,').rstrip(')')
        # initialize lights

    # getters
    def get_s(self):
        return self.s

    def get_block_id(self):
        return self.block_id

    def get_value(self):
        return self.value

    # setters
    def toggle_value(self):
        self.value = not self.value


class Block:
    def __init__(self, data):
        # from data
        self.section = data[0]
        self.id = data[1]
        self.length = data[2]
        self.grade = data[3]
        self.speed_lim = data[4]
        self.elevation = data[5]
        self.station_side = data[7]
        # add direction of travel?

        # defaults
        self.occupancy = False
        self.temp = 74
        self.beacon_msg = ''

        # infrastructure & underground status
        self.underground = False
        self.infrastructure_list = []
        if not str(data[6]) == 'nan':
            self.infrastructure_list = data[6].split(';')
            for i in range(0, len(self.infrastructure_list)):
                s = self.infrastructure_list[i].strip()
                if s == 'UNDERGROUND':
                    self.underground = True

        # Beacons
        if not str(data[8]) == 'nan':
            self.beacon_msg = str(data[8])

    # getters
    def get_section(self):
        return self.section

    def get_id(self):
        return self.id

    def get_length(self):
        return self.length

    def get_grade(self):
        return self.grade

    def get_speed_lim(self):
        return self.speed_lim

    def get_elevation(self):
        return self.elevation

    def get_occupancy(self):
        return self.occupancy

    def get_temp(self):
        return self.temp

    def get_beacon_msg(self):
        return self.beacon_msg

    def get_underground(self):
        return self.underground

    def get_station_side(self):
        return self.station_side

    def get_infrastructure_list(self):
        return self.infrastructure_list

    # setters
    def toggle_occupancy(self):
        self.occupancy = not self.occupancy

    def set_temp(self, x: int):
        self.temp = x

#

