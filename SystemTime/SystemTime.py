from threading import Timer
import threading
import time as python_time


class SystemTime:
    def __init__(self):
        self.__sys_time:float = python_time.time()
        self.__scale:float = 1
        self.__update_interval:float = 0.1

        self.__timer_flag = True
        self.__time_update_thread = threading.Thread(target=self.__update_time)
        self.__time_update_thread.start()

    def __del__(self):
        self.__timer_flag = False
        self.__time_update_thread.join()
    
    def time(self)->float:
        return self.__sys_time
    
    def set_multiplier(self, multiplier:float)->None:
        self.__scale = multiplier
        self.__update_interval = 1.0 / (10 * self.__scale)

    def __update_time(self):

        while(self.__timer_flag):
            python_time.sleep(self.__update_interval)
            self.__sys_time += 0.1 # 1 s precison
