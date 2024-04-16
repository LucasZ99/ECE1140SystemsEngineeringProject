from datetime import datetime
from threading import Timer, Thread
import time as python_time
from PyQt6.QtCore import QObject


def time_to_str(t: float):
    return python_time.strftime("%H:%M:%S", python_time.localtime(t))


class SystemTime(QObject):
    time_paused = False
    scale: float = 1

    last_captured_real_time = python_time.time()
    sys_time = last_captured_real_time
    print("SystemTime Object Created")


def time() -> float:
    # For any time t, the time system elapsed since the last real time captured is the change in time * scale
    if not SystemTime.time_paused:
        real_time_elapsed = python_time.time() - SystemTime.last_captured_real_time
        SystemTime.last_captured_real_time = python_time.time()
        delta_sys_time = real_time_elapsed * SystemTime.scale
        SystemTime.sys_time = SystemTime.sys_time + delta_sys_time
    return SystemTime.sys_time


def play():
    SystemTime.time_paused = False


def pause():
    time()
    SystemTime.time_paused = True


def set_multiplier(multiplier: float) -> None:
    # update system time
    time()

    SystemTime.scale = multiplier
    print(f"multiplier set: {multiplier}")
    print("SystemTime started")
