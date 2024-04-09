import os, sys, time, datetime, shutil
#print(f"FILE:\t\t<{__file__[-10:-3]}>")
#print(f"FILE2:\t\t<{sys.argv[0][-10:-3]}>")

from Tovarish_Belback_Jonah_Train_Controller_Testbenchv2 import *
from Tovarish_Belback_Jonah_Train_Controller_HW_UI_PyFirmata import *


#================================================================================
#testing func
def PTSD_test(file, title_str,variable,expected,perc=None,Controller=None):
    #float
    if perc:
        file.write("\n-------------\n")
        test = ( variable <= expected*(1+(perc/100)) and variable >= expected*(1-(perc/100)) )        
        file.write(f"{title_str}: <{'PASS' if test else 'FAIL'}>\n")
        file.write(f"REAL:\t<{variable}>\t\tGOAL:\t<{expected}> *<{perc}>% (<{expected*(1+(perc/100))}>,<{expected*(1-(perc/100))}>)\n")
        file.write(f"ERR:\t<{variable - expected}>\n")
    #other
    else:
        file.write("\n-------------\n")
        test = ( variable == expected )        
        file.write(f"{title_str}: <{'PASS' if test else 'FAIL'}>\n")
        file.write(f"REAL:\t<{variable}>\t\tGOAL:\t<{expected}>\n")
    
    if Controller:
        file.write(f"Driver TrainC #1:\t{Controller.Driver_arr}\t{'AUTO' if not Controller.Mode else 'MANUAL'}\n")
        file.write(f"TrainModel TrainC #1:\t{Controller.TrainModel_arr} {'AUTO' if not Controller.Mode else 'MANUAL'}\n")
        file.write(f"Output TrainC #1:\t{Controller.output_arr}\t{'AUTO' if not Controller.Mode else 'MANUAL'}\n")
        
    return test



#================================================================================
#get testing folder
def get_testing_folder():
    print("================================================================================")
    print("\n\n[!!!!!!!] TESTING:\t get_testing_folder")
    
    #reset log folder for todays date
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"DIRECTORY:\t\t{dir_path}>")
    
    if os.path.exists(dir_path+'\Testlogs'):
        #folder path and name
        print(f"TIME:\t\t<{str(datetime.datetime.now())[:10]}>")
        test_dir = f"{dir_path}\Testlogs\{str(datetime.datetime.now())[:10]}"
        print(f"TESTING DIRECTORY:\t\t<{test_dir}>")
        
        #deleting folder if it exists
        if os.path.exists( test_dir ):
            print(f"ATTENTION!!!!!!!!!!!!!!!!!!!\nLOG FOLDER ALREADY EXISTS\nDELETE?: {test_dir}........")
            inp = input("y/n: ")
            if inp.lower() in ["n","no"]:
                raise TypeError("TRAIN CONTROLLER HW TESTING:\t\tNO DELETION")
            elif inp.lower() in ["y","ye","yes"]:
                print("DELETING...")
                shutil.rmtree( test_dir )
            else:
                raise TypeError("TRAIN CONTROLLER HW TESTING:\t\tINVALID SELECTION")
        
        #remake folder    
        os.makedirs(test_dir)
        print("DIRECTORY MADE")
    else:
        raise TypeError("TRAIN CONTROLLER HW TESTING:\t\tNO Testlogs DIRECTORY")
    
    return test_dir



#================================================================================
#Passenger Break enables eBrake
def pass_ebreak_enable(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 00pass_ebreak_enable")
    print(f"file:\t\t{folder}/00pass_ebreak_enable.txt")
    file = open(f"{folder}/00pass_ebreak_enable.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    trainCtrl.TrainModel_arr[3] = True #passenger brake
    Endcase *= PTSD_test(file, "PASSENGER EBRAKE: CHANGE1", trainCtrl.TrainModel_arr[3], True)
    trainCtrl.updateCalc()
    Endcase *= PTSD_test(file, "PASSENGER EBRAKE: AUTO", trainCtrl.output_arr[3], True, Controller=trainCtrl)
    
    trainCtrl.TrainModel_arr[3] = False #passenger brake
    Endcase *= PTSD_test(file, "PASSENGER EBRAKE: CHANGE2", trainCtrl.TrainModel_arr[3], False)
    trainCtrl.updateCalc()
    Endcase *= PTSD_test(file, "PASSENGER EBRAKE: REMOVED", trainCtrl.output_arr[3], False, Controller=trainCtrl)
    
    trainCtrl.TrainModel_arr[3] = True #passenger brake
    Endcase *= PTSD_test(file, "PASSENGER EBRAKE: CHANGE3", trainCtrl.TrainModel_arr[3], True)
    trainCtrl.Mode = True
    trainCtrl.updateCalc()
    Endcase *= PTSD_test(file, "PASSENGER EBRAKE: MANUAL", trainCtrl.output_arr[3], True, Controller=trainCtrl)
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Driver can disable Passenger Brake's effect in any mode
def driver_disable_pass(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 01driver_disable_pass")
    print(f"file:\t\t{folder}/01driver_disable_pass.txt")
    file = open(f"{folder}/01driver_disable_pass.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Driver can enable ebrake in any mode
def driver_ebreak_enable(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 02driver_ebreak_enable")
    print(f"file:\t\t{folder}/02driver_ebreak_enable.txt")
    file = open(f"{folder}/02driver_ebreak_enable.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Driver can enable service brake in manual mode only
def driver_sbreak_enable(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 03driver_sbreak_enable")
    print(f"file:\t\t{folder}/03driver_sbreak_enable.txt")
    file = open(f"{folder}/03driver_sbreak_enable.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Driver can change door state when train is stopped in manual mode
def driver_door(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 04driver_door")
    print(f"file:\t\t{folder}/04driver_door.txt")
    file = open(f"{folder}/04driver_door.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Train opens stationside door when train is stopped in auto mode
def train_door(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 05train_door")
    print(f"file:\t\t{folder}/05train_door.txt")
    file = open(f"{folder}/05train_door.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Driver can enable interior lights in manual when it is otherwise off
def driver_int_lights(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 06driver_int_lights")
    print(f"file:\t\t{folder}/06driver_int_lights.txt")
    file = open(f"{folder}/06driver_int_lights.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Driver can enable exterior lights in manual mode when it is otherwise off.
def driver_ext_lights(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 07driver_ext_lights")
    print(f"file:\t\t{folder}/07driver_ext_lights.txt")
    file = open(f"{folder}/07driver_ext_lights.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Power is zero without authority
def zero_pow_auth(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 08zero_pow_auth")
    print(f"file:\t\t{folder}/08zero_pow_auth.txt")
    file = open(f"{folder}/08zero_pow_auth.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Power is zero without commanded speed
def zero_pow_cmdspd(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 09zero_pow_cmdspd")
    print(f"file:\t\t{folder}/09zero_pow_cmdspd.txt")
    file = open(f"{folder}/09zero_pow_cmdspd.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Enable of Emergency brake turns off service brake
def brake_overturn(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 10brake_overturn")
    print(f"file:\t\t{folder}/10brake_overturn.txt")
    file = open(f"{folder}/10brake_overturn.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Turn on both lights when given lack of ambient light in both modes
def amb_light_on(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 11amb_light_on")
    print(f"file:\t\t{folder}/11amb_light_on.txt")
    file = open(f"{folder}/11amb_light_on.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#turn off both lights when given ambient light in both mode, unless enabled by driver in manual
def amb_light_off(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 12amb_light_off")
    print(f"file:\t\t{folder}/12amb_light_off.txt")
    file = open(f"{folder}/12amb_light_off.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Train calculates correct stopping distance with current speed
def stop_dist(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 13stop_dist")
    print(f"file:\t\t{folder}/13stop_dist.txt")
    file = open(f"{folder}/13stop_dist.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Train enables service brake within correct stopping distance
def sbrake_dist(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 14sbrake_dist")
    print(f"file:\t\t{folder}/14sbrake_dist.txt")
    file = open(f"{folder}/14sbrake_dist.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Train enables emergency brake if it cant stop in time
def ebrake_dist(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 15ebrake_dist")
    print(f"file:\t\t{folder}/15ebrake_dist.txt")
    file = open(f"{folder}/15ebrake_dist.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Train gives station when in the block
def announce_stat_block(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 16announce_stat_block")
    print(f"file:\t\t{folder}/16announce_stat_block.txt")
    file = open(f"{folder}/16announce_stat_block.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")


#----------------------------------------------
#Driver can adjust Temperature in any mode within limit
def driver_temp(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t 17driver_temp")
    print(f"file:\t\t{folder}/17driver_temp.txt")
    file = open(f"{folder}/17driver_temp.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")



#----------------------------------------------
#must be done by a person manually
'''#HW: correct buttons correspond to correct changes in driver array
def pass_break_enable(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t pass_break_enable")
    print(f"file:\t\t{folder}/pass_break_enable.txt")
    file = open(f"{folder}/pass_break_enable.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")



#HW: display corresponds to store information
def pass_break_enable(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t pass_break_enable")
    print(f"file:\t\t{folder}/pass_break_enable.txt")
    file = open(f"{folder}/pass_break_enable.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")



#HW: displayes "APP" when within authority of a station
def pass_break_enable(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t pass_break_enable")
    print(f"file:\t\t{folder}/pass_break_enable.txt")
    file = open(f"{folder}/pass_break_enable.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")



#HW: displayers "NOW:" when in a station
def pass_break_enable(folder):
    #prints, prep log
    print("================================================================================")
    print("\n[!!!!!!!] TESTING:\t pass_break_enable")
    print(f"file:\t\t{folder}/pass_break_enable.txt")
    file = open(f"{folder}/pass_break_enable.txt", 'w')
    file.write("Hi\n")
    
    #----------------------------------------------
    #making controller
    main_TrainModel_arr = [0,0,0,False,False,False,"0"*128]
    main_output_arr = []
    main_Driver_arr = []
    
    try: it = util.Iterator(board); it.start()
    except: print("No Train Controller HW detected: util.Iterator")
    
    trainCtrl = HW_UI_JEB382_PyFirmat(main_Driver_arr, main_TrainModel_arr, main_output_arr)
    
    #----------------------------------------------
    #Testing
    Endcase = True
    
    
    
    
    
    #----------------------------------------------
    #Endcase
    file.write("\n-------------\n")
    file.write(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>\n")

    print("\n-------------")
    print(f"[!!!!!] 00pass_ebreak_enable: <{'PASS' if Endcase else 'FAIL'}>")

'''









#================================================================================
#================================================================================
if __name__ == "__main__":
    #folder: test_dir
    test_dir = get_testing_folder()
    
    
    #Passenger Break enables eBrake
    pass_ebreak_enable(test_dir)
    #Driver can disable Passenger Brake's effect in any mode
    '''driver_disable_pass(test_dir)
    #Driver can enable ebrake in any mode
    driver_ebreak_enable(test_dir)
    #Driver can enable service brake in manual mode only
    driver_sbreak_enable(test_dir)
    #Driver can change door state when train is stopped in manual mode
    driver_door(test_dir)
    #Train opens stationside door when train is stopped in auto mode
    train_door(test_dir)
    #Driver can enable interior lights in manual when it is otherwise off
    driver_int_lights(test_dir)
    #Driver can enable exterior lights in manual mode when it is otherwise off.
    driver_ext_lights(test_dir)
    #Power is zero without authority
    zero_pow_auth(test_dir)
    #Power is zero without commanded speed
    zero_pow_cmdspd(test_dir)
    #Enable of Emergency brake turns off service brake
    brake_overturn(test_dir)
    #Turn on both lights when given lack of ambient light in both modes
    amb_light_on(test_dir)
    #turn off both lights when given ambient light in both mode, unless enabled by driver in manual
    amb_light_off(test_dir)
    #Train calculates correct stopping distance with current speed
    stop_dist(test_dir)
    #Train enables service brake within correct stopping distance
    sbrake_dist(test_dir)
    #Train enables emergency brake if it cant stop in time
    ebrake_dist(test_dir)
    #Train gives station when in the block
    announce_stat_block(test_dir)
    #Driver can adjust Temperature in any mode within limit
    driver_temp(test_dir)'''
    
    #NOTE: [!!!!!!!!!!] Must be done manually
    #HW: correct buttons correspond to correct changes in driver array
    #HW: display corresponds to store information
    #HW: displayes "APP" when within authority of a station
    #HW: displayers "NOW:" when in a station
