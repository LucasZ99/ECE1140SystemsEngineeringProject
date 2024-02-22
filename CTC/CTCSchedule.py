from PyQt6.QtCore import QObject, QTime
from time import struct_time
from CTC.CTCTime import *

class Train:
    def __init__(self, number:int, line:int, destination:str, departure_time:QTime, route:list[str]):
        self.number = number
        self.line = line
        self.destination = destination
        self.departure_time = departure_time
        # self.arrival_time = arrival_time
        self.route = route

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
        print("Train Scheduled.")
        print("Departure time: ", train.departure_time)
        self.dispatch_queue.append(train)
        self.dispatch_queue.sort(key=lambda train:train.departure_time)
        self.current_train_number += 1

    # def get_trains_to_dispatch(self, time:struct_time)->list[Train]:
    #     dispatch_now_list:list[Train] = []
        
    #     for train in self.dispatch_queue:
    #         if train.departure_time == get_current_time_hh_mm():
    #             dispatch_now_list.append(train)

    #     return dispatch_now_list
    
    def get_schedule(self)->list[Train]:
        return self.dispatch_queue
    
    def get_trains_to_dispatch(self, current_time:QTime)->list[Train]:
        trains_to_dispatch = []
        for train in self.dispatch_queue:
            if (train.departure_time.hour() == current_time.hour() and
                    train.departure_time.minute() == current_time.minute()):
                print("Train added to dispatch list")
                trains_to_dispatch.append(train)

        return trains_to_dispatch

    def dispatch_trains(self, current_time:QTime)->list[Train]:
        dispatch_list = self.get_trains_to_dispatch(current_time)[:]
        for train in dispatch_list:
            self.dispatch_queue.remove(train)
        return dispatch_list

    # def import_schedule(self):
