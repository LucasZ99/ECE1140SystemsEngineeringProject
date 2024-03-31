from threading import Timer
from multiprocessing import Process, Value
import time as python_time

from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal

time_updated_signal = pyqtSignal(float)

def update_time(timer_flag, update_interval, sys_time):
    sys_time_float = float(sys_time.value)

    while timer_flag.value:
        # python_time.sleep(update_interval.value)

        start_time = python_time.time()

        while True:
            if python_time.time() >= start_time + update_interval.value:
                break
        sys_time_float = sys_time_float + 0.1
        # print("time updated %f", sys_time_float)
        sys_time.value = sys_time_float  # 0.1 s precison

class SystemTime(QObject):

    update_time_to_ui_signal = pyqtSignal(float)
    def __init__(self):
        super().__init__()
        self.__scale: float = 1

        init_time = python_time.time()
        # print(init_time)
        self.__sys_time = Value('d', init_time)
        self.__update_interval = Value('d', 0.1)
        self.__timer_flag = Value('i', 1)

        self.__time_update_process = Process(
            target=update_time,
            args=(self.__timer_flag,
                  self.__update_interval,
                  self.__sys_time,))

        self.__time_update_process.start()

    def __del__(self):
        self.__timer_flag.value = 0
        self.__time_update_process.join()

    def time(self) -> float:
        # print("On ret: %f", self.__sys_time.value)
        sys_time = self.__sys_time.value
        return sys_time

    def set_multiplier(self, multiplier: float) -> None:
        self.__scale = multiplier
        self.__update_interval.value = 1.0 / (10 * self.__scale)
        print(f"multiplier set: {multiplier}")

system_time = SystemTime()