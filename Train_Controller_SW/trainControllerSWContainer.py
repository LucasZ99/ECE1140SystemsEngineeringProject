import trainControllerSW

# container class for calling everything from train


class Container:
    def __init__(self):
        self.trainCtrl = trainControllerSW.TrainController()
        return

    #  receiver functions

    def updatevalues(self, inputs):

        self.actspeedfromtrain(inputs[0])
        self.cmdspeedfromtrain(inputs[1])
        self.authorityfromtrain(inputs[2])
        self.passebrakefromtrain(inputs[3])
        self.polarityfromtrain(inputs[4])
        self.doorsidefromtrain(inputs[5])
        self.undergroundfromtrain(inputs[6])
        self.beaconfromtrain(inputs[7])

        return

    def actspeedfromtrain(self, newspeed):
        self.trainCtrl.actualSpeed = newspeed
        # self.trainCtrl.powercontrol
        return

    def cmdspeedfromtrain(self, newcmdspd):
        pass

    def authorityfromtrain(self, auth):
        pass

    def passebrakefromtrain(self, newpassbrake):
        pass

    def polarityfromtrain(self, newpolarity):
        pass

    def doorsidefromtrain(self, newdoor):
        pass

    def undergroundfromtrain(self, newunder):
        pass

    def beaconfromtrain(self, newbeacon):
        pass
