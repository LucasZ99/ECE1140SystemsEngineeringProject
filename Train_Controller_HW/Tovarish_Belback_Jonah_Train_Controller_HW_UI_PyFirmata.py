import pyfirmata



global board
board = pyfirmata.Arduino('YOUR_PORT_HERE')

#mini classes---------------------------------------------------------
class LED_PyF():
    def __init__(self,Pin):
        self.item = board.digital[Pin]
        self.item.write(0)#start with LOW
    def read(self):
        return self.item.read()
    
class BTN_PyF():
    def __init__(self,Pin):
        self.item = board.digital[Pin]
        self.item.mode = pyfirmata.INPUT
    def read(self):
        return self.item.read()
    
class POT_PyF():
    def __init__(self,Pin,start=0,end=100):
        self.start=start;self.end=end#read items
        self.item = board.analog[Pin]
        self.item.enable_reporting()
    def read(self):
        return self.item.read()
    
#arduino verison of HW UI----------------------------------------------
class HW_UI_JEB382_PyFirmat():
    def __init__(self,in_Driver_arr):
        self.TCK_Kp     = POT_PyF(0)
        self.TCK_Ki     = POT_PyF(0)
        self.TCK_CmdSpd = POT_PyF(0)
        self.TCK_Temp   = POT_PyF(0)
        self.BTN_CabnLgt = BTN_PyF(0)
        self.BTN_HeadLgt = BTN_PyF(0)
        self.BTN_Door_L  = BTN_PyF(0)
        self.BTN_Door_R  = BTN_PyF(0)
        self.BTN_EBRK    = BTN_PyF(0)
        self.BTN_SBRK    = BTN_PyF(0)
        self.BTN_DisPaEB = BTN_PyF(0)
        
        
        
        self.out_arr = in_Driver_arr
        self.out_arr[0] = self.TCK_Kp = POT_PyF(0)
        self.out_arr[1] = self.TCK_Ki = POT_PyF(0)
        self.out_arr[2] = self.TCK_CmdSpd = POT_PyF(0)
        self.out_arr[3] = self.BTN_CabnLgt = BTN_PyF(0)
        self.out_arr[4] = self.BTN_HeadLgt = BTN_PyF(0)
        self.out_arr[5] = self.TCK_Temp = POT_PyF(0)
        self.out_arr[6] = self.BTN_Door_L = BTN_PyF(0)
        self.out_arr[7] = self.BTN_Door_R = BTN_PyF(0)
        self.out_arr[8] = self.BTN_EBRK = BTN_PyF(0)
        self.out_arr[9] = self.BTN_SBRK = BTN_PyF(0)
        self.out_arr[10]= self.BTN_DisPaEB = BTN_PyF(0)