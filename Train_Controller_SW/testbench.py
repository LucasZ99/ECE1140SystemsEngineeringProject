class TestBench:
    def __init__(self):

        self.actualSpeed = float(0)
        self.cmdedSpeed = float(0)
        self.speedLim = float(0)
        self.vitalAuthority = float(0)
        self.accelLimit = float(0)
        self.decelLimit = float(0)
        self.eBrakeDecelLimit = float(0)
        self.passengerBrake = bool(0)
        self.circuitPolarityTB = bool(0)
        self.signalPickupFailure = bool(0)
        self.engineFailure = bool(0)
        self.brakeFailure = bool(0)
        self.doorsOpen = bool(0)
        self.beaconInfo = ""

    def setactualspeed(self, newv):
        pass
