from CTC.Train import Train
from SystemTime import SystemTime

class CTCSchedule:
    def __init__(self, system_time:SystemTime):
        self.current_train_number = 1
        self.train_list:list[Train] = []

        self.system_time = system_time

    """
    Returns the 
    """
    def get_next_train_number(self)->int:
        return self.current_train_number

    """
    Add a train to the queue of trains to be dispatched and sort the trains by departure time.
    """
    def schedule_train(self, train:Train)->None:
        print("Train Scheduled.")
        print("Departure time: ", train.departure_time())
        self.train_list.append(train)
        self.train_list.sort(key=lambda train:train.departure_time())
        self.current_train_number += 1

    # def get_trains_to_dispatch(self, time:struct_time)->list[Train]:
    #     dispatch_now_list:list[Train] = []
        
    #     for train in self.dispatch_queue:
    #         if train.departure_time == get_current_time_hh_mm():
    #             dispatch_now_list.append(train)

    #     return dispatch_now_list
    
    def get_schedule(self)->list[Train]:
        return self.train_list
    
    def get_trains_to_dispatch(self)->list[Train]:
        trains_to_dispatch = []
        for train in self.train_list:
            # round to this current minute 
            if (round(train.departure_time(), -2) == round(self.system_time.time(), -2)):
                print("Train added to dispatch list")
                trains_to_dispatch.append(train)

        return trains_to_dispatch

    def dispatch_trains(self)->list[Train]:
        dispatch_list = self.get_trains_to_dispatch()[:]
        for train in dispatch_list:
            self.train_list.remove(train)
        return dispatch_list

    # def import_schedule(self):
