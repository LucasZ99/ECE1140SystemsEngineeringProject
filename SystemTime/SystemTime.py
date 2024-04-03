from threading import Timer, Thread
import time as python_time
from PyQt6.QtCore import QObject, pyqtSignal


class SystemTime(QObject):
    update_time_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__scale: float = 1

        init_time = python_time.time()
        # print(init_time)
        self.__sys_time = init_time
        self.__update_interval = 1
        self.__timer_flag = 1

        self.__time_update_thread = Thread(target=self.update_time)
        self.__time_update_thread.start()

    def update_time(self):
        while self.__timer_flag:
            start_time = python_time.time()

            while True:
                if python_time.time() >= start_time + self.__update_interval:
                    break

            self.__sys_time += self.__update_interval
            self.update_time_signal.emit()

    def __del__(self):
        self.__timer_flag.value = 0
        self.__time_update_thread.join()

    def time(self) -> float:
        sys_time = self.__sys_time
        return sys_time

    def set_multiplier(self, multiplier: float) -> None:
        self.__scale = multiplier
        self.__update_interval = 1.0 / (1 * self.__scale)
        print(f"multiplier set: {multiplier}")
