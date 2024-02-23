#import pyfirmata
import pyfirmata2
import time



global board
board = pyfirmata2.ArduinoMega('COM7')

#mini classes---------------------------------------------------------
class LED_PyF():
    def __init__(self,Pin):
        self.item = board.digital[Pin]
        self.item.write(0)#start with LOW
    def write(self,writing):
        #print("O:",writing)
        self.item.write(int(writing))
    
class BTN_PyF():
    def __init__(self,Pin):
        self.item = board.get_pin('d:'+str(Pin)+':i')
        self.item.enable_reporting()
    def read(self):
        if self.item.read() == None or self.item.read() <0.85: return 0
        else: return 1
    
class POT_PyF():
    def __init__(self,Pin,start=0,end=100):
        self.start=start;self.end=end#read items
        self.item = board.analog[Pin]
        self.item.enable_reporting()
    def read(self):
        #print("I2:",self.item.read() )
        if self.item.read() == None: return 0
        else: return round( ( (self.item.read())*(self.end-self.start) )+self.start,2)
    
#arduino verison of HW UI----------------------------------------------
class HW_UI_JEB382_PyFirmat():
    def __init__(self,in_Driver_arr,in_TrainModel_arr):
        self.Driver_arr = in_Driver_arr
        self.TrainModel_arr = in_TrainModel_arr
        self.init_clk = time.time()
        
        #input sets
        self.TCK_Kp     = POT_PyF(0)
        self.TCK_Ki     = POT_PyF(1)
        self.TCK_CmdSpd = POT_PyF(2)
        self.TCK_Temp   = POT_PyF(3)
        self.BTN_CabnLgt = BTN_PyF(40)
        self.BTN_HeadLgt = BTN_PyF(41)
        self.BTN_Door_L  = BTN_PyF(42)
        self.BTN_Door_R  = BTN_PyF(43)
        self.BTN_EBRK    = BTN_PyF(44)
        self.BTN_SBRK    = BTN_PyF(45)
        self.BTN_DisPaEB = BTN_PyF(46)
        
        #LEDs
        self.LED_CabnLgt    = LED_PyF(22)
        self.LED_HeadLgt    = LED_PyF(23)
        self.LED_Door_L     = LED_PyF(24)
        self.LED_Door_R     = LED_PyF(25)
        self.LED_Pass_EB    = LED_PyF(26)
        self.LED_Track_Circ = LED_PyF(27)
        self.LED_Stat_Side2 = LED_PyF(28)
        self.LED_Stat_Side1 = LED_PyF(29)
        self.LED_Sig_Fail   = LED_PyF(30)
        self.LED_Eng_Fail   = LED_PyF(31)
        self.LED_Brk_Fail   = LED_PyF(32)
    
    def updateOuts(self):
        if int(time.time() - self.init_clk)%3 == 0:
            self.Driver_arr[3] = 0
            self.Driver_arr[6] = 0
            self.Driver_arr[7] = 0
            self.Driver_arr[8] = 0
            self.Driver_arr[9] = 0
            self.Driver_arr[10]= 0
        else:
            self.Driver_arr[3] = self.BTN_CabnLgt.read()
            self.Driver_arr[6] = self.BTN_Door_L.read()
            self.Driver_arr[7] = self.BTN_Door_R.read()
            self.Driver_arr[8] = self.BTN_EBRK.read()
            self.Driver_arr[9] = self.BTN_SBRK.read()
            self.Driver_arr[10]= self.BTN_DisPaEB.read()
        '''#self.Driver_arr[0] = self.TCK_Kp.read()
        #self.Driver_arr[1] = self.TCK_Ki.read()
        #self.Driver_arr[2] = self.TCK_CmdSpd.read()
        self.Driver_arr[3] = self.BTN_CabnLgt.read()
        #self.Driver_arr[4] = self.BTN_HeadLgt.read()
        #self.Driver_arr[5] = self.TCK_Temp.read()
        self.Driver_arr[6] = self.BTN_Door_L.read()
        self.Driver_arr[7] = self.BTN_Door_R.read()
        self.Driver_arr[8] = self.BTN_EBRK.read()
        self.Driver_arr[9] = self.BTN_SBRK.read()
        self.Driver_arr[10]= self.BTN_DisPaEB.read()'''
        
        self.Driver_arr[0] = self.TCK_Kp.read()
        self.Driver_arr[1] = self.TCK_Ki.read()
        self.Driver_arr[2] = self.TCK_CmdSpd.read()
        self.Driver_arr[5] = self.TCK_Temp.read()
        #board.send_sysex(pyfirmata2.STRING_DATA, pyfirmata2.util.str_to_two_byte_iter(self.TrainModel_arr[0:20]))
    
    def updateDisplay(self):
        self.LED_CabnLgt   .write(self.BTN_CabnLgt.read())
        self.LED_HeadLgt   .write(self.BTN_HeadLgt.read())
        self.LED_Door_L    .write(self.BTN_Door_L .read())
        self.LED_Door_R    .write(self.BTN_Door_R .read())
        self.LED_Pass_EB   .write( bool(self.TrainModel_arr[5]) and not bool(self.Driver_arr[10]) )
        self.LED_Track_Circ.write( bool(self.TrainModel_arr[6]) )
        self.LED_Stat_Side2.write( self.TrainModel_arr[5]>1 ) #_x 2,3
        self.LED_Stat_Side1.write( self.TrainModel_arr[5]%2 ) #x_ 1,3
        self.LED_Sig_Fail  .write( bool(self.TrainModel_arr[-4]) )
        self.LED_Eng_Fail  .write( bool(self.TrainModel_arr[-3]) )
        self.LED_Brk_Fail  .write( bool(self.TrainModel_arr[-2]) )
        
import time
        
if __name__ == "__main__":
    Arduino = True
    
    main_Driver_arr = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    main_TrainModel_arr = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0,0.0,
                           "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"]
    w = HW_UI_JEB382_PyFirmat(main_Driver_arr,main_TrainModel_arr)
    
    it = pyfirmata2.util.Iterator(board)  
    it.start()
    #a = board.analog[13]
    #a.mode = pyfirmata2.INPUT
    #BTN_CabnLgt = BTN_PyF(8)
    #TCK_Kp = POT_PyF(0)
    while True:
        w.updateOuts()
        w.updateDisplay()
        print(w.Driver_arr)
        #print(a.read())
        #print(BTN_CabnLgt.read())
        #print(TCK_Kp.read())
        #time.sleep(1)
        