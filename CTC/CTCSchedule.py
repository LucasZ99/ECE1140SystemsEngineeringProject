from CTC.Train import Train
from SystemTime import SystemTime
from SystemTime.SystemTime import time_to_str


class CTCSchedule:
    def __init__(self):
        self.current_train_number = 1
        self.train_list: list[Train] = []

    """
    Returns the next train number to be dispatched to the next
    """
    def get_next_train_number(self) -> int:
        return self.current_train_number

    """
    Add a train to the queue of trains to be dispatched and sort the trains by departure time.
    """
    def schedule_train(self, train: Train) -> None:
        print("Train Scheduled.")
        print("Departure time: ", train.departure_time())
        self.train_list.append(train)
        self.train_list.sort(key=lambda train: train.departure_time())
        self.current_train_number += 1
        print(f"{0} Train {1} scheduled. Departure time: {2}".format(time_to_str(SystemTime.time()), train.id, time_to_str(train.departure_time())))

    # def get_trains_to_dispatch(self, time:struct_time)->list[Train]:
    #     dispatch_now_list:list[Train] = []

    #     for train in self.dispatch_queue:
    #         if train.departure_time == get_current_time_hh_mm():
    #             dispatch_now_list.append(train)

    #     return dispatch_now_list

    def get_schedule(self) -> list[Train]:
        return self.train_list

    def get_trains_to_dispatch(self) -> list[Train]:
        trains_to_dispatch = []
        for train in self.train_list:
            # round to this current minute 
            if round(train.departure_time(), -2) == round(SystemTime.time(), -2):
                print("Train added to dispatch list")
                trains_to_dispatch.append(train)

        return trains_to_dispatch

    """
    Returns a list of trains that are to be dispatched at the time called
    """
    def dispatch_trains(self) -> list[Train]:
        dispatch_list = self.get_trains_to_dispatch()[:]
        for train in dispatch_list:
            self.train_list.remove(train)
        return dispatch_list

    # def import_schedule(self):
