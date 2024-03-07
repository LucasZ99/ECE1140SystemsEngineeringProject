class Signals:
    def __init__(self, comm_speed=0, auth=0, beac=""):
        self.commanded_speed = comm_speed
        self.authority = auth
        self.beacon = beac

    def set_commanded_speed(self, comm_speed, fail):
        if fail:
            self.commanded_speed = 0
        else:
            self.commanded_speed = comm_speed

    def set_authority(self, auth, fail):
        if fail:
            self.authority = 0
        else:
            self.authority = auth

    def package_signals(self):
        return [self.commanded_speed, self.authority, self.beacon]

    def depackage_signals(self, incoming):
        self.commanded_speed = incoming[0]
        self.authority = incoming[1]
        self.beacon = incoming[2]
