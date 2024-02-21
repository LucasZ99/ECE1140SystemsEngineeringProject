from PyQt6.QtCore import QObject
from time import struct_time
from CTC.CTCTime import *

class Train:
    def __init__(self, number:int, line:str, destination:str, departure_time:str, arrival_time:str, stops:list[str]):
        self.number = number
        self.line = line
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.stops = stops

class CTCSchedule:
    def __init__(self):
        self.current_train_number = 1
        self.dispatch_queue:list[Train] = []

    """
    Returns the 
    """
    def get_next_train_number(self):
        return self.current_train_number

    """
    Add a train to the queue of trains to be dispatched and sort the trains by departure time.
    """
    def schedule_train(self, train:Train)->None:
        self.dispatch_queue.append(train)
        self.dispatch_queue.sort(key=lambda train:train.departure_time)
        self.current_train_number += 1

    def get_trains_to_dispatch(self, time:struct_time)->list[Train]:
        dispatch_now_list:list[Train] = []
        
        for train in self.dispatch_queue:
            if train.departure_time == get_current_time_hh_mm():
                dispatch_now_list.append(train)

        return dispatch_now_list


    # def import_schedule(self):
