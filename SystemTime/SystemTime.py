from threading import Timer, Thread
import time as python_time
from PyQt6.QtCore import QObject


def time_to_str(t: float):
    return python_time.strftime("%H:%m", python_time.localtime(t))


class SystemTime(QObject):
    def __init__(self):
        super().__init__()
        self.__scale: float = 1

        init_time = python_time.time()
        # print(init_time)
        self.__sys_time = init_time
        self.__update_timeout = 0.1
        self.__update_interval = 0.1
        self.__timer_flag = 1

        self.__time_update_thread = Thread(target=self.update_time)
        self.__time_update_thread.start()

    def update_time(self):
        while self.__timer_flag:
            start_time = python_time.time()

            while True:
                if python_time.time() >= start_time + self.__update_timeout:
                    break

            self.__sys_time += self.__update_interval

    def __del__(self):
        self.__timer_flag = 0
        self.__time_update_thread.join()

    def time(self) -> float:
        sys_time = self.__sys_time
        return sys_time

    def play(self):
        pass

    def pause(self):
        pass

    def set_multiplier(self, multiplier: float) -> None:
        self.__scale = multiplier
        self.__update_timeout = self.__update_interval / self.__scale
        print(f"multiplier set: {multiplier}")
