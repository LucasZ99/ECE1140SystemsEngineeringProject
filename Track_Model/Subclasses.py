import numpy as np


class Station:
    def __init__(self, block_id, s, station_side):
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
    def __init__(self, block_id):
        self.block_id = block_id
        self.value = False  # (F,T) --> (Red, Green)


class Crossing:
    def __init__(self, block_id, s):
        self.block_id = block_id
        self.value = False  # (F,T) --> (Inactive, Active)

    # getters
    def get_block_id(self):
        return self.block_id

    def get_value(self):
        return self.value

    # setters
    def set_value(self, x: bool):
        self.value = x


class Switch:
    def __init__(self, block_id, s):
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
    def set_value(self, x: bool):
        self.value = x


class Block:
    def __init__(self, data):
        # from data
        self.section = data[0]
        self.id = self.section = data[1]
        self.length = data[2]
        self.grade = data[3]
        self.speed_lim = data[4]
        self.elevation = data[5]
        # add direction of travel?

        # defaults
        self.occupancy = 0
        self.temp = 74
        self.beacon_msg = ''

        # infrastructure & underground status
        self.underground = False
        self.infrastructure = np.array([], dtype=object)
        if not str(data[6]) == 'nan':
            infrastructure_list = data[6].split(';')
            for i in range(0, len(infrastructure_list)):
                s = infrastructure_list[i].strip()
                if 'STATION' in s:
                    station_side = data[7]
                    self.infrastructure = np.append(self.infrastructure, Station(self.id, s, station_side))
                elif s == 'RAILWAY CROSSING':
                    self.infrastructure = np.append(self.infrastructure, Crossing(self.id, s))
                elif 'SWITCH' in s:
                    self.infrastructure = np.append(self.infrastructure, Switch(self.id, s))
                    b = s.replace('-', ',').split(',')  # blocks involved in switch
                    for j in range(len(b)):  # adding signals
                        if b.count(b[j]) == 1:
                            self.infrastructure = np.append(self.infrastructure, Signal(b[j]))
                elif s == 'UNDERGROUND':
                    self.underground = True

        # Beacons
        if not str(data[8]) == 'nan':
            self.beacon_msg = str(data[8])


# testing:


