import linecache
from SystemTime import SystemTime
import time
from PyQt6.QtCore import pyqtSignal


class TrainController:
    # send: setpt speed, speedlim, actspeed, power, kp, ki to ui
    ui_update = pyqtSignal(float, float, float, float, float, float)

    # signals for ui communication
    mode_to_ui = pyqtSignal()
    extlights_to_ui = pyqtSignal()
    intlights_to_ui = pyqtSignal()
    cabintemp_to_ui = pyqtSignal()
    doorsopen_to_ui = pyqtSignal()
    station_to_ui = pyqtSignal()
    doorside_to_ui = pyqtSignal()
    kp_to_ui = pyqtSignal()
    ki_to_ui = pyqtSignal()
    speedlim_to_ui = pyqtSignal()
    actspeed_to_ui = pyqtSignal()
    setspeed_to_ui = pyqtSignal()
    power_to_ui = pyqtSignal()
    servicebrake_to_ui = pyqtSignal()
    ebrake_to_ui = pyqtSignal()

    # constants
    maxSpeed = 19.44  # 70 kmh in m/s
    maxPower = float(120000)  # in watts
    accelLim = float(0.5)  # acceleration limit of the train based on 2/3 load
    decelLim = float(-1.2)  # deceleration limit of the train based on 2/3 load
    eBrakeDecelLim = float(-2.73)  # deceleration limit of the train emergency brake based on current capacity
    KMH2ms = 3.6  # divide by this to go from KMH to m/s or multiply to go from m/s to KMH
    mph2ms = 2.237  # divide by this to go from mph to m/s or multiply to go from m/s to mph
    kW2HP = 1.34102  # multiply by this to go from kW to HP or divide to go from HP to kW

    def __init__(self):  # , system_time: SystemTime):
        # initial inits
        # self.system_time = SystemTime.time
        self.last_update_time = SystemTime.time()
        self.update_time = SystemTime.time()

        # train mode, as input from driver
        self.mode = bool(0)  # automatic or manual mode as bool: 0 automatic, 1 manual (0 default)
        self.testBenchState = bool(0)  # state of test bench: 0 closed, 1 open (0 default)

        # cabin environment, as inputs from driver
        self.extLights = bool(0)  # headlights as bool: 0 off, 1 on (default 0)
        self.intLights = bool(0)  # cabin lights as bool: 0 off, 1 on (default 0)
        self.doorState = bool(0)  # door open/close status as bool: 0 closed, 1 opened (default 0)
        self.doorL = bool(0)  # door control for left side doors: 0 closed, 1 opened (default 0)
        self.doorR = bool(0)  # door control for right side doors: 0 close, 1 opened (default 0)
        self.extLightsByDriver = bool(False)
        self.intLightsByDriver = bool(False)

        # cabin environment, as inputs from train model
        self.cabinTemp = float(68)  # cabin thermostat temp as float, in Fahrenheit (default 68)

        # environment information, as inputs from train model / beacon
        self.station = str("")  # station name, parsed from beacon / static data
        self.doorSide = int(0)  # station door side: 0 neither, 1 left, 2 right, 3 both
        self.isUnderground = bool(0)  # parsed from beacon, if the train is going underground

        # fail states, as inputs from train model
        self.signalFail = bool(0)  # track circuit signal pick up failure as bool: 0 no fail, 1 fail
        self.engineFail = bool(0)  # engine failure as bool: 0 no fail, 1 fail
        self.brakeFail = bool(0)  # brake failure as bool: 0 no fail, 1 fail

        # train model inputs
        self.actualSpeed = float(0)  # actual speed of the train
        self.cmdSpeed = float(0)  # commanded vital speed of the train, as passed from wayside controller
        self.speedLim = float(31.0686)  # speed limit of the current block, 50 kmh in mph, blue line speed lim
        self.vitalAuth = float(0)  # vital authority for the train, as passed from wayside controller
        self.passEBrake = bool(0)  # passenger emergency brake as bool: 0 off, 1 on
        self.polarity = bool(0)  # track circuit state: 0 left, 1 right
        self.beacon = str("")  # 128 byte message, as passed from track model

        # train vital control, derived from train model inputs or driver/engineer inputs
        # self.currSpeed = float(0.5)  # referenced current speed from actual speed of train model
        self.setPtSpeed = float(0)  # set point speed as determined by driver input
        self.power = float(0)  # power of the train engine as determined by driver and engineer input
        self.servBrake = bool(False)
        self.eBrake = bool(False)  # application of emergency brake as bool: 0 off, 1 on

        self.sBrakeSetByDriver = bool(False)

        # power calculation vars
        self.uk = float(0)
        self.uk1 = float(0)
        self.ek = float(0)
        self.ek1 = float(0)
        self.T = 0  # time between sample from train model(eg time between train controller value updates for IT3)
        # PID gain values, as inputs from engineer
        self.ki = float(500)  # integral gain as float,
        self.kp = float(1000)  # proportional gain as float

        # authority and distance
        self.distanceTraveled = float(-25)
        self.blocksTraveled = int(0)
        self.currentBlock = int(62)

        # vital flags
        self.stopSoon = bool(0)
        self.trainMoving = bool(0)
        self.trainSafeToMove = bool(1)
        self.trainStopped = bool(1)

        self.makeAnnouncement = bool(0)  # if announcement is to be made: 0 no, 1 yes
        self.atStation = bool(0)
        self.station = ""

        self.i = int(1)  # index for reading through block list
        self.blockline = linecache.getline('Resources/IT3_GreenLine.txt', self.i).split("\t")
        self.line = self.blockline[0]
        self.section = self.blockline[1]
        self.block = self.blockline[2]
        self.length = float(self.blockline[3])
        self.speedlim = float(self.blockline[4]) / self.KMH2ms
        self.notes = self.blockline[5]

        self.nextblockline = linecache.getline('Resources/IT3_GreenLine.txt', self.i+1).split("\t")
        self.nextline = self.blockline[0]
        self.nextsection = self.blockline[1]
        self.nextblock = self.blockline[2]
        self.nextlength = float(self.blockline[3])
        self.nextspeedlim = float(self.blockline[4]) / self.KMH2ms
        self.nextnotes = self.blockline[5]

        # TODO: connect signals from ui (from top level signals)

        # TODO: emit init value signals to ui (to top level signals)

    def settestbenchstate(self, newtestbenchstate):
        self.testBenchState = newtestbenchstate
        return

    # def setspeedlim(self, newspeedlim):
    #     self.speedLim = newspeedlim
    #     # if curr speed greater than speed lim need to drop down speeds and power
    #     if self.currSpeed > self.speedLim:
    #         self.currSpeed = self.speedLim
    #     return

    def setvitalauth(self, newvitalauth):
        self.vitalAuth = newvitalauth
        return

    def setbeacon(self, newbeacon):
        self.beacon = newbeacon
        return

    def setactspeed(self, newactspeed):
        if newactspeed >= self.speedlim:
            self.actualSpeed = self.speedlim
        else:
            self.actualSpeed = newactspeed
        return

    def setsetptspeed(self, newsetptspeed):
        if newsetptspeed > self.cmdSpeed:  # new setpt speed cannot exceed command speed, cap at cmd speed
            newsetptspeed = self.cmdSpeed

        if newsetptspeed > self.speedlim:  # new setpt speed cannot exceed speed lim, cap at speed lim
            newsetptspeed = self.speedlim

        if newsetptspeed != self.setPtSpeed:  # TODO need to update engine power
            self.setPtSpeed = newsetptspeed
        return

    def setservbrake(self, newservbrake):
        self.servBrake = newservbrake
        return

    def ebrakecontrol(self, newbrake):
        self.eBrake = newbrake

        if self.eBrake == 1:  # ebrake is on, need to cut power
            self.power = 0
        return

    def ui_ebrakecontrol(self):
        if self.eBrake == 1:
            self.eBrake = 0
        elif self.eBrake == 0:
            self.eBrake = 1  # ebrake turns on
            self.servBrake = False
            self.sBrakeSetByDriver = False
            print(self.servBrake)
            self.power = 0  # power cut

    def passebrakecontrol(self):
        if self.passEBrake == 0:  # ebrake is off
            self.passEBrake = 1  # enable ebrake
            self.power = 0  # kill power
        elif self.passEBrake == 1:  # ebrake is on
            self.passEBrake = 0  # disable ebrake
        return

    def intlightscontrol(self):
        if not self.intLights:
            self.intLights = True  # turn on cabin lights
            self.intLightsByDriver = True
        elif self.intLights:
            self.intLights = False  # turn off cabin lights
            self.intLightsByDriver = False
        return

    def intlightson(self):
        self.intLights = True

    def intlightsoff(self):
        self.intLights = False

    def extlightson(self):
        self.extLights = True

    def extlightsoff(self):
        self.extLights = False

    def extlightscontrol(self):
        if not self.extLights:
            print("turned on")
            self.extLights = True  # turn on headlights
            self.extLightsByDriver = True
        elif self.extLights:
            print("turned off")
            self.extLights = False  # turn off headlights
            self.extLightsByDriver = False
        return

    def tempcontrol(self, temp):
        self.cabinTemp = temp
        return

    def getcabintemp(self):
        return self.cabinTemp

    def doorcontrol(self):
        if self.doorState == 0:  # doors are closed
            self.doorState = 1  # doors will be opened
            if self.doorSide == 1:  # control doors on train left side
                self.doorL = self.doorState  # open left side doors
            elif self.doorSide == 2:  # control doors on train right side
                self.doorR = self.doorState  # open right side doors
            elif self.doorSide == 3 or self.doorSide == 0:  # control doors on both sides
                self.doorL = self.doorState
                self.doorR = self.doorState
            else:  # doorSide = 0 (neither side), or a value that is not previously defined
                self.doorcontrol()  # rerun doorcontrol to ensure doors are closed
        elif self.doorState == 1:  # doors are already opened
            self.doorState = 0  # doors will be closed
            # close all doors
            self.doorL = self.doorState
            self.doorR = self.doorState
        return

    def polaritycontrol(self, newpolarity):
        if self.polarity != newpolarity:
            print("train controller sw.py: polarity changed, train has entered new block")

            self.polarity = newpolarity
            self.blocksTraveled += 1

            print("train controller sw.py: updating distance traveled")
            self.distanceTraveled += self.length
            print(f'train controller sw.py: distance traveled: {self.distanceTraveled + 25}')

            self.i += 1
            self.blockline = linecache.getline('Resources/IT3_GreenLine.txt', self.i).split("\t")
            self.line = self.blockline[0]
            self.section = self.blockline[1]
            self.block = self.blockline[2]
            self.length = float(self.blockline[3])
            self.speedlim = float(self.blockline[4])/self.KMH2ms
            self.notes = self.blockline[5]
            door = self.blockline[6]

            if self.i == 172:
                print("train controller sw.py: looped to yard")
                print()
                self.i = 0

            self.nextblockline = linecache.getline('Resources/IT3_GreenLine.txt', self.i+1).split("\t")
            self.nextline = self.blockline[0]
            self.nextsection = self.blockline[1]
            self.nextblock = self.blockline[2]
            self.nextlength = float(self.blockline[3])
            self.nextspeedlim = float(self.blockline[4])/self.KMH2ms
            self.nextnotes = self.blockline[5]

            print(f'train controller sw.py: current block is: {self.block}')
            if self.notes != "" and self.notes != "SPAWN":
                # print(self.notes)
                # print(door)
                self.atStation = True
                noteslist = self.notes.split("; ", -1)
                self.station = noteslist[1]
                if door == "Right\n" or door == "Right" or str(door) == "Right":
                    self.doorSide = 2
                elif door == "Left\n":
                    self.doorSide = 1
                elif door == "Left/Right\n":
                    self.doorSide = 3
                else:
                    self.doorSide = 0
                print(f'station is: {self.station}')
                print(f'train controller sw.py: door side is {self.doorSide}')
            else:
                self.doorSide = 0
                self.atStation = False

            self.arriveatstation(self.atStation)
        return

    def signalfailcontrol(self):
        if self.signalFail == 0:
            self.signalFail = 1  # enable failure
        elif self.signalFail == 1:
            self.signalFail = 0  # disable failure
        return

    def enginefailcontrol(self):
        if self.engineFail == 0:
            self.engineFail = 1  # enable failure
        elif self.engineFail == 1:
            self.engineFail = 0  # disable failure
        return

    def brakefailcontrol(self):
        if self.brakeFail == 0:
            self.brakeFail = 1  # enable failure
        elif self.brakeFail == 1:
            self.brakeFail = 0  # disable failure
        return

    def parsebeacon(self, beaconinfo):
        currentblock = int(beaconinfo)

    def testbenchcontrol(self):
        if self.testBenchState == 0:
            self.testBenchState = 1
        elif self.testBenchState == 1:
            self.testBenchState = 0

    def failhandler(self):  # i will not be needing this actually, fails will be handled as reactions to other inputs
        if self.signalFail == 1 or self.engineFail == 1 or self.brakeFail == 1:
            self.power = 0

    def powercontrol(self):

        print("train controller sw.py: entered power control")
        self.vitalitycheck()

        print(f'stopSoon: {self.stopSoon}')
        print(f'ebrake: {self.eBrake}')
        print(f'service brake: {self.servBrake}')
        print(f'train safe to move: {self.trainSafeToMove}')
        # do power checks and calcs, train doesn't need to stop, brake not on, train can move
        # stopSoon: false, eBrake: false, trainSafeToMove: true
        if not self.stopSoon and not self.eBrake and self.trainSafeToMove and not self.servBrake:

            if self.nextspeedlim < self.speedlim:
                self.power = 0  # kill power
                self.servBrake = True  # enable service brake and slow down
            elif (self.nextspeedlim == self.speedlim) and (self.actualSpeed >= self.nextspeedlim):
                self.power = 0  # kill power and coast
            else:
                # calculate ek
                self.ek = self.cmdSpeed - self.actualSpeed

                # calculate T interval between calls
                self.update_time = SystemTime.time()
                t = self.update_time - self.last_update_time

                # calculate uk
                self.uk = self.uk1 + (t/2)*(self.ek - self.ek1)

                # power calculation thank you Dr. Profeta (Final Project vF.pdf, slides 61-66) (pages 54-59) :3
                # self.power = self.kp * self.ek + self.ki * self.uk

                # using TMR
                power1 = self.kp * self.ek + self.ki * self.uk
                power2 = self.kp * self.ek + self.ki * self.uk
                power3 = self.kp * self.ek + self.ki * self.uk
                self.power = power1 and power2 and power3

                # check to make sure max power is not exceeded
                if self.power > self.maxPower:
                    print("capping at max")
                    self.power = self.maxPower

                if self.power < 0:
                    self.power = 0  # power can't be negative, enable service brake instead
                    self.servBrake = True
                    print("service brake on")
        else:
            self.power = 0

        print(f'train controller sw.py: power is : {self.power}')

        # closing value updates
        self.last_update_time = self.update_time  # update time becomes last_update_time for next call
        self.ek1 = self.ek  # current ek become ek-1 for next call
        self.uk1 = self.uk  # current ek become uk-1`for next call

        # self.ui_update.emit(self.setPtSpeed, self.speedlim, self.actualSpeed, self.power, self.kp, self.ki)
        # print("train controller sw.py: signal emitted")

    def authority(self):
        print("train controller sw.py: in authority func")
        if self.vitalAuth is not None:
            if self.vitalAuth < 4:
                print(f'train controller sw.py: train authority less then 4, currently at {self.vitalAuth}')
                self.stopSoon = True
                self.power = 0
                if not self.sBrakeSetByDriver:
                    self.servBrake = True
            elif self.vitalAuth >= 4:
                self.stopSoon = False
                if not self.sBrakeSetByDriver:
                    self.servBrake = False
                print("train controller sw.py: train authority has been given authority 4, able to move forward")
        else:
            self.vitalAuth = None
            self.eBrake = True


        print("train controller sw.py: authority updated")

    def vitalitycheck(self):

        self.authority()
        self.speedcheck()
        # perform vitality checks to determine if train has right parameters to move
        if self.vitalAuth == 0:
            self.trainSafeToMove = False
            print("train controller sw.py: train unsafe to move: no authority")
        elif self.vitalAuth != 0 and self.cmdSpeed == 0:
            self.trainSafeToMove = False
            print("train controller sw.py: train unsafe to move: no commanded speed")
        elif self.vitalAuth != 0 and self.cmdSpeed != 0:
            self.trainSafeToMove = True
            print("train controller sw.py: rain safe to move: authority and cmd speed received")
        elif self.vitalAuth is None or self.cmdSpeed is None:
            self.trainSafeToMove = False

        print()

    def speedcheck(self):
        # check if cmd speed and actual speed are within legal speed limits:
        if self.cmdSpeed is not None:
            if self.cmdSpeed > self.speedlim:
                print("train controller sw.py: command speed too high, limiting to speed limit")
                self.cmdSpeed = self.speedlim
            elif self.cmdSpeed <= self.speedlim:
                print("train controller sw.py: command speed within speed limits")
        else:
            self.cmdSpeed = None
            print("No speed picked up, signal pick up failure")
            self.eBrake = True

        print()

    def modeswitch(self):
        if self.mode == 0:  # train in auto
            self.mode = 1  # put into manual
        elif self.mode == 1:  # train in manual
            self.mode = 0  # put into auto
        return

    def ms2mph(self, ms):
        return ms * self.mph2ms

    def updater(self, inputs, num):
        print("train controller sw.py: train controller values being updated in back")
        print(inputs)

        if not self.sBrakeSetByDriver:
            self.servBrake = False  # turn off service brake, will be turned on if needed again
        # print("serve brake turned off")
        # called from train controller container when train sends new values
        # perform all calculations for new values here and update output array

        # update all values and call control functions

        self.update_time = SystemTime.time()

        if num == 1:
            print("train controller sw.py: update type 1 values (authority safe speed): authority and cmd speed")
            self.vitalAuth = inputs[0]  # authority is distance to destination
            # print(self.vitalAuth)
            # print(inputs[0])
            print(inputs)
            print()

            self.cmdSpeed = inputs[1]
            # print(self.cmdSpeed)
            # self.speedcheck()

            # distance control
            self.vitalitycheck()
            # self.authority()
        elif num == 2:
            print("train controller sw.py: update type 2 values (track info): polarity, underground, beacon")
            print(inputs)
            print()
            # check if in new block and update block values
            self.polaritycontrol(inputs[0])
            self.isUnderground = inputs[1]

            if self.isUnderground:
                self.intlightson()
                self.extlightson()
            elif not self.isUnderground and not self.extLightsByDriver and not self.intLightsByDriver:
                self.intlightsoff()
                self.extlightsoff()

            if self.intLights:
                print("train controller sw.py: cabin lights on")
            elif not self.intLights:
                print("train controller sw.py: cabin lights off")

            if self.extLights:
                print("train controller sw.py: headlights on")
            elif not self.extLights:
                print("train controller sw.py: headlights off")
            print()

            self.beacon = inputs[2]
            self.parsebeacon(self.beacon)
        elif num == 3:
            print("train controller sw.py: update type 3 values (train info): actual speed, passenger e-brake")
            print(inputs)

            self.actualSpeed = inputs[0]
            self.passEBrake = inputs[1]
            print
            #self.ebrakecontrol(self.passEBrake)

            if self.passEBrake:
                self.eBrake = True

            # power stuff
            self.powercontrol()
            print(f'train controller sw.py: power is {self.power}')

            # if self.atStation and self.actualSpeed == 0 and self.power == 0:
            #     self.doorcontrol()
            #     print(f'entered station: doorstate is {self.doorState}')
            #     SystemTime.pause()
            #     time.sleep(60/SystemTime.scale)
            #     self.doorcontrol()
            #     print(f'leaving station: doorstate is: {self.doorState}')

        return

    def arriveatstation(self, is_at_station):
        if is_at_station and self.actualSpeed == 0 and self.power == 0:
            print(f'entered station at: {SystemTime.time()}')
            self.doorcontrol()
            print(f'opening doors, door state is {self.doorState}')
            # time.sleep(6)  # waits at station for 60 seconds, set to 6 seconds for individual module purposes
            self.doorcontrol()
            print(f'closing doors, door state is: {self.doorState}')
            print(f'left station at: {SystemTime.time()}')

    def old_updater(self, inputs):
        print("train controller sw.py: train controller values being updated in old")
        self.servBrake = False  # turn off service brake, will be turned on if needed again
        # print("serve brake turned off")
        # called from train controller container when train sends new values
        # perform all calculations for new values here and update output array

        # update all values and call control functions

        self.update_time = SystemTime.time()

        # check if in new block and update block values
        self.polaritycontrol(inputs[4])

        self.actualSpeed = inputs[0]
        #print("actual speeded")
        self.cmdSpeed = inputs[1]
        #print("cmd speeded")
        self.vitalAuth = inputs[2]  # authority is distance to destination
        print(self.vitalAuth)
        print(inputs[2])
        #print("authority changed")
        # distance control
        self.authority()
        #print("authority controlled")
        # ebrake control here
        self.passEBrake = inputs[3]
        #print("ebraked")

        self.isUnderground = inputs[5]
        #print("undregrounded")
        self.beacon = inputs[6]
        #print("beaconed")

        # power stuff
        self.powercontrol()
        #print("powered")
        print(f'power is {self.power}')
        # update all values in output array and call train model container update function
        # reference adjacent container (train model cntr)
        # call update function to inject new values to train model
        # 8 el list + cabin temp
        outputs = [self.power, self.servBrake, self.eBrake, self.doorSide, self.makeAnnouncement,
                   self.intLights, self.extLights]

        print("all values updated")

        return outputs

    def update_train_model_from_train_controller(self):
        print("train controller sw.py: updating train model values")

        # update all values in output array and call train model container update function
        # reference adjacent container (train model cntr)
        # call update function to inject new values to train model
        # 8 el list + cabin temp

        outputs = [self.cmdSpeed, self.power, self.servBrake, self.eBrake, self.doorSide, self.station,
                   self.intLights, self.extLights, self.cabinTemp]
        return outputs
