import math


class Heater:
    target_temp: float
    # constant
    time_to_set = 20  # in seconds

    def __init__(self, temp=68.0):
        self.initial_temp = temp
        self.target_temp = temp
        self.current_temp = temp
        self.time_constant = 0.0
        self.running_time = 0.0

    def update_target(self, target=float()):
        self.running_time = 0
        self.initial_temp = self.current_temp
        self.target_temp = target
        if target == self.current_temp:
            self.time_constant = 0
        elif self.initial_temp < self.target_temp:
            self.time_constant = math.log(self.target_temp - self.initial_temp) / self.time_to_set
        else:
            self.time_constant = math.log(self.initial_temp - self.target_temp) / self.time_to_set

    def physics_calculation(self, time):
        self.running_time += time
        if self.running_time > 200:
            self.running_time = 200

        self.current_temp = ((self.initial_temp - self.target_temp) *
                             math.exp(-1 * self.time_constant * self.running_time) + self.target_temp)
