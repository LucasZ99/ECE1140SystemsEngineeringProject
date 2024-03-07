from pyfirmata2 import ArduinoMega, util, STRING_DATA
import time#replace with shared time module when created and we do integration
from Tovarish_Belback_Jonah_Train_Controller_Testbenchv2 import *#TestBench_JEB382
from PyQt6.QtWidgets import *
#import sys


#commanded speed: Auto/Manual: Turn into Verr, calc power with Kp Ki
#double check array.txt lines up with I/O
#if new indexes, add new LEDs???
#change test bench to new I/O
    #input text box of station name
    #label below displays the output beacon with other given info
#add txt file of look up table
    #one per line?
    #line number is index number, use '.split()'
    #look at excel file
    #python parser?

#fill out rest of updatCalc()

#doors open: cant move


#max auth of 4 (no foresight)
#auth=0: sits there (if station from beacon, open doors, else dont just sit)

#when entering driver, reset to whats the auto array set





global board
board = ArduinoMega('COM7')

#mini classes---------------------------------------------------------
class LED_PyF():
    def __init__(self,Pin):
        self.item = board.get_pin('d:'+str(Pin)+':o')
        self.item.write(0)#start with LOW
    def write(self,writing):
        #print("O:",writing)
        self.item.write(int(writing))
    
class BTN_PyF():
    def __init__(self,Pin):
        self.item = board.get_pin('d:'+str(Pin)+':i')
        self.prev_red=False
        self.outp=False
        #self.item.enable_reporting()
    def read(self):
        #print(self.item.read())
        #if self.item.read() == None or self.item.read() <0.85: return 0
        #else: return 1
        #toggle
        red = self.item.read()
        if red == 1 and red != self.prev_red: self.outp = not self.outp
        self.prev_red = red
        return int(self.outp)
    
class POT_PyF():
    def __init__(self,Pin,start=0,end=100):
        self.start=start;self.end=end#read items
        self.item = board.analog[Pin]
        self.item.enable_reporting()
    def read(self):
        #print("I2:",self.item.read() )
        if self.item.read() == None: return 0
        else: return round( ( (self.item.read())*(self.end-self.start) )+self.start,0)

class DISP_PyF():
    def __init__(self):
        self.laststring = ""
        board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(""))
    def send(self,writing):
        #autobreaks line if over 16 characters, max length is 31 characters
        #autofills with spaces to elimate bug with it not clearing 2nd line
        temp = writing+" "*(31-len(writing))
        if writing != self.laststring:
            board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(temp))
            #print("."+f"{writing:<31}"[:32]+".")
            #print("."+str(temp)+".")
            self.laststring = writing

#arduino verison of HW UI----------------------------------------------
class HW_UI_JEB382_PyFirmat():
    def __init__(self,in_Driver_arr,in_TrainModel_arr,in_output_arr,TestBench=False):
        
        #TODO: ADJUST LENGTH AND INDEX BASED ON I/O dictionary
        
        
        in_output_arr = [1.0,1.0, False,False, False,False, False,False, 0.0, ""]
        self.output_arr = in_output_arr
        
        #-------adjust arrays-------
        #array inputed as an init gets updated as UI is used
        #classes that created this TB have the array they passed locally update with it as well
        if len(in_TrainModel_arr)<12:
            #if array is empty or missing values, autofills at end of missing indexes
            t_TrainModel_arr = [0.0, 0.0, 0.0, 0.0, 0.0, False, False, 0, False, False,False,"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"]
            in_TrainModel_arr = in_TrainModel_arr + t_TrainModel_arr[len(in_TrainModel_arr):]
        #if over, snips
        elif len(in_TrainModel_arr)>12: in_TrainModel_arr = in_TrainModel_arr[0:-(len(in_TrainModel_arr)-12)]
        #ensure beacon arr indx is proper size
        if   len(str(in_TrainModel_arr[-1]))<128: in_TrainModel_arr[-1] = "0"*(128-len(str(in_TrainModel_arr[-1])))+str(in_TrainModel_arr[-1])
        elif len(str(in_TrainModel_arr[-1]))>128: in_TrainModel_arr[-1] = str(in_TrainModel_arr[-1])[len(str(in_TrainModel_arr[-1]))-128:]
        #checks door side state is within range
        if in_TrainModel_arr[7] not in range(0,5): in_TrainModel_arr[7]=0
        #check tickboxes are within limit(0,100)
        limit1=0;limit2=100
        for i in range(0,4):
            if   in_TrainModel_arr[i] < limit1: in_TrainModel_arr[i]=limit1
            elif in_TrainModel_arr[i] > limit2: in_TrainModel_arr[i]=limit2
        
        #print(in_TrainModel_arr); print(len(in_TrainModel_arr))#debug
        self.TrainModel_arr = in_TrainModel_arr
        
        #Driver_arr, is output, the inputted arr is just used for the variable reference
        in_Driver_arr = [1.0, 1.0, 0.0, False, False, 0.0, False, False, False, False, False]
        self.Driver_arr = in_Driver_arr
        
        
        
        
        #+-+-+-+-
        self.init_clk = time.time()#replace with shared time module when created and we do integration
        
        #input sets
        self.TCK_Kp     = POT_PyF(0)
        self.TCK_Ki     = POT_PyF(1)
        self.TCK_CmdSpd = POT_PyF(2)
        self.TCK_Temp   = POT_PyF(3)
        
        self.BTN_CabnLgt = BTN_PyF(38)
        self.BTN_HeadLgt = BTN_PyF(39)#
        self.BTN_Door_L  = BTN_PyF(42)
        self.BTN_Door_R  = BTN_PyF(44)#
        self.BTN_EBRK    = BTN_PyF(46)
        self.BTN_SBRK    = BTN_PyF(48)#
        self.BTN_DisPaEB = BTN_PyF(50)#
        self.BTN_Mode    = BTN_PyF(52)#
        
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
        self.LED_EBRK       = LED_PyF(33)
        self.LED_SBRK       = LED_PyF(34)
        
        self.Announcements=""
        
        self.DISP = DISP_PyF()
        
        #TestBench
        if TestBench:
            self.HW_UI_fin(TestBench)
    
    def updateRead(self):
        self.Driver_arr[3] = self.BTN_CabnLgt.read()
        self.Driver_arr[4] = self.BTN_HeadLgt.read()
        self.Driver_arr[6] = self.BTN_Door_L.read()
        self.Driver_arr[7] = self.BTN_Door_R.read()
        self.Driver_arr[8] = self.BTN_EBRK.read()
        self.Driver_arr[9] = self.BTN_SBRK.read()
        self.Driver_arr[10]= self.BTN_DisPaEB.read()
        
        self.Driver_arr[0] = self.TCK_Kp.read()
        self.Driver_arr[1] = self.TCK_Ki.read()
        self.Driver_arr[2] = self.TCK_CmdSpd.read()
        self.Driver_arr[5] = self.TCK_Temp.read()
        self.Mode = self.BTN_Mode.read()
            
    def updateDisplay(self):
        '''
        self.LED_CabnLgt   .write(self.BTN_CabnLgt.read())
        self.LED_HeadLgt   .write(self.BTN_HeadLgt.read())
        self.LED_Door_L    .write(self.BTN_Door_L .read())
        self.LED_Door_R    .write(self.BTN_Door_R .read())
        self.LED_Pass_EB   .write( bool(self.TrainModel_arr[5]) )
        self.LED_Track_Circ.write( bool(self.TrainModel_arr[6]) )
        self.LED_Stat_Side2.write( self.TrainModel_arr[7]>1 ) #_x 2,3
        self.LED_Stat_Side1.write( self.TrainModel_arr[7]%2 ) #x_ 1,3
        self.LED_Sig_Fail  .write( bool(self.TrainModel_arr[-4]) )
        self.LED_Eng_Fail  .write( bool(self.TrainModel_arr[-3]) )
        self.LED_Brk_Fail  .write( bool(self.TrainModel_arr[-2]) )
        self.LED_EBRK  .write( (bool(self.TrainModel_arr[5]) and not bool(self.Driver_arr[10])) or bool(self.Driver_arr[8]) )
        self.LED_SBRK  .write( bool(self.Driver_arr[9]) )
        
        self.DISP.send(self.TrainModel_arr[-1][1:32])'''
        
        #change outputs to out arr
        self.LED_CabnLgt   .write( bool(self.output_arr[6])      )
        self.LED_HeadLgt   .write( bool(self.output_arr[7])      )
        self.LED_Door_L    .write( bool(self.output_arr[4]>1)    )
        self.LED_Door_R    .write( bool(self.output_arr[4]%2)    )
        self.LED_Pass_EB   .write( bool(self.TrainModel_arr[5])  )
        self.LED_Track_Circ.write( bool(self.TrainModel_arr[6])  )
        self.LED_Stat_Side2.write( bool(self.TrainModel_arr[7]>1) ) #_x 2,3
        self.LED_Stat_Side1.write( bool(self.TrainModel_arr[7]%2) ) #x_ 1,3
        self.LED_Sig_Fail  .write( bool(self.TrainModel_arr[-4]) )
        self.LED_Eng_Fail  .write( bool(self.TrainModel_arr[-3]) )
        self.LED_Brk_Fail  .write( bool(self.TrainModel_arr[-2]) )
        self.LED_EBRK  .write( bool(self.output_arr[3]) )
        self.LED_SBRK  .write( bool(self.output_arr[2]) )
        
        #decode message from beacon "(self.TrainModel_arr[-1]" in Update Calc into self.Announcements and display it
        self.DISP.send(self.Announcements)
        
        
        
    def updateCalc(self):
        #fill out self.output_arr and self.Announcements
        pass
        
    def updateTot(self):
        self.updateRead()
        self.updateCalc()
        self.updateDisplay()
        
    def __del__(self):
        print('HW_UI_JEB382_PyFirmat: Destructor called')
        #if self.TB_window: sys.exit(self.app.exec())



    #[{!!!!!!!!!!!!!!!!!!!!!!!!}]
    #can call this just as its class, this implies its not getting information from a testbench which requires threading
    def HW_UI_mainloop_fast(self):
        time.sleep(2)
        global printout
        while True:
            self.updateTot()
            if printout == 1: print(f"Driver TrainC #1:\t{self.Driver_arr}\t{'AUTO' if self.Mode else 'MANUAL'}")
            elif printout == 2: print(f"TrainModel TrainC #1:\t{self.TrainModel_arr}\t{'AUTO' if self.Mode else 'MANUAL'}")
            elif printout == 3: print(f"Output TrainC #1:\t{self.Output_arr}\t{'AUTO' if self.Mode else 'MANUAL'}")


    def HW_UI_fin(self, TestBench=False):
        t1 = threading.Thread(target=self.HW_UI_mainloop_fast, args=())
        t1.start()
        
        if TestBench:
            t2 = threading.Thread(target=TB_pyqtloop, args=(1,self.TrainModel_arr))
            t2.start()
            t2.join()
        t1.join()


if __name__ == "__main__":
    Arduino = True
    
    main_Driver_arr = []#[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    main_TrainModel_arr = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0,0.0,
                           "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"]
    main_output_arr =[] #[7.00]*90
    #w = HW_UI_JEB382_PyFirmat(main_Driver_arr,main_TrainModel_arr,True)
    
    it = util.Iterator(board)  
    it.start()
    
    #global glob_UI
    global printout
    printout=1
    #print("-1234567890abcdefghijklmnopqrstuvvvvv")
    glob_UI = HW_UI_JEB382_PyFirmat(main_Driver_arr,
                                    main_TrainModel_arr,
                                    main_output_arr,
                                    True)
    
        