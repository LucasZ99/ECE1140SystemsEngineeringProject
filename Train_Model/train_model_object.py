class TrainModel:
    def __init__(self, numid=0):
        # physics values
        self.velocity = 0.0
        self.acceleration = 0.0
        self.service_force = 55991.44
        self.emergency_force = 127380.526
        self.grade = 0.0
        self.elevation = 0.0
        self.service_status = False
        self.emergency_status = False
        self.power = 0.0
        self.max_power = 120000
        self.min_power = 0

        # train descriptors
        self.ID = numid
        self.length = 32.2  # per car
        self.height = 3.42
        self.width = 2.65
        self.car_number = 1
        self.passenger_count = 0
        self.max_passenger_count = 222
        self.crew_count = 0
        self.train_mass = 37103.86

        # train services
        self.exterior_light = False
        self.internal_light = True
        self.left_door = False
        self.right_door = False
        self.announcement = ""
        self.cabin_temp = 68  # room temp

        # signals received
        self.commanded_velocity = 0.0
        self.authority = 0.0
        self.beacon = 0

        # failures
        self.engine_failure = False
        self.pickup_failure = False
        self.brake_failure = False

    def set_ID(self, id):
        self.ID = id

    def get_ID(self):
        return self.ID

    def set_velocity(self, vel):
        self.velocity = vel

    def get_velocity(self):
        return self.velocity

    def set_acceleration(self, acc):
        self.acceleration = acc

    def get_acceleration(self):
        return self.acceleration











