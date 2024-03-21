from datetime import date, datetime
import time
from PyQt6.QtCore import QTime

#class CTCTime:
def get_current_time()->datetime:
    return datetime.now()

def get_current_time_qtime()->QTime:
    return QTime.currentTime()
    
def get_current_time_hh_mm()->int:
    current_time = get_current_time()
    h = str(current_time.hour)
    m = str(current_time.minute)

    if(len(h) == 1):
        hh = "0" + h
    else:
        hh = h
    
    if(len(m) == 1):
        mm = "0" + m
    else:
        mm = m

    return int(hh + mm)

def get_current_time_hh_mm_str()->str:
    current_time = get_current_time()
    h = str(current_time.hour)
    m = str(current_time.minute)

    if(len(h) == 1):
        hh = "0" + h
    else:
        hh = h
    
    if(len(m) == 1):
        mm = "0" + m
    else:
        mm = m

    return hh + mm