class TrainConstruction:
    # constants
    max_passengers_per_car = 222
    mass_per_car = 37103.86  # in kg
    length_per_car = 32.2  # per car in meters
    height = 3.42  # in meters
    width = 2.65  # in meters

    def __init__(self, num_car=1):
        self.car_number = int()
        self.set_cars(num_car)

    def set_cars(self, num_car):
        if num_car < 1:
            self.car_number = 1
        else:
            self.car_number = num_car

    def train_mass(self):
        return self.mass_per_car * self.car_number

    def train_length(self):
        return self.length_per_car * self.car_number

    def max_passengers(self):
        return self.max_passengers_per_car * self.car_number
    