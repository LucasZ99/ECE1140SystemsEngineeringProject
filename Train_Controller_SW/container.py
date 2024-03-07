import trainController
import testbench

# container class for calling everything


class Container:
    def __init__(self):

        self.trainController = trainController.TrainController()
        self.testBench = testbench.TestBench()
        # UI class ? TODO

    #  receiver functions

    def actspeedfromtrain(self):
        pass

    def cmdspeedfromtrain(self):
        pass

    def authorityfromtrain(self):
        pass

    def passebrakefromtrain(self):
        pass

    def polarityfromtrain(self):
        pass

    def doorsidefromtrain(self):
        pass

    def undergroundfromtrain(self):
        pass

    def failurefromtrain(self):
        pass

    def beaconfromtrain(self):
        pass

    # transmitter functions

    def powertotrain(self):
        pass

    def cmdspeedtotrain(self):
        pass

    def ebraketotrain(self):
        pass

    def servicebraketotrain(self):
        pass

    def doorstotrain(self):
        pass

    def announcementtotrain(self):
        pass

    def intlightstotrain(self):
        pass

    def extlightstotrain(self):
        pass

    def temptotrain(self):
        pass

