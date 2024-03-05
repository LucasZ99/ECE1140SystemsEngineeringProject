class Engine:
    # constants
    max_power = 120000  # in watts
    min_power = 0  # in watts

    def __init__(self, pwr=0.0):
        self.power = float()
        self.set_power(pwr)  # in watts

    def set_power(self, pwr):
        if pwr <= self.min_power:
            self.power = self.min_power
        elif pwr >= self.max_power:
            self.power = self.max_power
        else:
            self.power = pwr

    def force_from_engine(self, vel, fail):
        if fail:
            return 0.0
        elif vel == 0 and self.power == 0:
            return 0.0
        else:
            if vel == 0:
                vel = 0.1
            return self.power/vel
