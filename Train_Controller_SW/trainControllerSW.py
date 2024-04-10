# import numpy as np
import time
import linecache
from SystemTime import SystemTime


class TrainController:

    maxSpeed = 19.44  # 70 kmh in m/s
    maxPower = 120000  # in watts
    accelLim = float(0.5)  # acceleration limit of the train based on 2/3 load
    decelLim = float(-1.2)  # deceleration limit of the train based on 2/3 load
    eBrakeDecelLim = float(-2.73)  # deceleration limit of the train emergency brake based on current capacity
    KMH2ms = 3.6  # divide by this to go from KMH to m/s or multiply to go from m/s to KMH
    mph2ms = 2.237  # divide by this to go from mph to m/s or multiply to go from m/s to mph
    kW2HP = 1.34102  # multiply by this to go from kW to HP or divide to go from HP to kW
    # TODO uk, uk-1 values and ek ek-1 values e is m/s and u is m

    # testing arrays IT2
    # formatted as [uk, uk-1, ek, ek-1], "sampled" every 5 seconds from train model
    # arr = np.array([[1.25, 0, 0.5, 0], [6.25, 1.25, 1.5, 0.5], [15.625, 6.25, 2.25, 1.5], [26.25, 15.625, 2, 2.25],
    #                 [31.875, 26.25, 0.25, 2], [26.875, 31.875, -2.25, 0.25], [10.625, 26.875, -4.25, -2.25]])

    # t_arr = np.array([[0.5, 0, 0.2, 0], [2, 0.5, 0.4, 0.2], [4.25, 2, 0.5, 0.4], [6.25, 4.25, 0.3, 0.5],
    #                  [6.5, 6.25, -0.2, 0.3], [4.25, 6.5, -0.7, -0.2], [0, 4.25, -1, -0.7]])

    def __init__(self, system_time: SystemTime):
        # initial inits
        self.system_time = system_time
        self.last_update_time = self.system_time.time()
        self.update_time = self.system_time.time()

        # train mode, as input from driver
        self.mode = bool(0)  # automatic or manual mode as bool: 0 automatic, 1 manual (0 default)
        self.testBenchState = bool(0)  # state of test bench: 0 closed, 1 open (0 default)

        # cabin environment, as inputs from driver
        self.extLights = bool(0)  # headlights as bool: 0 off, 1 on (default 0)
        self.intLights = bool(0)  # cabin lights as bool: 0 off, 1 on (default 0)
        self.doorState = bool(0)  # door open/close status as bool: 0 closed, 1 opened (default 0)
        self.doorL = bool(0)  # door control for left side doors: 0 closed, 1 opened (default 0)
        self.doorR = bool(0)  # door control for right side doors: 0 close, 1 opened (default 0)

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
        self.cmdSpeed = float(31.0686)  # commanded vital speed of the train, as passed from wayside controller
        # self.speedLim = float(31.0686)  # speed limit of the current block, 50 kmh in mph, blue line speed lim
        self.vitalAuth = float(0)  # vital authority for the train, as passed from wayside controller
        self.passEBrake = bool(0)  # passenger emergency brake as bool: 0 off, 1 on
        self.polarity = bool(0)  # track circuit state: 0 left, 1 right
        self.beacon = str("")  # 128 byte message, as passed from track model

        # train vital control, derived from train model inputs or driver/engineer inputs
        # self.currSpeed = float(0.5)  # referenced current speed from actual speed of train model
        self.setPtSpeed = float(0)  # set point speed as determined by driver input
        self.power = float(0)  # power of the train engine as determined by driver and engineer input
        self.servBrake = bool(0)
        self.eBrake = bool(0)  # application of emergency brake as bool: 0 off, 1 on

        self.prevSpeed = float(0)  # velocity of previous step

        # power calculation vars
        self.uk = float(0)
        self.uk1 = float(0)
        self.ek = float(0)
        self.ek1 = float(0)
        self.T = 0  # time between sample from train model(eg time between train controller value updates for IT3)
        # PID gain values, as inputs from engineer
        self.ki = float(50)  # integral gain as float,
        self.kp = float(50)  # proportional gain as float

        # authority and distance
        self.distanceTraveled = float(-25)
        self.blocksTraveled = int(0)
        self.currentBlock = int(62)

        # vital flags
        self.stopSoon = bool(0)
        self.trainMoving = bool(0)
        self.trainSafeToMove = bool(0)
        self.trainStopped = bool(1)

        self.makeAnnouncement = bool(0)  # if announcement is to be made: 0 no, 1 yes
        self.station = bool(0)

        self.i = int(1)  # index for reading through block list
        self.blockline = linecache.getline('Resources/IT3_GreenLine.txt', self.i).split("\t")
        self.line = self.blockline[0]
        self.section = self.blockline[1]
        self.block = self.blockline[2]
        self.length = float(self.blockline[3])
        self.speedlim = float(self.blockline[4])
        self.notes = self.blockline[5]

        self.blockline = linecache.getline('Resources/IT3_GreenLine.txt', self.i+1).split("\t")
        self.nextline = self.blockline[0]
        self.nextsection = self.blockline[1]
        self.nextblock = self.blockline[2]
        self.nextlength = float(self.blockline[3])
        self.nextspeedlim = float(self.blockline[4])
        self.nextnotes = self.blockline[5]

    def settestbenchstate(self, newtestbenchstate):
        self.testBenchState = newtestbenchstate
        return

    def setspeedlim(self, newspeedlim):
        self.speedLim = newspeedlim
        # TODO if curr speed greater than speed lim need to drop down speeds and power
        if self.currSpeed > self.speedLim:
            self.currSpeed = self.speedLim
        return

    def setvitalauth(self, newvitalauth):
        self.vitalAuth = newvitalauth
        return

    def setbeacon(self, newbeacon):
        self.beacon = newbeacon
        return

    def setcurrspeed(self, newcurrspeed):
        self.currSpeed = newcurrspeed
        return

    def setsetptspeed(self, newsetptspeed):
        if newsetptspeed > self.cmdSpeed:  # new setpt speed cannot exceed command speed, cap at cmd speed
            newsetptspeed = self.cmdSpeed

        if newsetptspeed > self.speedLim:  # new setpt speed cannot exceed speed lim, cap at speed lim
            newsetptspeed = self.speedLim

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

    def passebrakecontrol(self):
        if self.passEBrake == 0:  # ebrake is off
            self.passEBrake = 1  # enable ebrake
            self.power = 0  # kill power
        elif self.passEBrake == 1:  # ebrake is on
            self.passEBrake = 0  # disable ebrake
        return

    def intlightscontrol(self):
        if self.intLights == 0:
            self.intLights = 1  # turn on cabin lights
        elif self.intLights == 1:
            self.intLights = 0  # turn off cabin lights
        return

    def intlightson(self):
        self.intLights = 1

    def intlightsoff(self):
        self.intLights = 0

    def extlightson(self):
        self.extLights = 1

    def extlightsoff(self):
        self.extLights = 0

    def extlightscontrol(self):
        if self.extLights == 0:
            self.extLights = 1  # turn on headlights
        elif self.extLights == 1:
            self.extLights = 0  # turn off headlights
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

    def polaritycontrol(self, newpolarity):  # TODO change to check for diff between old polarity and new polarity
        if self.polarity != newpolarity:
            print("polarity changed, train has entered new block")
            self.polarity = newpolarity
            self.blocksTraveled += 1

            print("updating distance travelled")
            self.distanceTraveled += self.length

            self.i += 1
            self.blockline = linecache.getline('Resources/IT3_GreenLine.txt', self.i).split("\t")
            self.line = self.blockline[0]
            self.section = self.blockline[1]
            self.block = self.blockline[2]
            self.length = float(self.blockline[3])
            self.speedlim = float(self.blockline[4])
            self.notes = self.blockline[5]

        # if self.polarity == 0:  # track is negative
        #     self.polarity = 1  # switch to positive
        #     self.blocksTraveled += 1
        # elif self.polarity == 1:  # track is positive
        #     self.polarity = 0  # switch to negative
        #     self.blocksTraveled += 1
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
        if not self.stopSoon and not self.eBrake:  # do power checks and calcs, train doesn't need to stop, brake not on

            if self.nextspeedlim < self.speedlim:
                self.power = 0  # kill power
                self.servBrake = 1  # enable service brake and slow down
            elif (self.nextspeedlim == self.speedlim) and (self.currSpeed <= self.speedlim):
                self.power = 0  # kill power and coast
            else:
                # calculate ek
                self.ek = self.cmdSpeed - self.actualSpeed

                # calculate T interval between calls
                self.update_time = self.system_time.time()
                t = self.update_time - self.last_update_time

                # calculate uk
                self.uk = self.uk1 + (t/2)*(self.ek - self.ek1)

                # power calculation thank you Dr. Profeta (Final Project vF.pdf, slides 61-66) (pages 54-59) :3
                self.power = self.kp * self.ek + self.ki * self.uk

                # check to make sure max power is not exceeded
                if self.power > self.maxPower:
                    self.power = self.maxPower

        print(f'power is : {self.power}')

        # closing value updates
        self.last_update_time = self.update_time  # update time becomes last_update_time for next call
        self.ek1 = self.ek  # current ek become ek-1 for next call
        self.uk1 = self.uk  # current ek become uk-1`for next call

    def authority(self):
        print("in authority fxn")
        if self.vitalAuth < 3:
            print(f'train authority less then 4, currently at" {self.vitalAuth}')
            self.stopSoon = True
            self.power = 0
            self.servBrake = True
        elif self.vitalAuth == 4:
            self.stopSoon = False
            self.servBrake = False
            print("train authority has been given authority 4, able to move forward")

    def vitalitycheck(self):
        # perform vitality checks to determine if train has right parameters to move
        if self.vitalAuth == 0:
            self.trainSafeToMove = 0
            print("train unsafe to move: no authority")
        elif self.vitalAuth != 0 and self.cmdSpeed == 0:
            self.trainSafeToMove = 0
            print("train unsafe to move: no commanded speed")
        elif self.vitalAuth != 0 and self.cmdSpeed != 0:
            self.trainSafeToMove = 1
            print("train safe to move: authority and cmd speed received")

    def speedcheck(self):
        # check if cmd speed and actual speed are within legal speed limits:
        if self.cmdSpeed > self.speedlim:
            print("command speed too high, limiting to speed limit")
            self.cmdSpeed = self.speedlim
        elif self.cmdSpeed <= self.speedlim:
            print("command speed within speed limits")

    def automode(self):  # deprecated in IT3, used in IT2 for testing. honk mimimi
        for i in range(0, 7):
            # power cmd = ek * kp + uk * ki, converted to mph rounded to 3 decimal places
            self.power = round(((self.arr[i, 2]*self.kp + self.arr[i, 0]*self.ki)/745.7), 3)

            if self.power < 0:
                self.servBrake = 1
                print("service brake enabled")
            elif self.power > 0:
                self.servBrake = 0
                print("service brake disabled")

            self.currSpeed = self.t_arr[i, 0]  # speed received from train model
            if self.ms2mph(self.currSpeed) > self.speedLim:
                self.currSpeed = self.speedLim/self.mph2ms

            print(f'power = {self.power} HP')
            print(f'current speed = {self.ms2mph(self.currSpeed)} mph')
            time.sleep(2)

    def modeswitch(self):
        if self.mode == 0:  # train in auto
            self.mode = 1  # put into manual
        elif self.mode == 1:  # train in manual
            self.mode = 0  # put into auto
        return

    def ms2mph(self, ms):
        return ms * self.mph2ms

    def updater(self, inputs, num):
        print("train controller values being updated in back")
        self.servBrake = 0  # turn off service brake, will be turned on if needed again
        #print("serve brake turned off")
        # called from train controller container when train sends new values
        # perform all calculations for new values here and update output array

        # update all values and call control functions

        self.update_time = self.system_time.time()

        if num == 1:
            print("update type 1 values (authority safe speed): authority and cmd speed")
            self.vitalAuth = inputs[0]  # authority is distance to destination
            print(self.vitalAuth)
            print(inputs[0])

            self.cmdSpeed = inputs[1]
            print(self.cmdSpeed)

            # distance control
            self.vitalitycheck()
            self.authority()
        elif num == 2:
            print("update type 2 values (track info): polarity, underground, beacon")
            # check if in new block and update block values
            self.polaritycontrol(inputs[0])
            self.isUnderground = inputs[1]

            if self.isUnderground:
                self.intlightson()
                self.extlightson()
            elif not self.isUnderground:
                self.intlightsoff()
                self.extlightsoff()

            self.beacon = inputs[2]
            self.parsebeacon(self.beacon)
        elif num == 3:
            print("update type 3 values (train info): actual speed, passenger e-brake")
            self.actualSpeed = inputs[0]
            self.passEBrake = inputs[1]
            self.ebrakecontrol(self.passEBrake)

            # power stuff
            self.powercontrol()

        print(f'power is {self.power}')

        return

    def old_updater(self, inputs):
        print("train controller values being updated in old")
        self.servBrake = 0  # turn off service brake, will be turned on if needed again
        # print("serve brake turned off")
        # called from train controller container when train sends new values
        # perform all calculations for new values here and update output array

        # update all values and call control functions

        self.update_time = self.system_time.time()

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
        print("updating train model values")

        # update all values in output array and call train model container update function
        # reference adjacent container (train model cntr)
        # call update function to inject new values to train model
        # 8 el list + cabin temp

        outputs = [self.power, self.servBrake, self.eBrake, self.doorSide, self.makeAnnouncement,
                   self.intLights, self.extLights, self.cabinTemp]
        return outputs

