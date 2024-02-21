import time

#class CTCTime:
def get_current_time()->time.struct_time:
    return time.localtime()
    
def get_current_time_hh_mm()->int:
    current_time = get_current_time()
    h = str(current_time.tm_hour)
    m = str(current_time.tm_min)

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
    h = str(current_time.tm_hour)
    m = str(current_time.tm_min)

    if(len(h) == 1):
        hh = "0" + h
    else:
        hh = h
    
    if(len(m) == 1):
        mm = "0" + m
    else:
        mm = m

    return hh + mm